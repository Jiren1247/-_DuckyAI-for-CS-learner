import asyncio
import helpers.sidebar
from helpers import util
from services import prompts
import services.llm
import streamlit as st

from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide",
    # initial_sidebar_state="collapsed"
)
st.sidebar.title(":memo: Editor settings")

st.title("Generate Code")

documentation, example = st.columns([1, 1], gap="large")

with documentation:
    st.info("""    
    Please wirte your codes here:
    """)
    EDITOR_KEY_PREFIX = "ace-editor"
    if 'editor_id' not in st.session_state:
        st.session_state.editor_id = 0

    # Empty code on first run
    if "code" not in st.session_state:
        st.session_state.code = ""

    if "messages" not in st.session_state:
        initial_messages = []
        st.session_state.messages = initial_messages

    # This is how we update code in the editor - saving it in a session variable "code".
    INITIAL_CODE = st.session_state.code

    # The component parameters are documented in the Streamlit Ace documentation
    # Command-Click on the st_ace function to see the documentation in PyCharm
    # (Ctrl-Click on Windows)

    # st.write(f"#### Code Editor ID: {st.session_state.editor_id}")
    code = st_ace(
        value=INITIAL_CODE,
        language=st.sidebar.selectbox("Language mode", options=LANGUAGES, index=121),
        placeholder="Please write your code here...",
        theme=st.sidebar.selectbox("Theme", options=THEMES, index=25),
        keybinding=st.sidebar.selectbox(
            "Keybinding mode", options=KEYBINDINGS, index=3
        ),
        font_size=st.sidebar.slider("Font size", 5, 24, 14),
        tab_size=st.sidebar.slider("Tab size", 1, 8, 4),
        wrap=st.sidebar.checkbox("Wrap lines", value=False),
        show_gutter=st.sidebar.checkbox("Show gutter", value=True),
        show_print_margin=st.sidebar.checkbox("Show print margin", value=True),
        auto_update=st.sidebar.checkbox("Auto update", value=True),
        readonly=st.sidebar.checkbox("Read only", value=False),
        key=f"{EDITOR_KEY_PREFIX}-{st.session_state.editor_id}",
        height=300,
        min_lines=12,
        max_lines=20
    )
    

with example:
    

    review_button = st.button("Review your code&nbsp;&nbsp;➠", type="primary", key="generate_button_sb")
    debug_button = st.button("Debug your code&nbsp;&nbsp;➠", type="primary", key="generate_button_debug")
    if st.checkbox("Modify Code"):
        modification_request = st.text_input("Your Modification Request")
        if st.button("Modify"):
            explanation = services.prompts.modify_code_prompt(code, modification_request)
            st.write(asyncio.run(helpers.util.run_prompt(explanation, st.empty())))

    review_code_prompt = services.prompts.review_code_prompt(code)
    modify_code_prompt = services.prompts.modify_code_prompt(code, st.session_state.messages)
    debug_code_prompt = services.prompts.debug_code_prompt(code)
    advice = st.empty()
    if review_button:
        asyncio.run(helpers.util.run_prompt(review_code_prompt, advice))
    if debug_button:
        asyncio.run(helpers.util.run_prompt(debug_code_prompt, advice))

# for message in st.session_state.messages:
#     st.write(message["content"])
#     # if modify_button:
#         # asyncio.run(helpers.util.run_prompt(modify_code_prompt, advice))
#         # modified_code = asyncio.run(helpers.util.run_prompt(modify_code_prompt, advice))
#         # st.code(modified_code, language="python")
#         # if prompt := st.chat_input("Ask a software question..."):
#         #     st.session_state.messages.append({"role": "user", "content": prompt})
#         #     # asyncio.run(chat(st.session_state.messages))
#         #     modify_code_prompt = services.prompts.modify_code_prompt(code, st.session_state.messages)
#         #     asyncio.run(chat(helpers.util.run_prompt(modify_code_prompt, advice)))
#     

    st.session_state.code = code

    print("STATE", st.session_state, "INITIAL", INITIAL_CODE, "CURRENT", code)

    
    reload_button = st.button("↪︎ Reload Page", key="reload_button")
    if reload_button:
        # Clear the session code
        del st.session_state['code']

        # Clear the editor component by id
        for k in st.session_state.keys():
            if k.startswith(EDITOR_KEY_PREFIX):
                del st.session_state[k]

        # Increment the editor id
        st.session_state.editor_id += 1

        # Restart the page
        st.experimental_rerun()

