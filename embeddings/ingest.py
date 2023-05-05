from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings

def _get_embeddings():
    model = "shibing624/text2vec-base-chinese"
    embeddings = HuggingFaceEmbeddings(model_name = model)
    return embeddings

def ingest(source_directory, persist_directory):
    loader = DirectoryLoader(source_directory, glob='**/*.txt')
    documents = loader.load()    
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0
    )
    documents = text_splitter.split_documents(documents)
    embeddings = _get_embeddings()
