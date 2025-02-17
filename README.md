# Multimodal-RAG-Application

This repository provides a Multimodal Retrieval-Augmented Generation (RAG) application that leverages the **LLAMA Vision Model** via **Together AI** as a generator model and **ColPali** model as a retrieval model.

## Installation

Follow these steps to set up the environment:

### 1. Install dependencies
Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Create a directory for document storage
Make a `doc` directory in the current working directory to store uploaded documents:

```bash
mkdir doc
```

### 3. Install Poppler utilities
Poppler utilities are required for PDF processing. Install them using:

```bash
apt-get install poppler-utils
```

## API Key Setup

We use **Together AI** to access the **LLAMA Vision Model** (which is free to use). Register at [Together AI](https://www.together.ai/) to get an API key.

Once registered, export your API key as an environment variable:

```bash
export TOGETHER_API_KEY=your_api_key_here
```

## Usage

After completing the setup, you can run the application.
```bash
streamlit run app.py
```

---

Happy coding! 🚀
