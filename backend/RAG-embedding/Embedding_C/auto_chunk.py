import os
import re
import math

def auto_chunk_text(file_path, min_chunk_size=500, max_chunk_size=1500, overlap_ratio=0.2):
    """
    Automatically split a text file into optimal chunks based on file length.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    text_length = len(text)

    if text_length <= min_chunk_size:
        return [text]
    elif text_length <= 2 * max_chunk_size:
        chunk_size = text_length // 2
    elif text_length <= 3 * max_chunk_size:
        chunk_size = text_length // 3
    else:
        chunk_size = max_chunk_size

    overlap = int(chunk_size * overlap_ratio)

    # Split by sentence endings
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            if overlap > 0:
                current_chunk = current_chunk[-overlap:] + sentence + " "
            else:
                current_chunk = sentence + " "
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
