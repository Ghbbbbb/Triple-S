import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def load_docs(prompt_doc):
    """
    Load documents from a text file and split them into chunks of 1000 characters.
    """
    loader = TextLoader(os.path.join(os.path.dirname(__file__), "../prompts/{}/task_settings.txt".format(prompt_doc)),encoding="utf-8")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(separator="---", chunk_size=500, chunk_overlap=20)
    docs = text_splitter.split_documents(documents)
    return docs


def init_embedding_model(model_name = 'flax-sentence-embeddings/all_datasets_v4_MiniLM-L6'):
    """
    Initialize embeddings
    """
    embeddings = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs={"device": "cuda"},
                )
    return embeddings

def init_vector_store(embedding_model, prompt_doc, is_already_indexed=True):
    """
    Initialize vector store
    """
    vector_store = init_chroma_vector_store(embedding_model, prompt_doc, is_already_indexed)
    return vector_store

def init_chroma_vector_store(embedding_model, prompt_doc, is_already_indexed=True):
    """
    Initialize chroma vector store
    """
    docs = load_docs(prompt_doc)

    vector_store = Chroma.from_documents(docs, embedding_model)

    return vector_store
