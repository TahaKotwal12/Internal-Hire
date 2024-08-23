# Internal Hire AI

[![TiDB](https://img.shields.io/badge/Database-TiDB-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.pingcap.com/tidb/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)

## Overview

Expertise Locator is an AI vector-search based web application built with Streamlit. It enables organizations to efficiently search for colleagues with specific expertise based on their resumes, facilitating knowledge sharing and mentoring opportunities.

## 🚀 Features

- 📊 **Dashboard**: View HR metrics and charts
- 📤 **Upload Resume**: Process and store new resumes
- 🔍 **Search Expertise**: Find employees based on skills or experience and chat with the retrieved results


## 🛠 Tech Stack
- TiDB Vector Database
- Python 3.11+
- Streamlit
- LangChain
- Google AI (for embeddings and language models)
- PyPDF2 (PDF parsing)
- Plotly (for data visualization)
- PyMySQL (Database connection)
- Docker

## 📋 Prerequisites
- Python
- Docker
- Google AI API key
- Access to a TiDB vector database

## 📌 TiDB Table Schema
For detailed table schema refer the `./Database/scripts.sql` file.

## 🔧 Installation

### 🐳 Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/TahaKotwal12/Internal-Hire.git
cd Internal-Hire
```
2. Download isrgrootx1.pem file from the link and add it to the root directory

    [[isrgrootx1.pem]](https://letsencrypt.org/certs/isrgrootx1.pem)

3. Docker image:
- Option 1: Build Docker Image
```bash
docker build -t internalhire:latest .
```
- Option 2: Pull the Existiong Docker Image
```
docker pull tahakotwal/internal-hire:0.0.4
```
4. Run the Docker container:
```bash
docker run -p 8501:8501 -e GOOGLE_API_KEY="your_google_api_key" -e HOST="your_tidb_host" -e PORT=your_tidb_port -e USER="your_tidb_user" -e PASSWORD="your_tidb_password" -e DATABASE="your_tidb_database" -e SSL_CA="./isrgrootx1.pem" --name internal_hire internalhire:latest
```

Replace the placeholders with your actual credentials:
- `your_google_api_key`: Your Google Gemini API key
- `your_tidb_host`: Your TiDB cluster host
- `your_tidb_port`: Your TiDB cluster port
- `your_tidb_user`: Your TiDB username
- `your_tidb_password`: Your TiDB password
- `your_tidb_database`: Your TiDB database name

You can obtain these credentials as follows:

[![TiDB Credentials](https://img.shields.io/badge/TiDB-Get%20Credentials-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://docs-archive.pingcap.com/tidb/v7.6/dev-guide-sample-application-python-pymysql)

[![Google AI API](https://img.shields.io/badge/Google%20AI-Get%20API%20Key-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/app/apikey)

Make sure to keep your credentials secure and never share them publicly.

5. Open a web browser and navigate to `http://localhost:8501` to access the application.

### 💻 Development Installation

1. Clone the repository:
```bash
git clone https://github.com/TahaKotwal12/Internal-Hire.git
cd Internal-Hire
```
2. Create a virtual environment:
```bash
python -m venv venv
```
3. Activate the virtual environment:
- On Windows:
```bash
  venv\Scripts\activate
```
- On macOS and Linux:
```bash
  source venv/bin/activate
```
4. Install the required dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file in the project root and add your credentials refer the ```.env.example``` file

6. Ensure you have the `isrgrootx1.pem` file in your project root directory. Else download from the below link:

    [[isrgrootx1.pem]](https://letsencrypt.org/certs/isrgrootx1.pem)

7. Run the Streamlit app:
```bash
streamlit run app.py
```
8. Open a web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

Remember to replace the placeholder values in the `.env` file with your actual credentials. You can obtain these credentials as follows:

[![TiDB Credentials](https://img.shields.io/badge/TiDB-Get%20Credentials-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://docs-archive.pingcap.com/tidb/v7.6/dev-guide-sample-application-python-pymysql)

[![Google AI API](https://img.shields.io/badge/Google%20AI-Get%20API%20Key-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/app/apikey)


Make sure to keep your credentials secure and never share them publicly.

## 🖥 Usage
- Upload and process PDF resumes
- Extract text content from resumes
- Generate embeddings for resume content using AI models
- Store resume data and embeddings in a TiDB vector database
- Search for expertise using natural language queries
- Display matching employees based on vector similarity
- Interactive dashboard for HR metrics
- Chatbot interface for HR queries
## 🌐 Live Demo

Experience the Internal Hire AI in action:

[![Internal Hire](https://img.shields.io/badge/Internal%20Hire-Live%20Demo-blue?style=for-the-badge)](https://internal-hire-y2c6jfb2ma-el.a.run.app/)

Click the badge above to access the live webapp and explore its features firsthand.
## 🛠 Customization
- To modify the UI or add new features, edit the relevant files in the `views/` directory.
- To change the embedding method or similarity calculation, update the functions in `utils/util_functions.py`.
- To modify database operations, update the methods in `Database/Db.py`.



