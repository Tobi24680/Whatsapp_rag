import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

BASE_VECTOR_PATH = "data/vector_db"


def get_vector_path(user_id: str) -> str:
    return f"{BASE_VECTOR_PATH}/{user_id}"


# Embedding model (loaded once)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Prompt (langchain_core)
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)


def create_vector_db(text: str, user_id: str) -> None:
    path = get_vector_path(user_id)
    os.makedirs(path, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("No text chunks generated from document")

    db = FAISS.from_texts(chunks, embeddings)
    db.save_local(path)


def load_db(user_id: str) -> FAISS:
    path = get_vector_path(user_id)

    if not os.path.exists(path):
        raise FileNotFoundError("Vector DB not found for this user")

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_context(question: str, user_id: str, k: int = 3) -> str:
    db = load_db(user_id)
    docs = db.similarity_search(question, k=k)

    return "\n\n".join(doc.page_content for doc in docs)


def rag_answer(question: str, user_id: str) -> str:
    context = retrieve_context(question, user_id)

    if not context.strip():
        return "I don't know."

    response = llm.invoke(
        prompt.format(
            context=context,
            question=question
        )
    )

    return response.content.strip()
