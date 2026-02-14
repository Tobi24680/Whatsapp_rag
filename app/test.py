from rag_engine import create_vector_db, search

text = """
LangChain is a framework for building applications with large language models.
It supports retrieval augmented generation, agents, tools, and memory.
FAISS is a fast vector database for similarity search.
"""

# Create vector DB (run once)
create_vector_db(text)

# Search
result = search("What is LangChain?")
print(result)
