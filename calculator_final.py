import streamlit as st

# Set page config
st.markdown("""
<h1 style='text-align: center; margin-bottom: 10px;'>Khizar Shujaat's Calculator</h1>
""", unsafe_allow_html=True)

# Initialize expression
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Button layout (as strings)
buttons = [
    ["C", "(", ")", "←"],
    ["7", "8", "9", "%"],
    ["4", "5", "6", "÷"],
    ["1", "2", "3", "×"],
    [".", "0", "±", "−"],
    ["=", "", "", " ＋ "]
]

# Button color map
color_map = {
    "C": "red", "←": "red",
    "%": "green", "÷": "green", "×": "green", "−": "green", " ＋ ": "green",
    "=": "orange",
    "0": "blue", "1": "blue", "2": "blue", "3": "blue", "4": "blue", "5": "blue",
    "6": "blue", "7": "blue", "8": "blue", "9": "blue", ".": "blue",
    "(": "blue", ")": "blue", "±": "blue"
}

# Symbol replacement for eval
symbol_map = {
    "÷": "/", "×": "*", "−": "-", " ＋ ":"+"
}

# Custom CSS
st.markdown("""
<style>

div[data-testid="stVerticalBlock"] > div:has(.display-area) {
    
    padding: 20px;
    width: 420px;
    margin: auto;
}

div[data-testid="stVerticalBlock"] > div:has(.stHorizontalBlock) {
    margin-bottom: -25px;
}

div.stButton > button {
    font-size: 20px;
    height: 60px;
    width: 100%;
    border-radius: 8px;
    font-weight: bold;
    margin-bottom: 5px;
}

/* Special equal button that spans 3 columns */
.st-key---orange button {
    grid-column: span 3;
    width: calc(300% + 32px) !important;  /* 3 columns plus gap */
    margin-right: 10px;
}

div[class*="st-key"][class*="-red"] button { background-color: #f44336; color: white; }
div[class*="st-key"][class*="-blue"] button { background-color: #2196f3; color: white; }
div[class*="st-key"][class*="-green"] button { background-color: #8bc34a; color: white; }
div[class*="st-key"][class*="-orange"] button { background-color: #ff9800; color: white; }

</style>
""", unsafe_allow_html=True)

with st.container(border=True):

    # Display area
    st.markdown(f"""
    <div class="display-area" style='
        background: linear-gradient(to bottom, #c2e6fa, #a0d1f2);
        padding: 15px;
        border-radius: 8px;
        font-size: 28px;
        font-weight: bold;
        text-align: right;
        margin-bottom: 20px;
        color: #002B45;
        box-shadow: inset 0 0 5px #0077b6;
        height: 65px;
    '>
        {st.session_state.expression}
    </div>
    """, unsafe_allow_html=True)

    # Render grid buttons
    for row in buttons:
        cols = st.columns(4, vertical_alignment="center")
        for i, btn in enumerate(row):
            if btn == "":
                cols[i].markdown(" ")
                continue

            with cols[i]:
                clicked = st.button(btn, key=f"{btn}-{color_map.get(btn)}")
                # Inject class styling for the most recent button
                st.markdown(
                    f"<script>var btns = parent.document.querySelectorAll('button'); btns[btns.length-1].classList.add('{color_map.get(btn, 'blue')}');</script>",
                    unsafe_allow_html=True
                )
                if clicked:
                    # Check if the last operation was equals
                    last_was_equals = st.session_state.get("last_was_equals", False)

                    if btn == "C":
                        st.session_state.expression = ""
                    elif btn == "←":
                        st.session_state.expression = st.session_state.expression[:-1]
                    elif btn == "=":
                        try:
                            expr = st.session_state.expression
                            for k, v in symbol_map.items():
                                expr = expr.replace(k, v)
                            st.session_state.expression = str(eval(expr))
                            st.session_state.last_was_equals = True
                        except:
                            st.session_state.expression = "Error"
                            st.session_state.last_was_equals = False
                    elif btn == "%":
                        try:
                            # Safely convert last number or entire expression to percentage
                            expr = st.session_state.expression
                            for k, v in symbol_map.items():
                                expr = expr.replace(k, v)
                            result = str(eval(expr) / 100)
                            st.session_state.expression = result
                            st.session_state.last_was_equals = True
                        except:
                            st.session_state.expression = "Error"
                            st.session_state.last_was_equals = False
                    elif btn == "±":
                        if st.session_state.expression.startswith("-"):
                            st.session_state.expression = st.session_state.expression[1:]
                        else:
                            st.session_state.expression = "-" + st.session_state.expression
                    elif btn == " ＋ ":
                        st.session_state.expression += symbol_map.get(btn)
                    else:
                        # Clear display if last operation was equals
                        if last_was_equals:
                            st.session_state.expression = btn if btn != "±" else "-"
                        else:
                            st.session_state.expression += btn
                        st.session_state.last_was_equals = False
                    st.rerun()

