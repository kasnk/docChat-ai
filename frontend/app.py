import streamlit as st
import requests
import time

st.set_page_config(page_title="DocuChat AI", layout="centered")
st.title("📄 DocuChat AI")

# Initialize session state
if "document_id" not in st.session_state:
    st.session_state.document_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔼 Upload Section (visible until PDF is uploaded)
if st.session_state.document_id is None:
    with st.expander("📎 Upload Your PDF First"):
        pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if pdf_file is not None:
            with st.spinner("Uploading and chunking..."):
                response = requests.post("http://localhost:8000/upload-pdf", files={"file": pdf_file})
                data = response.json()
                if "documentId" in data and "chunkCount" in data:
                    st.session_state.document_id = data["documentId"]
                    st.success(f"✅ PDF uploaded — {data['chunkCount']} chunks created")
                else:
                    st.error("❗ Upload failed")
else:
    st.info("✅ PDF already uploaded — ready to chat!")

# 💬 Query Box always visible and fixed at bottom
if st.session_state.document_id:
    st.markdown("---")
    st.markdown("### 💬 Ask Your Question")

    query = st.text_input("Type your query here", placeholder="e.g. What is the purpose of this document?")
    submit_button = st.button("Submit")

    if submit_button and query.strip():
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://localhost:8000/ask", json={
                    "documentId": st.session_state.document_id,
                    "queryText": query
                })
                raw = res.json()
                answer = raw.get("response", "")
                if isinstance(answer, dict):
                    answer = answer.get("response", "❗ Unexpected format")

                # Save to chat history: newest entry first
                st.session_state.chat_history.insert(0, {
                    "query": query,
                    "answer": answer
                })

            except Exception as e:
                st.error(f"❗ Failed to get response: {e}")

# 🧠 Display chat history (newest first, above query box)
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 🧾 Conversation")
    for item in st.session_state.chat_history:
        st.markdown(f"**🧑 You:** {item['query']}")
        placeholder = st.empty()
        typed = ""
        for char in item["answer"]:
            typed += char
            placeholder.markdown(f"**🤖 DocuChat AI:** {typed}")
            time.sleep(0.005)
        st.markdown("")