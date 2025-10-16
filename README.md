# 🎓 CodeMentor - AI-Powered Programming Tutor with RAG

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> An intelligent programming tutor that uses **Retrieval-Augmented Generation (RAG)** to provide contextually-aware programming assistance with cited documentation sources.


---

## 📖 Table of Contents
- [Problem Statement](#problem-statement)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [RAG Implementation](#rag-implementation)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Problem Statement

Learning programming is challenging due to:
- **Information Overload**: Scattered resources across the internet
- **Generic Answers**: AI responses without proper context or sources
- **Lack of Personalization**: One-size-fits-all solutions don't work
- **No Verification**: Answers without citations are hard to trust

### Solution: CodeMentor

CodeMentor solves these problems by implementing **RAG (Retrieval-Augmented Generation)** to:
1. ✅ Retrieve relevant documentation in real-time
2. ✅ Provide contextually-aware answers with citations
3. ✅ Adapt responses to user's skill level
4. ✅ Offer multiple features (Q&A, Code Review, Exercises, Learning Paths)

---

## ✨ Key Features

### 1. 💬 Smart Q&A System
- Real-time documentation retrieval using RAG
- Context-aware responses based on skill level
- Source citations for transparency
- Multi-language support (Python, JavaScript, Java, C++)

### 2. 🔍 AI Code Reviewer
- Comprehensive code analysis
- Bug detection and security checks
- Performance optimization suggestions
- Best practices recommendations
- Quality scoring (0-100)

### 3. 📝 Personalized Exercise Generator
- Custom coding challenges based on topic and difficulty
- Progressive hints system
- Auto-generated test cases
- Complete solutions with explanations

### 4. 🗺️ Learning Path Creator
- Goal-based curriculum design
- Time-aware planning (1-12 months)
- Project recommendations
- Resource curation with links
- Milestone tracking

---

## 🛠️ Tech Stack

### Core Technologies
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.31 | Interactive web UI |
| **Backend** | Python 3.8+ | Core application logic |
| **LLM** | OpenAI GPT-4 | Natural language generation |
| **Embeddings** | SentenceTransformers | Text vectorization |
| **Vector DB** | ChromaDB | Similarity search & RAG |
| **API Client** | OpenAI Python SDK | API integration |

### Dependencies
```
streamlit==1.31.0
openai==1.12.0
chromadb==0.4.22
sentence-transformers==2.3.1
python-dotenv==1.0.1
tiktoken==0.5.2
beautifulsoup4==4.12.3
requests==2.31.0
tenacity==8.2.3
numpy>=1.24.0
```

---

## 🏗️ Architecture

### System Architecture
```
┌─────────────────────────────────────────┐
│         User Interface (Streamlit)      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Application Layer             │
│  ┌──────────┐  ┌──────────┐            │
│  │ Q&A      │  │ Code     │  ┌────────┐│
│  │ System   │  │ Review   │  │Exercise││
│  └────┬─────┘  └────┬─────┘  └───┬────┘│
└───────┼─────────────┼─────────────┼─────┘
        │             │             │
┌───────▼─────────────▼─────────────▼─────┐
│            Core Layer                    │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  RAG Engine  │◄──►│ LLM Handler  │  │
│  │  - ChromaDB  │    │  - GPT-4 API │  │
│  │  - Embeddings│    │  - Prompts   │  │
│  └──────────────┘    └──────────────┘  │
└──────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Data Layer                      │
│  ┌────────────────┐  ┌───────────────┐ │
│  │  Vector Store  │  │ Documentation │ │
│  │  (ChromaDB)    │  │   Sources     │ │
│  └────────────────┘  └───────────────┘ │
└──────────────────────────────────────────┘
```

### RAG Flow
```
User Query
    ↓
Generate Query Embedding (SentenceTransformer)
    ↓
Vector Similarity Search (ChromaDB)
    ↓
Retrieve Top-K Documents
    ↓
Build Context-Enhanced Prompt
    ↓
GPT-4 Generation with Context
    ↓
Return Answer with Citations
```

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- 4GB RAM minimum
- 2GB free disk space

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/codementor-ai.git
cd codementor-ai
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create `.env` file in project root:
```bash
OPENAI_API_KEY=your-openai-api-key-here
MODEL_NAME=gpt-4
EMBEDDING_MODEL=text-embedding-ada-002
```

### Step 5: Initialize Vector Database
```bash
python scripts/initialize_db.py
```

Expected output:
```
============================================================
CodeMentor - Vector Database Initialization
============================================================

Step 1: Initializing RAG Engine...
✅ RAG Engine initialized

Step 2: Loading sample documentation...
✅ Loaded 5 documents

Step 3: Processing documents...
✅ Processed into 5 document chunks

Step 4: Adding documents to vector database...
✅ All documents added successfully!

✅ Initialization completed successfully!
============================================================
```

### Step 6: Run Application
```bash
streamlit run app.py
```

Open your browser to: **http://localhost:8501**

---

## 🎮 Usage

### 1. Ask Programming Questions
```python
# Example Question:
"How do I handle exceptions in Python?"

# Response includes:
- Detailed explanation
- Code examples
- Best practices
- Cited documentation sources
```

### 2. Get Code Reviewed
```python
# Submit your code
def calculate_average(nums):
    total = 0
    for i in range(len(nums)):
        total = total + nums[i]
    return total / len(nums)

# Receive:
- Quality score
- Identified issues
- Refactoring suggestions
- Best practices
```

### 3. Generate Exercises
```python
# Input:
Topic: "loops"
Difficulty: "Medium"

# Output:
- Problem statement
- Requirements
- Test cases
- Progressive hints
- Complete solution
```

### 4. Create Learning Path
```python
# Input:
Goal: "Learn web development"
Timeframe: "3 months"
Hours/week: 10

# Output:
- Structured curriculum
- Learning phases
- Project ideas
- Milestones
- Resources
```

---

---

## 📁 Project Structure
```
codementor-ai/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
├── .gitignore                      # Git ignore file
├── README.md                       # This file
│
├── core/                           # Core functionality
│   ├── __init__.py
│   ├── rag_engine.py              # RAG implementation with ChromaDB
│   └── llm_handler.py             # OpenAI API handler
│
├── features/                       # Feature modules
│   ├── __init__.py
│   ├── qa_system.py               # Q&A with RAG
│   ├── code_review.py             # Code review logic
│   ├── exercise_generator.py      # Exercise generation
│   └── learning_path.py           # Learning path creator
│
├── scripts/                        # Utility scripts
│   └── initialize_db.py           # Database initialization
│
├── utils/                          # Helper utilities
│   ├── __init__.py
│   └── web_scraper.py             # Documentation scraper
│
├── data/                           # Data directory
│   ├── vector_db/                 # ChromaDB storage
│   ├── documentation/             # Downloaded docs
│   └── user_data/                 # User progress (optional)
│
└── screenshots/                    # Demo screenshots
    ├── dashboard.png
    ├── qa_system.png
    ├── code_review.png
    └── exercise_generator.png
```

---

## 🧠 RAG Implementation Details

### What is RAG?
**Retrieval-Augmented Generation (RAG)** combines information retrieval with language generation to provide accurate, contextually-aware responses.

### How CodeMentor Implements RAG

#### 1. Document Ingestion
```python
# Sample documentation is chunked and stored
documents = [
    {
        'text': "Python Functions: Use 'def' keyword...",
        'metadata': {'language': 'Python', 'type': 'tutorial'}
    }
]

# Generate embeddings using SentenceTransformer
embeddings = model.encode(texts)

# Store in ChromaDB for similarity search
collection.add(documents=texts, embeddings=embeddings)
```

#### 2. Query Processing
```python
# User asks: "How do I create a function in Python?"

# Generate query embedding
query_embedding = model.encode(query)

# Retrieve top-K similar documents
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)
```

#### 3. Context-Enhanced Generation
```python
# Build prompt with retrieved context
prompt = f"""
Context from documentation:
{retrieved_docs}

Question: {user_question}

Provide a clear answer based on the context.
"""

# Generate response with GPT-4
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

### Benefits of RAG
- ✅ **Accurate**: Responses grounded in documentation
- ✅ **Up-to-date**: Add new docs without retraining
- ✅ **Transparent**: Citations show source material
- ✅ **Cost-effective**: No expensive fine-tuning needed

---

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Multi-language UI (translations)
- [ ] Voice input/output
- [ ] GitHub integration for code analysis
- [ ] Collaborative coding sessions
- [ ] Mobile app (iOS/Android)
- [ ] Gamification (badges, leaderboards)
- [ ] Video tutorial generation
- [ ] Live coding interviews practice

### Technical Improvements
- [ ] Fine-tuned models for programming
- [ ] Hybrid search (BM25 + semantic)
- [ ] Streaming responses
- [ ] Advanced analytics dashboard
- [ ] GraphRAG for knowledge graphs
- [ ] Multi-modal support (images, diagrams)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---



## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Streamlit team for the framework
- ChromaDB for vector database
- SentenceTransformers community
- All open-source contributors

---

## 📊 Project Stats

- **Lines of Code**: 3,000+
- **Files**: 15+
- **Features**: 4 major features
- **Tech Stack**: 10+ technologies
- **Development Time**: 75+ hours
- **Documentation**: Comprehensive

---


---

**⭐ If you find this project helpful, please give it a star!**

**Happy Learning! 🚀📚**
