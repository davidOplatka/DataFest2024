from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import pinecone
import requests
from bs4 import BeautifulSoup
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer


os.environ["OPENAI_API_KEY"] = getpass.getpass()
os.environ["PINECONE_API_KEY"] = getpass.getpass()
os.environ["COHERE_API_KEY"] = getpass.getpass()

import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredFileLoader
# from langchain.document_loaders.image import UnstructuredImageLoader
from langchain.document_loaders import ImageCaptionLoader
from langchain.docstore.document import Document
# from langchain_experimental.text_splitter import SemanticChunker
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import WebBaseLoader
# from langchain_mistralai import MistralAIEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_cohere import CohereEmbeddings
# from langchain.callbacks.base import BaseCallbackHandler
import os
# import pytube
import openai


st.header("Ask questions related to Statistics textbook")

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4-turbo", streaming=True) #max_tokens=16000


if "processed_data" not in st.session_state:
    documents = []
    with open('collegeABCD.txt', 'r') as file:
        for url in file:
            url = url.strip()
            loader = WebBaseLoader(url)
            loaded_documents = loader.load()
            bs_transformer = BeautifulSoupTransformer()
            docs = bs_transformer.transform_documents(
                loaded_documents, tags_to_extract=["div"], unwanted_classnames=["mdc-drawer__content", "mdc-drawer-scrim", "banner-text", "nav-menu", "nav-menu--login", "mdc-touch-target-wrapper", "preview-content", "mdc-dialog student-data-preview", "footer-links-container"]
            )
            documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter() # chunk_size=1500, chunk_overlap=150
    document_chunks = text_splitter.split_documents(documents)
    
    
    # embeddings = MistralAIEmbeddings()
    embeddings = OpenAIEmbeddings()
    # embeddings = CohereEmbeddings()
    # embeddings = HuggingFaceEmbeddings() # model_name="Salesforce/SFR-Embedding-Mistral"
    # vectorstore = Chroma.from_documents(document_chunks, embeddings, persist_directory="./c_chroma_db_college")
    # vectorstore = Chroma(persist_directory="./c_chroma_db_college", embedding_function=embeddings)

    index_name = "langchain-new-index"

    vectorstore = PineconeVectorStore.from_documents(document_chunks, embeddings, index_name=index_name)


else:
    vectorstore = st.session_state.processed_data["vectorstore"]


st.session_state.processed_data = {
            "vectorstore": vectorstore,
        }

from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from langchain.chains import RetrievalQAWithSourcesChain


memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')

qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(search_kwargs={"k": 5}), chain_type="stuff", memory=memory, max_tokens_limit=4000, return_source_documents=True, get_chat_history=lambda h : h)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your questions?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = [
        f"{message['role']}: {message['content']}" 
        for message in st.session_state.messages
    ]

    result = qa({
        "question": prompt, 
        "chat_history": history
    })

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = result["answer"]
        message_placeholder.markdown(f"{full_response}|")
    message_placeholder.markdown(full_response)
    print(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
