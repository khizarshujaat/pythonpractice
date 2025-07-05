import streamlit as st

st.title("Unicode Calculator")

# Button layout using Unicode and spaced `+`
layout = [
    ["7", "8", "9", " ÷ "],       # Division symbol
    ["4", "5", "6", " × "],       # Multiplication symbol
    ["1", "2", "3", " − "],       # Minus symbol
    ["0", "C", "=", " ＋ "]      # Fullwidth plus (U+FF0B)
]

# Mapping display symbols to actual Python operators
symbol_map = {
    "÷": "/",
    "×": "*",
    "−": "-",
    "＋": "+"  # Fullwidth plus to normal plus
}

# Initialize expression in session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Render buttons
for i, row in enumerate(layout):
    cols = st.columns(4)
    for j, label in enumerate(row):
        cleaned_label = label.strip()
        if cols[j].button(label, key=f"{i}-{j}"):
            if cleaned_label == "C":
                st.session_state.expression = ""
            elif cleaned_label == "=":
                try:
                    # Convert symbols to Python operators
                    expr = st.session_state.expression
                    for sym, op in symbol_map.items():
                        expr = expr.replace(sym, op)
                    st.session_state.expression = str(eval(expr))
                except:
                    st.session_state.expression = "Error"
            else:
                st.session_state.expression += cleaned_label

# Display current expression or result
st.text_input("Result", value=st.session_state.expression, disabled=True)
