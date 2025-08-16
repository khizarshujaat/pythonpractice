import streamlit as st
import numpy as np
import joblib
import os

MODEL_FILE_NAME = "water_potability_rf.pkl"

st.set_page_config(page_title="Water Potability Checker", page_icon="🚰", layout="centered")

st.title("🚰 Water Potability Checker By Khizar Shujaat")

# Get the directory where this script lives
BASE_DIR = os.path.dirname(__file__)

# Point to the pkl file in the same folder
MODEL_PATH = os.path.join(BASE_DIR, MODEL_FILE_NAME)

# Load model bundle
if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found: {MODEL_PATH}. Please run `python train_model.py` first.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
FEATURES = bundle["features"]
test_acc = bundle.get("test_accuracy", None)

if test_acc is not None:
    st.caption(f"Loaded model • Test accuracy at train time: **{test_acc:.4f}**")

st.write("Enter the measurements and click **Predict** to see if the water is likely potable.")

# --- Input form ---
with st.form("water_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    ## Values for Water is not Potable, Potability Value: 1.000000, Record Number 313
    with col1:
        ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=5.862641, step=0.000001, format="%.6f", help="Recommended 0.0–14.0")
        hardness = st.number_input("Hardness", min_value=0.0, value=185.065220, step=0.000001, format="%.6f", help="Typically ≤ 400")
        solids = st.number_input("Solids", min_value=0.0, value=44069.272158, step=0.000001, format="%.6f", help="Typically ≤ 100000")
        chloramines = st.number_input("Chloramines", min_value=0.0, value=4.382721, step=0.000001, format="%.6f", help="Typically ≤ 100")
        sulfate = st.number_input("Sulfate", min_value=0.0, value=412.690111, step=0.000001, format="%.6f", help="Typically ≤ 1000")
    with col2:
        conductivity = st.number_input("Conductivity", min_value=0.0, value=331.570139, step=0.000001, format="%.6f", help="Typically ≤ 1000")
        organic_carbon = st.number_input("Organic Carbon", min_value=0.0, value=15.306079, step=0.000001, format="%.6f", help="Typically ≤ 100")
        trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0, value=59.605812, step=0.000001, format="%.6f", help="Typically ≤ 1000")
        turbidity = st.number_input("Turbidity", min_value=0.0, value=5.507421, step=0.000001, format="%.6f", help="Typically ≤ 100")

    ## Values for Water is Potable, Portability Value: 0.000000, Record Number 3
    # with col1:
    #     ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=8.316766, step=0.000001, format="%.6f", help="Recommended 0.0–14.0")
    #     hardness = st.number_input("Hardness", min_value=0.0, value=214.373394, step=0.000001, format="%.6f", help="Typically ≤ 400")
    #     solids = st.number_input("Solids", min_value=0.0, value=22018.417441, step=0.000001, format="%.6f", help="Typically ≤ 100000")
    #     chloramines = st.number_input("Chloramines", min_value=0.0, value=8.059332, step=0.000001, format="%.6f", help="Typically ≤ 100")
    #     sulfate = st.number_input("Sulfate", min_value=0.0, value=356.886136, step=0.000001, format="%.6f", help="Typically ≤ 1000")
    # with col2:
    #     conductivity = st.number_input("Conductivity", min_value=0.0, value=363.266516, step=0.000001, format="%.6f", help="Typically ≤ 1000")
    #     organic_carbon = st.number_input("Organic Carbon", min_value=0.0, value=18.436524, step=0.000001, format="%.6f", help="Typically ≤ 100")
    #     trihalomethanes = st.number_input("Trihalomethanes", min_value=0.0, value=100.341674, step=0.000001, format="%.6f", help="Typically ≤ 1000")
    #     turbidity = st.number_input("Turbidity", min_value=0.0, value=4.916218, step=4.628771, format="%.6f", help="Typically ≤ 100")

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        submitted = st.form_submit_button("Predict", use_container_width=True)

# --- Rule thresholds (adjust as needed) ---
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

def check_range(value, lo, hi):
    return lo <= value <= hi

def evaluate_potability(inputs):
    checks = {
        "pH": check_range(inputs["pH"], *THRESHOLDS["pH"]),
        "Hardness": check_range(inputs["Hardness"], *THRESHOLDS["Hardness"]),
        "Solids": check_range(inputs["Solids"], *THRESHOLDS["Solids"]),
        "Chloramines": check_range(inputs["Chloramines"], *THRESHOLDS["Chloramines"]),
        "Sulfate": check_range(inputs["Sulfate"], *THRESHOLDS["Sulfate"]),
        "Conductivity": check_range(inputs["Conductivity"], *THRESHOLDS["Conductivity"]),
        "Organic Carbon": check_range(inputs["Organic Carbon"], *THRESHOLDS["Organic Carbon"]),
        "Trihalomethanes": check_range(inputs["Trihalomethanes"], *THRESHOLDS["Trihalomethanes"]),
        "Turbidity": check_range(inputs["Turbidity"], *THRESHOLDS["Turbidity"]),
    }
    values = [
        inputs["pH"], inputs["Hardness"], inputs["Solids"], inputs["Chloramines"], inputs["Sulfate"],
        inputs["Conductivity"], inputs["Organic Carbon"], inputs["Trihalomethanes"], inputs["Turbidity"]
    ]
    X = np.array([values], dtype=float)

    pred = model.predict(X)[0]

    return pred, checks

if submitted:
    with st.spinner("Evaluating water quality..."):
        inputs = {
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
        # potable, score, checks = evaluate_potability(inputs)
        prediction_result, checks = evaluate_potability(inputs)
        # values = [
        #     ph, hardness, solids, chloramines, sulfate,
        #     conductivity, organic_carbon, trihalomethanes, turbidity
        # ]
        # X = np.array([values], dtype=float)

        # pred = model.predict(X)[0]

    if prediction_result == 1:
        st.success("✅ Water is **Potable**")
    else:
        st.error("❌ Water is **Not Potable**")

    with st.expander("See parameter-by-parameter checks"):
        for name, ok in checks.items():
            rng = THRESHOLDS[name] if name != "Trihalomethanes" else THRESHOLDS["Trihalomethanes"]
            badge = "✅ OK" if ok else "⚠️ Out of range"
            st.write(f"- **{name}**: {inputs[name]} (target: {rng[0]}–{rng[1]}) {badge}")
