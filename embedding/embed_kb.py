from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Load markdown files
loader = DirectoryLoader("kb", glob="**/*.md")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Use sentence-transformers for embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vectorstore and persist
vectorstore = Chroma.from_documents(docs, embedding_model, persist_directory="embedding/chroma_store")
vectorstore.persist()

print("✅ Knowledge base embedded successfully using LangChain!")
