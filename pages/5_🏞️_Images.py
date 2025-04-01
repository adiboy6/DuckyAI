import streamlit as st
import helpers.sidebar
import asyncio
import pandas as pd
from services.images import generate_image, get_all_images, delete_image  # Ensure these functions are implemented in images.py

st.set_page_config(
    page_title="Images",
    page_icon="🏞️",
    layout="wide"
)

helpers.sidebar.show()

st.header("Image Generation")

# This page should have 2 tabs, the first being named 'Image Generation' and the second 'Image List'.
tab1, tab2 = st.tabs(["Image Generation", "Image List"])

# Tab 1: Image Generation
with tab1:
    prompt = st.text_input("Prompt", placeholder="Enter a prompt for the image generation model")
    if st.button("Generate Image"):
        if prompt.strip():
            with st.spinner("Generating image..."):
                try:
                    image_path = asyncio.run(generate_image(prompt))
                    if image_path:
                        st.image(image_path[1], caption="Generated Image", use_column_width=True)
                except Exception as e:
                    st.error(f"Error generating image: {e}")
        else:
            st.warning("Please enter a prompt before generating an image.")

# Tab 2: Image List
with tab2:
    try:
        images_df = get_all_images()  # Fetch images as a Pandas DataFrame
        if not images_df.empty:
            for index, row in images_df.iterrows():
                col1, col2, col3, col4 = st.columns([2, 4, 2, 2])
                with col1:
                    st.image(row["Image"], width=100)  # Display image thumbnail
                with col2:
                    st.write(row["Description"])  # Display description
                with col3:
                    st.write(row["Date Created"].strftime("%Y-%m-%d %H:%M:%S"))  # Format date
                with col4:
                    if st.button("View", key=f"view_{index}"):
                        # Display image in a modal
                        st.image(row["Image"], caption=row["Description"], use_column_width=True)
                    if st.button("Delete", key=f"delete_{index}"):
                        # Delete image and refresh the list
                        delete_image(row["Image"])  # Ensure this function deletes the file and updates the data source
                        st.success("Image deleted successfully.")
                        st.experimental_rerun()  # Refresh the page to update the list
        else:
            st.info("No images found.")  # Display message if no images are available
    except Exception as e:
        st.error(f"Error loading images: {e}")  # Handle errors gracefully
