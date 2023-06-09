from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
import os
import toml
import sys

sys.path.append("..")
from templates.system_prompt import SYSTEM_PROMPT_CN

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def query(question, persist_directory, **chain_kwargs):
    chain = get_chain(persist_directory, **chain_kwargs)
    response = chain({"question": question})
    return response['answer']


def get_chain(persist_directory, **chain_kwargs):
    db = FAISS.load_local(persist_directory, _get_embeddings())

    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0,
                       openai_api_key=get_openai_api_key(), streaming=True)
    chain_type_kwargs = {
        "prompt": get_system_prompt()
    }
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm = model,
        chain_type = "stuff",
        retriever=db.as_retriever(), #search_kwargs={"k": 5}
        chain_type_kwargs = chain_type_kwargs,
        reduce_k_below_max_tokens=True,
        verbose = chain_kwargs['verbose'],
    )
    return chain



def get_system_prompt():
    messages = [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_CN),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt


def _get_embeddings():
    model_name = "shibing624/text2vec-base-chinese"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    return embeddings


def get_openai_api_key():
    with open(".streamlit/secrets.toml", "r") as secrets_file:
        secrets = toml.load(secrets_file)
    return secrets["OPENAI_KEY"]
