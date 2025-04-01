import asyncio
import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, LANGUAGES, THEMES
from services.prompts import (
    review_prompt,
    modify_code_prompt,
    debug_prompt,
    classify_user_prompt,
    parse_code_and_request
)
import helpers.util

st.set_page_config(
    page_title="Code & Prompt Interface",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.sidebar.title(":memo: Editor settings")

st.title("Code Editor & Prompt on One Screen")

EDITOR_KEY_PREFIX = "ace-editor"
if 'editor_id' not in st.session_state:
    st.session_state.editor_id = 0

# Code Editor on the left, user prompt on the right
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Your Code")
    # Show a Streamlit Ace editor for code input
    code = st_ace(
        value="",
        language=st.sidebar.selectbox("Language mode", options=LANGUAGES, index=121, key="lang_mode_main"),
        placeholder="Write or paste your code here",
        theme=st.sidebar.selectbox("Theme", options=THEMES, index=25, key="theme_main"),
        keybinding=st.sidebar.selectbox("Keybinding", options=KEYBINDINGS, index=3, key="keybinding_main"),
        font_size=st.sidebar.slider("Font size", 5, 24, 14, key="font_size_main"),
        tab_size=st.sidebar.slider("Tab size", 1, 8, 4, key="tab_size_main"),
        wrap=st.sidebar.checkbox("Wrap lines", value=False, key="wrap_lines_main"),
        show_gutter=st.sidebar.checkbox("Show gutter", value=True, key="show_gutter_main"),
        show_print_margin=st.sidebar.checkbox("Show print margin", value=True, key="show_print_margin_main"),
        auto_update=st.sidebar.checkbox("Auto update", value=True, key="auto_update_main"),
        readonly=False,
        key=f"{EDITOR_KEY_PREFIX}-{st.session_state.editor_id}",
        height=200,
        min_lines=12,
        max_lines=40
    )

with col2:
    response_placeholder = st.empty()
    st.write("### Your Prompt")
    user_prompt = st.text_area("", height=60)

    if st.button("Send"):
        advice_placeholder = st.empty()
        try:
            
            classification_prompt = classify_user_prompt(user_prompt)
            messages = [{"role": "user", "content": classification_prompt}]
            messages, classification_result = asyncio.run(helpers.util.run_conversation(messages, advice_placeholder))
            classification = classification_result.strip().lower()

            # Build AI prompt
            ai_prompt = ""
            if classification == "review":
                st.write("### Reviewing code...")
                ai_prompt = review_prompt(code)
            elif classification == "modify":
                st.write("### Modifying code...")
                ai_prompt = modify_code_prompt(user_prompt, code)
            elif classification == "debug":
                st.write("### Debugging code...")
                ai_prompt = debug_prompt(user_prompt, code)
            else:
                ai_prompt = "I'm unable to understand. Can you try explaining it again?"
            
            # Send the classified prompt to AI
            messages2 = [{"role": "user", "content": ai_prompt}]
            messages2, full_response = asyncio.run(helpers.util.run_conversation(messages2, advice_placeholder))
            advice_placeholder.empty()  #
            
            # Display AI response as a single final markdown output
            st.markdown(full_response)

        except Exception as e:
            st.error(f"Error during processing: {e}")

reset_button = st.button("↪︎ Reset")
if reset_button:
    st.session_state.clear()  # Clear all session state keys (code editor, prompt, etc.)
    st.rerun()
