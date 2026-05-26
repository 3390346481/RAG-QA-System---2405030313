from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_documents(chunks: list, source: str = "") -> list:
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={"source": source, "chunk_index": i}
        )
        documents.append(doc)
    return documents

def process_document(text: str, source: str = "") -> list:
    chunks = split_text(text)
    documents = create_documents(chunks, source)
    return documents

def process_documents(documents: list) -> list:
    all_docs = []
    for name, text in documents:
        docs = process_document(text, name)
        all_docs.extend(docs)
    return all_docs

if __name__ == "__main__":
    sample_text = "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language. It focuses on how to program computers to process and analyze large amounts of natural language data. Challenges in natural language processing frequently involve speech recognition, natural language understanding, and natural language generation."
    chunks = split_text(sample_text, chunk_size=50, chunk_overlap=10)
    print(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")
