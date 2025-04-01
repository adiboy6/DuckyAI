import os
from datetime import datetime
from typing import Literal, Tuple
from urllib.parse import urlparse

import httpx
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
# Load .env file
load_dotenv()

__IMAGES_BASE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/images')


def get_all_images() -> pd.DataFrame:
    """
    Retrieves a DataFrame containing information about all images stored in a folder.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Image', 'Description', and 'Date Created',
                      where 'Image' is the file path, 'Description' is the associated
                      description, and 'Date Created' is the creation timestamp.
    """
    # AI Generation Prompt:
    # Write a Python function that reads all `.png` image files from a given folder, retrieves
    # their associated descriptions from a `.txt` file with the same name, and returns a pandas
    # DataFrame containing the image file paths, descriptions, and creation timestamps.

    images_data = []
    for file in os.listdir(__IMAGES_BASE_FOLDER):
        if file.endswith('.png'):
            image_path = os.path.join(__IMAGES_BASE_FOLDER, file)
            description_path = os.path.splitext(image_path)[0] + '.txt'
            description = ''
            if os.path.exists(description_path):
                with open(description_path, 'r') as desc_file:
                    description = desc_file.read()
            creation_time = datetime.fromtimestamp(os.path.getctime(image_path))
            images_data.append({
                'Image': image_path,
                'Description': description,
                'Date Created': creation_time
            })
    return pd.DataFrame(images_data)


def delete_image(image_path: str):
    """
    Deletes an image file and its associated description file (if it exists).

    Args:
        image_path (str): The path to the image file to be deleted.
    """
    # AI Generation Prompt:
    # Write a Python function that deletes a given image file and its corresponding `.txt`
    # description file, if the description file exists.
    if os.path.exists(image_path):
        os.remove(image_path)
    description_path = os.path.splitext(image_path)[0] + '.txt'
    if os.path.exists(description_path):
        os.remove(description_path)

async def generate_image(
    prompt: str,
    model: str = "dall-e-3",
    style: Literal["vivid", "natural"] = "vivid",
    quality: Literal["standard", "hd"] = "hd",
    timeout: int = 100,
    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = "1024x1024"
) -> Tuple[str, str]:
    """
    Generates an image based on a given text prompt using the OpenAI client
    and saves the image to a local folder.

    Args:
        prompt (str): The description or prompt for generating the image.
        model (str): The model version to use (default is "dall-e-3").
        style (Literal): The style of the image, e.g., "vivid" or "natural".
        quality (Literal): The quality setting, either "standard" or "hd".
        timeout (int): The maximum time (in seconds) to wait for the image to be generated.
        size (Literal): The size of the image, e.g., "1024x1024", "1792x1024", etc.

    Returns:
        Tuple[str, str]: A tuple containing the prompt and the file path of the saved image.
    """
    # Create an OpenAI client
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv('OPENAI_API_BASE_URL'))

    # Generate the image using the OpenAI client
    try:
        response = client.images.generate(
            prompt=prompt,
            model=model,
            style=style,
            quality=quality,
            size=size
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate image: {e}")

    # Extract the image URL from the response
    image_url = response.data[0].url
    if not image_url:
        raise ValueError("No image URL returned by the API")

    # Download the image
    async with httpx.AsyncClient() as client:
        image_response = await client.get(image_url, timeout=timeout)
        if image_response.status_code != 200:
            raise RuntimeError(f"Failed to download image: {image_response.status_code}")

    # Save the image locally
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    image_path = os.path.join(__IMAGES_BASE_FOLDER, filename)
    os.makedirs(__IMAGES_BASE_FOLDER, exist_ok=True)
    with open(image_path, "wb") as image_file:
        image_file.write(image_response.content)

    # Save the prompt in a .txt file alongside the image
    description_path = os.path.splitext(image_path)[0] + ".txt"
    with open(description_path, "w") as desc_file:
        desc_file.write(prompt)

    return prompt, image_path



def _extract_filename_from_url(url: str) -> str:
    """
    Extracts the filename from a given URL.

    Args:
        url (str): The URL from which to extract the filename.

    Returns:
        str: The extracted filename.
    """
    # AI Generation Prompt:
    # Write a Python function that takes a URL as input, extracts the file path, and returns
    # the filename from the URL.
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path) if parsed_url.path else ''