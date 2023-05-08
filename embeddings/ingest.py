from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def ingest(source_directory: str, persist_directory: str) -> FAISS:
    """
    Ingests text documents from a source directory, processes them,
    and saves them to a persist directory.

    Args:
        source_directory (str): The directory containing the text documents to ingest.
        persist_directory (str): The directory to save the processed documents to.

    Returns:
        FAISS: A FAISS index containing document embeddings.
    """
    # Load text documents from source directory
    loader = DirectoryLoader(source_directory, glob='**/*.txt')
    documents = loader.load()
    print(documents)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0
    )
    docs = text_splitter.split_documents(documents)
    print(docs)

    # Get document embeddings and store them in a FAISS index
    embeddings = _get_embeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(persist_directory)
    return db

def _get_embeddings():
    model = "shibing624/text2vec-base-chinese"
    embeddings = HuggingFaceEmbeddings(model_name = model)
    return embeddings