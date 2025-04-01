from typing import List, Dict, Union, Tuple

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import services.llm
import services.rag

async def run_conversation(messages: List[Dict[str, str]], message_placeholder: Union[DeltaGenerator, None] = None) \
        -> Tuple[List[Dict[str, str]], str]:
    full_response = ""

    chunks = services.llm.converse(messages)
    chunk = await anext(chunks, "END OF CHAT")
    while chunk != "END OF CHAT":
        print(f"Received chunk from LLM service: {chunk}")
        if chunk.startswith("EXCEPTION"):
            full_response = ":red[We are having trouble generating advice.  Please wait a minute and try again.]"
            break
        full_response = full_response + chunk

        if message_placeholder is not None:
            message_placeholder.code(full_response + "▌")

        chunk = await anext(chunks, "END OF CHAT")

    if message_placeholder is not None:
        message_placeholder.code(full_response)

    messages.append({"role": "assistant", "content": full_response})
    return messages, full_response


# Chat with the LLM, and update the messages list with the response.
# Handles the chat UI and partial responses along the way.
async def chat(messages, prompt):
    with st.chat_message("user"):
        st.markdown(prompt)

    message_placeholder = st.empty()
    spinner_placeholder = st.empty()

    with st.chat_message("assistant"):
        # Step 1: Display spinner while processing the response
        with spinner_placeholder:
            with st.spinner("Receiving response..."):
                messages, response = await run_conversation(messages, message_placeholder)

        message_placeholder.empty()  # Clear the streamed chunks
        spinner_placeholder.empty()  # Clear the spinner

        # Display the final response
        st.write(response)

        st.session_state.messages = messages
    return messages

async def ask_book(messages, prompt):
    # Create an async function ask_book that takes a messages list and a prompt string as parameters
    # This function will:
    # 1. Use st.chat_message("user") to display the user's prompt in the chat UI using st.markdown(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Create an empty placeholder for the spinner using st.empty()
    spinner_placeholder = st.empty()
    
    # 3. Inside st.chat_message("assistant"):
    with st.chat_message("assistant"):
    #    a. Show a loading spinner with message "Asking the Pragmatic Programmer book..."
        with spinner_placeholder:
            with st.spinner("Asking the Pragmatic Programmer book..."):
    #    b. Call services.rag.ask_book(prompt, return_image=True) which returns a dictionary with:
    #       - answer: str - The AI-generated answer based on the book
    #       - context: str - The relevant text snippets from the book
    #       - page_number: int - The page number where the info was found
    #       - image_data: bytes - The binary image data of the book page (if available)
                rag_result = await services.rag.ask_book(prompt, return_image=True)

    #    c. Extract all returned values from rag_result using dictionary access:
    #       answer = rag_result["answer"]
    #       context = rag_result["context"]
    #       page_number = rag_result["page_number"]
    #       image_data = rag_result["image_data"]
                answer = rag_result["answer"]
                context = rag_result["context"]
                page_number = rag_result["page_number"]
                image_data = rag_result["image_data"]
    
    #    d. Clear the spinner placeholder using spinner_placeholder.empty()
        spinner_placeholder.empty()
    
    #    e. Display the answer using st.write(f"{answer}")
        st.write(f"{answer}")

    # 4. Display the response:
    #    a. Show the answer using st.write(f"{answer}")
    #    b. Handle the image data:
    #       - If image_data exists:
    #         * Import base64 module
    #         * Convert bytes to base64 using base64.b64encode(image_data).decode('utf-8')
    #         * Create HTML img tag: f'<img src="data:image/png;base64,{image_base64}" style="max-width: 100%;">'
    #       - If no image_data:
    #         * Set image_html to "No image available."
        if image_data:
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_html = f'<img src="data:image/png;base64,{image_base64}" style="max-width: 100%;">'
        else:
            image_html = "No image available."
    
    # 5. Create an evidence section using an f-string with:
    #    - A div for the page number in gray 10pt font
    #    - The image_html content
    #    Format:
    #    f"""
    #      <div style="color: gray; font-size: 10pt;">Page Number: {page_number}</div>
    #      {image_html}
    #    """
        evidence = f"""
          <div style="color: gray; font-size: 10pt;">Page Number: {page_number}</div>
          {image_html}
        """
        st.markdown(evidence, unsafe_allow_html=True)

    # 6. Update the chat history:
    #    a. Append the answer to messages with role "assistant"
    #    b. Append the evidence to messages with:
    #       - role: "evidence"
    #       - content: the evidence f-string
    #       - page_number: the page number
    #    c. Update st.session_state.messages with the new messages
        messages.append({"role": "assistant", "content": answer})
        messages.append({"role": "evidence", "content": evidence, "page_number": page_number})
        st.session_state.messages = messages

    # 7. Return the messages list for chat history
    return messages
