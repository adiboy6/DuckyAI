import csv
import os
from typing import List, Tuple
import tiktoken as tkn
from PyPDF2 import PdfReader
from openai import OpenAI
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
import numpy as np
import services.llm
from pdf2image import convert_from_path
from PIL import Image
import io

# Global configuration
EMBEDDING_MODEL = "text-embedding-3-small"  # OpenAI's best embeddings as of Feb 2024
CSV_FILE_PATH = "data/ThePragmaticProgrammer.embeddings.csv"

async def ask_book(query: str, return_image: bool = False):
    """
    Main RAG (Retrieval Augmented Generation) implementation.
    Takes a query about the book and returns relevant information with optional page image.
    
    Returns:
    {
        "answer": str,           # Generated response using context
        "page_number": int,      # Page where context was found
        "context": str,          # Text chunk used for answer
        "image_data": bytes      # Optional PNG of page if return_image=True
    }
    """
    # Keep the OpenAI client configuration
    client = OpenAI(
        base_url=os.getenv("OPENAI_API_BASE_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Source PDF path
    pdf_path = "data/ThePragmaticProgrammer.pdf"

    # Implement embedding management
    # 1. Check if embeddings exist in CSV_FILE_PATH
    if os.path.exists(CSV_FILE_PATH):
        embeddings = load_embeddings_from_csv(CSV_FILE_PATH)
        documents = [emb["context"] for emb in embeddings]

    # 2. If not:
    #    - Extract text from PDF using __extract_text_from_pdf()
    #    - Chunk the text (see chunking strategy note below)
    #    - Calculate embeddings using OpenAI API
    #    - Save to CSV for future use
    else:
        pages_text = __extract_text_from_pdf(pdf_path)
        chunks = await __chunk_prompt(pages_text)
        documents = [chunk[1] for chunk in chunks]
        embeddings = await __calculate_embeddings(client, documents)
        save_embeddings_to_csv(CSV_FILE_PATH, "ThePragmaticProgrammer", [chunk[0] for chunk in chunks], embeddings, documents)
    # 3. Load embeddings from CSV
    print("Loaded embeddings from CSV")
    print(embeddings)

    # Implement semantic search 
    # 1. Set up nearest neighbors search with sklearn
    embedding_vectors = np.array([emb["embedding"] for emb in embeddings])
    normalized_embeddings = normalize(embedding_vectors)
    nearest_neighbors = NearestNeighbors(algorithm='ball_tree').fit(normalized_embeddings)
    # nearest_neighbors.fit(normalized_embeddings)
    # Print the distance and index of the k nearest neighbor

    # 2. Get embedding for user's query (with caching)
    # Simple cache to avoid repeated embedding calls for the same query
    query_cache_key = f"query_embedding_{hash(query)}"
    if hasattr(ask_book, 'query_cache') and query_cache_key in ask_book.query_cache:
        query_embedding = ask_book.query_cache[query_cache_key]
        print("📦 Using cached query embedding")
    else:
        query_embedding = await __calculate_embeddings(client, [query])
        if not hasattr(ask_book, 'query_cache'):
            ask_book.query_cache = {}
        ask_book.query_cache[query_cache_key] = query_embedding
        print("📦 Cached new query embedding")
    
    normalized_query_embedding = normalize(query_embedding)

    # 3. Find most relevant context using cosine similarity
    dist, ind = nearest_neighbors.kneighbors(normalized_query_embedding, n_neighbors=1)
    print("Distance: ", dist)

    most_relevant_index = ind[0][0]
    most_relevant_context = embeddings[most_relevant_index]["context"]
    most_relevant_page = embeddings[most_relevant_index]["page_number"]

    # Implement answer generation 
    # 1. Format prompt with context and query
    prompt = f"""Answer the following question using the provided context:
    Question: {query}
    Context: {most_relevant_context}
    """
    # 2. Get response from LLM (use services.llm module for this)
    response, _ = services.llm.converse_sync(prompt, [], model=os.getenv("OPENAI_API_MODEL"))

    # 3. Package results with page number and context
    result = {
        "answer": response,
        "page_number": most_relevant_page,
        "context": most_relevant_context
    }

    # Optional - Handle page image extraction 
    # 1. Convert PDF page to image
    if return_image:
        result["image_data"] = __extract_page_as_image(pdf_path, most_relevant_page)
    
    # 2. Return as PNG bytes
    return result

def __extract_text_from_pdf(pdf_path: str) -> List[Tuple[int, str]]:
    """
    Extract text content from each page of the PDF.
    Returns: List of (page_number, page_text) tuples
    """
    text_from_pdf = []
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text_from_pdf.append((page_number, page.extract_text()))
    return text_from_pdf

def __extract_page_as_image(pdf_path: str, page_number: int) -> bytes:
    """
    Convert a specific PDF page to a PNG image.
    Returns: Raw PNG image data as bytes
    """
    page_as_image = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)[0]
    image_bytes = io.BytesIO()
    page_as_image.save(image_bytes, format='PNG')
    return image_bytes.getvalue()

async def __chunk_prompt(pages_text: List[Tuple[int, str]], chunk_size: int = 1500, overlap: int = 50) -> List[Tuple[int, str]]:
    """
    Split text into chunks suitable for embedding.
    
    Note: For a good chunking implementation example, see:
    http://aitools.cs.vt.edu:8888/edit/module5/util.py
    
    Hint: Consider using one chunk per page as a starting strategy.
    This makes it easier to track context and display relevant pages.
    
    Args:
        pages_text: List of (page_number, text) tuples
        chunk_size: Target size for each chunk in tokens
        overlap: Number of tokens to overlap between chunks
    
    Returns: List of (page_number, chunk_text) tuples
    """
    encoding = tkn.encoding_for_model("gpt-3.5-turbo")
    chunks = []
    for page_number, text in pages_text:
        tokens = encoding.encode(text)
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk = tokens[i:i + chunk_size]
            chunks.append((page_number, encoding.decode(chunk)))
    return chunks

async def __calculate_embeddings(client: OpenAI, documents: List[str], batch_size: int = 20) -> List[List[float]]:
    """
    Get embeddings for text chunks using OpenAI's API.
    
    Hint: http://aitools.cs.vt.edu:8888/notebooks/module5/embeddings-tutorial.ipynb shows how to calculate embeddings.

    Args:
        client: OpenAI client instance
        documents: List of text chunks to embed
        batch_size: Number of chunks to process at once
    
    Returns: List of embedding vectors (each vector is List[float])
    """
    embeddings = []
    for i in range(0, len(documents), batch_size):
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=documents[i : i + batch_size], encoding_format="float")
        for i, be in enumerate(response.data):
            assert i == be.index  # double check embeddings are in same order as input
        batch_embeddings = [e.embedding for e in response.data]
        embeddings.extend(batch_embeddings)
    return embeddings

def save_embeddings_to_csv(file_path: str, document_name: str, page_numbers: List[int], embeddings: List[List[float]], contexts: List[str]):
    """
    Cache embeddings to CSV for faster future lookups.
    
    CSV Format:
    document_name, page_number, embedding, context
    
    Args:
        file_path: Where to save the CSV
        document_name: Identifier for the source document
        page_numbers: List of page numbers for each chunk
        embeddings: List of embedding vectors
        contexts: List of text chunks
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["document_name", "page_number", "embedding", "context"])
        for page_number, embedding, context in zip(page_numbers, embeddings, contexts):
            writer.writerow([document_name, page_number, embedding, context])

def load_embeddings_from_csv(file_path: str) -> List[dict]:
    """
    Load previously cached embeddings from CSV.
    
    Returns: List of dicts with keys:
        - document_name: str
        - page_number: int  
        - embedding: List[float]
        - context: str
    """
    embeddings = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            embeddings.append({
                "document_name": row["document_name"],
                "page_number": int(row["page_number"]),
                "embedding": eval(row["embedding"]),
                "context": row["context"]
            })
    return embeddings
