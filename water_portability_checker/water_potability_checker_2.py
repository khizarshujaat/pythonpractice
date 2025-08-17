import streamlit as st
import numpy as np
import joblib
import os

MODEL_FILE_NAME = "water_potability_rf.pkl"

st.set_page_config(page_title="Water Potability Checker", page_icon="🚰", layout="wide")
st.markdown(
    """
    <h1 style="text-align:center; margin-top: 0;">
      🚰 Water Potability Checker By Khizar Shujaat
    </h1>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Load model bundle (.pkl)
# ------------------------------
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, MODEL_FILE_NAME)

if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found: {MODEL_PATH}. Please run `python train_model.py` first.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
FEATURES = bundle["features"]  # training feature order (lowercase)
test_acc = bundle.get("test_accuracy", None)

# Helper: get final estimator name and classes
def get_final_estimator(m):
    if hasattr(m, "steps"):  # Pipeline
        return m.steps[-1][1]
    return m

def get_model_name(m):
    est = get_final_estimator(m)
    return est.__class__.__name__

# ------------------------------
# KPI Metrics Row
# ------------------------------
m1, m2, m3 = st.columns(3)
m1.metric("Test Accuracy", f"{test_acc:.2%}" if test_acc is not None else "—")
m2.metric("Features", f"{len(FEATURES)}")
m3.metric("Model", get_model_name(model))

st.write("Enter the measurements and click **Predict** to see if the water is likely potable.")

# ------------------------------
# Thresholds for quick rule-check panel (cosmetic guidance)
# ------------------------------
THRESHOLDS = {
    "pH": (0.0, 14.0),
    "Hardness": (0, 400),
    "Solids": (0, 100000),
    "Chloramines": (0, 100),
    "Sulfate": (0, 1000),
    "Conductivity": (0, 1000),
    "Organic Carbon": (0, 100),
    "Trihalomethanes": (0, 1000),
    "Turbidity": (0, 100),
}

# Map UI keys -> training feature names
UI_TO_FEATURE = {
    "pH": "ph",
    "Hardness": "hardness",
    "Solids": "solids",
    "Chloramines": "chloramines",
    "Sulfate": "sulfate",
    "Conductivity": "conductivity",
    "Organic Carbon": "organic_carbon",
    "Trihalomethanes": "trihalomethanes",
    "Turbidity": "turbidity",
}

def check_range(value, lo, hi):
    return lo <= value <= hi

def verdict_banner(container, pred: int, prob: float | None):
    if pred == 1:
        bg = "#ecfdf5"; fg = "#065f46"; label = "Water is **Potable**"
    else:
        bg = "#fef2f2"; fg = "#991b1b"; label = "Water is not **Not Potable**"
    # prob_txt = f" • Prob: {prob:.6f}" if prob is not None else ""
    container.markdown(
        f"""
        <div style="padding:1rem;border-radius:12px;background:{bg};color:{fg};border:1px solid #eee">
          <strong>{label}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

def evaluate(inputs: dict):
    """
    inputs: dict with UI keys (e.g., 'pH', 'Hardness', ...)
    Returns: pred, prob, checks(dict), values_by_feature(dict in training order)
    """
    # Rule checks
    checks = {k: check_range(inputs[k], *THRESHOLDS[k]) for k in THRESHOLDS.keys()}

    # Build feature vector in training order
    feature_dict = {UI_TO_FEATURE[k]: float(v) for k, v in inputs.items()}
    values = [feature_dict[f] for f in FEATURES]
    X = np.array([values], dtype=float)

    # Prediction + probability
    pred = int(model.predict(X)[0])
    prob = None
    if hasattr(model, "predict_proba"):
        proba_row = model.predict_proba(X)[0]
        est = get_final_estimator(model)
        try:
            classes = list(est.classes_)
            if 1 in classes:
                idx = classes.index(1)
                prob = float(proba_row[idx])  # P(class=1 -> potable)
            else:
                # fallback: assume positive class is the second column
                prob = float(proba_row[-1])
        except Exception:
            prob = None

    return pred, prob, checks, dict(zip(FEATURES, values))

# ------------------------------
# Two-column layout
# ------------------------------
left, right = st.columns([1.3, 1])

with left:
    st.subheader("Inputs")
    with st.form("water_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        # --- Example defaults (you can change them) ---
        with col1:
            ph = st.number_input("pH", min_value=0.0, max_value=14.0,
                                 value=5.862641, step=0.000001, format="%.6f", help="0.000000–14.000000")
            hardness = st.number_input("Hardness", min_value=0.0,
                                       value=185.065220, step=0.000001, format="%.6f")
            solids = st.number_input("Solids", min_value=0.0,
                                     value=44069.272158, step=0.000001, format="%.6f")
            chloramines = st.number_input("Chloramines", min_value=0.0,
                                          value=4.382721, step=0.000001, format="%.6f")
            sulfate = st.number_input("Sulfate", min_value=0.0,
                                      value=412.690111, step=0.000001, format="%.6f")
        with col2:
            conductivity = st.number_input("Conductivity", min_value=0.0,
                                           value=331.570139, step=0.000001, format="%.6f")
            organic_carbon = st.number_input("Organic Carbon", min_value=0.0,
                                             value=15.306079, step=0.000001, format="%.6f")
            trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0,
                                              value=59.605812, step=0.000001, format="%.6f")
            turbidity = st.number_input("Turbidity", min_value=0.0,
                                        value=5.507421, step=0.000001, format="%.6f")

        # Centered Predict button
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            submitted = st.form_submit_button("Predict", use_container_width=True)

# Prepare containers on the right so they don't jump around
with right:
    st.subheader("Result")
    verdict_placeholder = st.container()
    metrics_row = st.container()
    checks_expander = st.expander("Parameter-by-parameter checks", expanded=False)

# ------------------------------
# On submit: compute + render
# ------------------------------
if submitted:
    user_inputs = {
        "pH": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": chloramines,
        "Sulfate": sulfate,
        "Conductivity": conductivity,
        "Organic Carbon": organic_carbon,
        "Trihalomethanes": trihalomethanes,
        "Turbidity": turbidity,
    }

    with st.spinner("Evaluating water quality..."):
        pred, prob, checks, values_by_feature = evaluate(user_inputs)

    # Verdict banner + metrics on the right
    with right:
        verdict_banner(verdict_placeholder, pred, prob)

        # Small KPI row specific to this prediction
        cA, _ = metrics_row.columns(2)
        passed = sum(checks.values())
        cA.metric("Checks Passed", f"{passed}/9")
        # if prob is not None:
        #     cB.metric("Potability Prob.", f"{prob:.6f}")
        # else:
        #     cB.metric("Potability Prob.", "—")

        # Detailed checks
        with checks_expander:
            for name, ok in checks.items():
                lo, hi = THRESHOLDS[name]
                badge = "✅ OK" if ok else "⚠️ Out of range"
                st.write(f"- **{name}**: {user_inputs[name]:.6f} (target: {lo}–{hi}) {badge}")

else:
    with right:
        st.info("Fill the inputs on the left and click **Predict** to see the result.")
