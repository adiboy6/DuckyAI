import streamlit as st


def show() -> None:
    with st.sidebar:
        st.markdown(f"""
            <a href="/" style="color:black;text-decoration: none;">
                <div style="display:flex;align-items:center;margin-bottom:1rem;">
                    <img src="app/static/logo.png" width="80"><span style="color: white">&nbsp;Ducky</span>
                    <span style="font-size: 0.8em; color: grey">&nbsp;&nbsp;v0.1.2</span>
                </div>
            </a>
            """, unsafe_allow_html=True)

        reload_button = st.button("↪︎  Reload Page")
        if reload_button:
            st.session_state.clear()
            st.rerun()


def show_footer() -> None:
    """Display footer with developer credit"""
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #1e1e1e; 
                   border-top: 1px solid #333; padding: 10px; text-align: center; z-index: 1000;">
            <span style="color: #bfc5d3; font-size: 0.9em; font-family: sans-serif;">
                Made in
                <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="16" height="16" style="vertical-align: middle; margin: 0 2px;"> 
                with ❤️ by 
                <a href="https://github.com/adiboy6" target="_blank" style="color: #4CAF50; text-decoration: underline;">@adiboy6</a>
            </span>
        </div>
        """, unsafe_allow_html=True)
