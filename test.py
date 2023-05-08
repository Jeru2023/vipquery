from embeddings.ingest import ingest
import embeddings.query as qa_chain
from utils.folder_updater import folder_updater

fu = folder_updater()
folder1_name = "火锅负面评价_1篇"
folder2_name = "Transformer解读-3篇"

folder1_id = fu.convert_uuid(folder1_name)
folder2_id = fu.convert_uuid(folder2_name)

persist_directory = f"./db/{folder1_id}"
source_directory = f"upload/{folder2_id}"

# check if db persisted
def test_ingest():
    db = ingest(source_directory, persist_directory)

def test_query(text):
    print(persist_directory)
    chain = qa_chain.get_chain(persist_directory)
    question = text
    response = qa_chain.query(chain, question)
    print(response)

#test_ingest()
#text = '用最简单的语言解释transformer是什么'
#test_query(text)'''

print(fu.query_uuid('火锅负面评价_1篇'))