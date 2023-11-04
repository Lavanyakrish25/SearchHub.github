import streamlit as st
from agent import process_pdf, query_agent

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def app():
    st.title("Query Page")
    st.write("This is the Query page.")

    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    document_search = None

    if pdf_file:
        st.write("File uploaded successfully!")
        # Process the PDF and obtain the document_search
        document_search = process_pdf(pdf_file)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("What is up?") if document_search else ""

    if query:
        st.chat_message("user").markdown(query)
        st.session_state.messages.append({"role": "user", "content": query})

        ans = query_agent(document_search, query)

        with st.chat_message("assistant"):
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

if __name__ == '__main__':
    app()
