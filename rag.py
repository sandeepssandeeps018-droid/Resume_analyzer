from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import API_KEY  
import google.generativeai as genai 
genai.configure(api_key=API_KEY)

# FIXED: Utilizing stable gemini-embedding-001 mapping structures 
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=API_KEY
)

model = genai.GenerativeModel("gemini-2.5-flash")

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def create_vector_store(text):
    chunks = chunk_text(text)
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def retrieve_chunks(vector_store, question):
    docs = vector_store.similarity_search(question, k=3)
    return docs

def rag_answer(vector_store, question):
    docs = vector_store.similarity_search(question, k=3)
    context = "".join([doc.page_content + "\n" for doc in docs])

    prompt = f"Answer ONLY using the provided context.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    response = model.generate_content(prompt)
    return response.text