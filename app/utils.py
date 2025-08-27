## with FASSI Vector Db

import pandas as pd
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
# FAISS vector store (in-memory store, but can also be persisted)
#from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_core.language_models.llms import LLM
#from langchain.vectorstores import FAISS  # Using FAISS instead of Chroma
from langchain_community.vectorstores import FAISS

from typing import Optional, List
import groq
import numpy as np
import os

os.environ["TRANSFORMERS_NO_TF"] = "1"


# -----------------------------
#  1. Load KB and Setup RAG
# -----------------------------
# KB_DIR = "D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS R&D/Cheese_Craft_EMS-COPY/kb"
# loader = DirectoryLoader(KB_DIR, glob="**/*.md")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DIR = os.path.join(BASE_DIR, "kb")
loader = DirectoryLoader(KB_DIR, glob="**/*.md")


documents = loader.load()
print("type documents : ", type(documents))

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
print("docs : ", type(docs))

for d in docs:
    print("d ==>", type(d))
    print("d content ==>", d)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# -----------------------------
#  Use FAISS as the Vector Store
# -----------------------------


# Create FAISS index from the documents and embeddings
faiss_index = FAISS.from_documents(docs, embedding_model)

# Now you have your FAISS index created for the documents and embeddings
retriever = faiss_index.as_retriever()

# -------------------------------
#  2. Custom Groq LLM Wrapper
# -------------------------------
class GroqLLM(LLM):
    model: str = "llama3-8b-8192"
    temperature: float = 0.0
    max_tokens: int = 1024
    groq_api_key: str = "****"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        client = groq.Client(api_key=self.groq_api_key)
        response = client.chat.completions.create(
            model=self.model,
            temperature=0.0,
            messages=[
                {"role": "system", "content": "You are a strategist at CheeseCraft."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    @property
    def _identifying_params(self):
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "groq"

# from typing import Optional, List
# from langchain_core.language_models import LLM
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ## For LLAMA llm
# class llama(LLM):
#     def __init__(self, model_name: str = "meta-llama/Llama-3-8b-8192", temperature: float = 0.7, max_tokens: int = 1024):
#         """
#         Initialize the LLaMA 3-8B model for text generation using Hugging Face.
        
#         :param model_name: The model name or path (e.g., "meta-llama/Llama-3-8b-8192")
#         :param temperature: Controls the randomness of the output (0.0 to 1.0)
#         :param max_tokens: Maximum number of tokens for the model's output
#         """
#         self.model_name = model_name
#         self.temperature = temperature
#         self.max_tokens = max_tokens
        
#         # Load the model and tokenizer from Hugging Face
#         self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
#         # Create a text generation pipeline
#         self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

#     def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
#         """
#         Generate a response using the LLaMA model.

#         :param prompt: The input prompt for the model to generate a response.
#         :param stop: Optional stop tokens for the generation.
#         :return: The generated response from the model.
#         """
#         # Generate the output using the pipeline
#         response = self.generator(prompt, max_length=self.max_tokens, temperature=self.temperature, num_return_sequences=1)
#         return response[0]['generated_text']

#     @property
#     def _identifying_params(self):
#         """
#         Returns the parameters that uniquely identify this LLM model.
#         """
#         return {"model": self.model_name, "temperature": self.temperature, "max_tokens": self.max_tokens}

#     @property
#     def _llm_type(self) -> str:
#         """
#         Returns the type of LLM.
#         """
#         return "llama"



# ----------------------------------
#  3. Retrieval QA Chain (for KB)
# ----------------------------------
groq_llm = GroqLLM()
qa_chain = RetrievalQAWithSourcesChain.from_llm(llm=groq_llm, retriever=retriever)

# ----------------------------
#  4. Historical Data Helper
# ----------------------------
def get_history_string(product, week):
    df = pd.read_csv("D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS_WITH_ARIMA/training/recent_sales_data.csv")
    df = df[(df["product"] == product) & (df["week"] < week)]
    return "\n".join(f"Week {row['week']}: {row['sales']}" for _, row in df.iterrows())

# --------------------------------------
#  5. RAG KB Retrieval for LLM Context
# --------------------------------------
def get_kb_context(query, return_docs=False):
    result = qa_chain({"question": query})
    return (result["answer"], result["sources"]) if return_docs else result["answer"]

# ---------------------------------------------
#  6. Dynamic Threshold via Statistical Logic
# ---------------------------------------------
def compute_dynamic_threshold(product: str, week: int):
    df = pd.read_csv("D:/OneDrive - ANANTARA SOLUTIONS PRIVATE LIMITED/Desktop/EMS R&D/Cheese_Craft_EMS - Copy/data/historical_sales_enriched_final_ready.csv")
    df = df[(df["product"] == product) & (df["week"] < week)]

    if len(df) < 3:
        raise ValueError("Too few historical points for threshold calculation")

    df["forecast"] = df["sales"].shift(1)
    df.dropna(inplace=True)
    df["error_pct"] = ((df["sales"] - df["forecast"]) / df["forecast"]) * 100

    mean_error = df["error_pct"].mean()
    std_error = df["error_pct"].std()

    if np.isnan(mean_error) or np.isnan(std_error):
        raise ValueError("Error stats could not be computed")

    threshold = abs(mean_error) + std_error
    return round(threshold, 2)

# -------------------------------------
#  7. Get Deviation Threshold via LLM
# -------------------------------------
def get_llm_suggested_threshold(product):
    kb_text = get_kb_context(f"{product} strategy")
    prompt = f"""
Based on the following product strategy, suggest a reasonable numeric sales deviation threshold (%) for forecast error detection.
Only respond with a number.

Strategy:
{kb_text}
"""
    value = query_groq(prompt)
    for token in value.split():
        if token.replace('.', '', 1).isdigit():
            return float(token)
    raise ValueError("LLM could not extract threshold number.")

# ---------------------------------------------------
#  8. Hybrid Method for Reliable Smart Thresholding
# ---------------------------------------------------
def smart_threshold(product, week):
    try:
        threshold = compute_dynamic_threshold(product, week)
        if threshold < 3 or threshold > 30:
            raise ValueError("Statistical value out of range")
    except:
        try:
            threshold = get_llm_suggested_threshold(product)
        except:
            threshold = 10.0  # fallback default

    return threshold

# ---------------------------------
#  9. Simple Groq Prompt Runner
# ---------------------------------
def query_groq(prompt):
    client = groq.Client(api_key="*****")
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a strategist at CheeseCraft."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
