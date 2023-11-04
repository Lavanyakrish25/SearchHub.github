
from PyPDF2 import PdfReader
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from const import openai_key

os.environ["OPENAI_API_KEY"] = openai_key

def process_pdf(pdf_path):
    pdf = PdfReader(pdf_path)

    # Read text from the PDF
    raw_text = ''
    for i, page in enumerate(pdf.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    embeddings = OpenAIEmbeddings()

    document_search = FAISS.from_texts(texts, embeddings)
    return document_search

def query_agent(document_search, query):
    from langchain.chains.question_answering import load_qa_chain
    from langchain.llms import OpenAI

    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    docs = document_search.similarity_search(query)
    ans = chain.run(input_documents=docs, question=query)
    return ans
