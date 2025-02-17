import streamlit as st
import base64
from huggingface_hub import notebook_login
from byaldi import RAGMultiModalModel
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from PIL import Image
from io import BytesIO
import torch
import re
import os

 
from dotenv import load_dotenv
load_dotenv()


from together import Together
client = Together()

upload_dir = "./doc"

# Set page layout to wide
st.set_page_config(layout="wide")

st.title("Multimodal Document RAG")

# Create sidebar for configuration options
with st.sidebar:
    st.header("Configuration Options")
    
    # Dropdown for selecting Colpali model
    colpali_model = st.selectbox(
        "Select Colpali Model",
        options=["vidore/colpali-v1.2"]
    )
    
    # Dropdown for selecting Multi-Model LLM
    multi_model_llm = st.selectbox(
        "Select Multi-Model LLM",
        options=["meta-llama/Llama-Vision-Free"]
    )
    
    # File upload button
    uploaded_file = st.file_uploader("Choose a Document", type=["pdf"])

# Main content layout
if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Uploaded Document")
        save_path = os.path.join(upload_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved: {uploaded_file.name}")
        @st.cache_resource
        def load_models(colpali_model):
            RAG = RAGMultiModalModel.from_pretrained(colpali_model, verbose=10)
            return RAG
        RAG= load_models(colpali_model)
        @st.cache_data
        def create_rag_index(image_path):
            RAG.index(
                input_path=image_path,
                index_name="image_index",
                store_collection_with_index=True,
                overwrite=True,
            )
        create_rag_index(save_path)
        
    with col2:
        # Text input for the user query
        text_query = st.text_input("Enter your text query")

        # Search and Extract Text button
        if st.button("Search and Extract Text"):
            if text_query:
                results = RAG.search(text_query, k=1, return_base64_results=True)

                image_data = base64.b64decode(results[0].base64)
                image = Image.open(BytesIO(image_data))
                st.image(image, caption="Result Image", use_column_width=True)

                response = client.chat.completions.create(
                        model=multi_model_llm,
                        messages=[
                        {
                            "role": "user",
                            "content": [
                            {"type": "text", "text": text_query},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{results[0].base64}"
                                }
                            },
                        ],
                        }
                    ],
                    max_tokens=300,
                )
                # print(response)
                output =response.choices[0].message.content
                st.subheader("Query with LLM Model")
                st.markdown(output,unsafe_allow_html=True)
                    # Placeholder for search results
                    # st.markdown(highlighted_output, unsafe_allow_html=True)
            else:
                st.warning("Please enter a query.")
else:
    st.info("Upload a document to get started.")