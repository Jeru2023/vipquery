from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
import sys

sys.path.append("..")
from utils.folder_updater import folder_updater


def ingest(dataset_name: str) -> FAISS:
    """
    Ingests text documents from a source directory, processes them,
    and saves them to a persist directory.

    Args:
        source_directory (str): The directory containing the text documents to ingest.
        persist_directory (str): The directory to save the processed documents to.

    Returns:
        FAISS: A FAISS index containing document embeddings.
    """
    fu = folder_updater()
    folder_id = fu.query_uuid(dataset_name)
    persist_directory = f"./db/{folder_id}"
    source_directory = f"upload/{folder_id}"

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

    model_name = "shibing624/text2vec-base-chinese"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings


'''
if __name__ == '__main__':
    ingest('火锅负面评价_1篇')
'''