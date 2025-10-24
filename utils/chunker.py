from semchunk import chunkerify

def chunk_document(text: str, chunk_size: int = 2000) -> list[str]:
    """
    Chunk document using semantic chunking.
    Returns list of text chunks that preserve meaning.
    """
    chunker = chunkerify(lambda x: len(x), chunk_size)
    chunks = chunker(text)
    return chunks
    