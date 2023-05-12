from embeddings.ingest import ingest
import embeddings.query as qa_chain

persist_directory = "db"
source_directory = "docs"

# check if db persisted
def test_ingest():
    db = ingest(source_directory, persist_directory)

def test_query():
    chain = qa_chain.get_chain(persist_directory)
    question = "总结一下用户的负面评论"
    response = qa_chain.query(chain, question)
    print(response)

test_query()
#test_ingest()