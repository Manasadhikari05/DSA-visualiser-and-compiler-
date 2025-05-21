import streamlit as st # type: ignore
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator
import pprint
import io
import contextlib

st.set_page_config(page_title="Compiler", layout="wide")

st.title("🧠 C/C++ Compiler")

# Input area
code_input = st.text_area("Enter your source code here:", height=300)

if st.button("Compile"):
    if not code_input.strip():
        st.warning("Please enter some code.")
    else:
        try:
            # Tokenize
            lexer = Lexer(code_input)
            tokens = lexer.tokenize()

            # Parse
            parser = Parser(tokens)
            ast = parser.parse()

            # Code generation
            codegen = CodeGenerator()
            pycode = codegen.generate(ast)
            ir = codegen.get_ir()

            # Display results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔹 Tokens")
                for token in tokens:
                    st.code(str(token), language="python")

                st.subheader("📦 AST (Abstract Syntax Tree)")
                st.code(pprint.pformat(ast), language="python")

            with col2:
                st.subheader("🛠 Intermediate Representation (IR)")
                st.code("\n".join(ir), language="python")

                st.subheader("🐍 Generated Python Code")
                st.code(pycode, language="python")

                st.subheader("▶️ Execution Output")
                try:
                    output_buffer = io.StringIO()
                    with contextlib.redirect_stdout(output_buffer):
                        exec(pycode, {}, {})
                    execution_output = output_buffer.getvalue()
                except Exception as e:
                    execution_output = f"❌ Error: {str(e)}"
                st.text(execution_output)

        except Exception as e:
            st.error(f"Compilation Error: {e}")
