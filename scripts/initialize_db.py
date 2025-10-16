"""
Initialize Database Script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rag_engine import RAGEngine, DocumentChunker

def load_sample_documents():
    """Load sample programming documentation"""
    
    python_docs = [
        {
            'text': """Python Functions: A function is a block of reusable code. Use 'def' keyword to define functions.

Example:
def greet(name):
    return f"Hello, {name}!"

Functions can have parameters, default values, and return statements.""",
            'metadata': {'title': 'Python Functions', 'language': 'Python', 'type': 'tutorial'}
        },
        {
            'text': """Python Lists: Lists are ordered, mutable collections. Created using square brackets [].

Common operations:
- append(x): Add item
- remove(x): Remove item
- sort(): Sort list
- len(): Get length

Example:
fruits = ['apple', 'banana']
fruits.append('cherry')""",
            'metadata': {'title': 'Python Lists', 'language': 'Python', 'type': 'reference'}
        },
        {
            'text': """Python Exception Handling: Use try-except blocks to handle errors gracefully.

Syntax:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Cleanup")

Common exceptions: ValueError, TypeError, KeyError, IndexError""",
            'metadata': {'title': 'Python Exceptions', 'language': 'Python', 'type': 'tutorial'}
        },
        {
            'text': """Python Classes: Object-oriented programming in Python.

Example:
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says Woof!"

dog = Dog("Buddy")
print(dog.bark())

Key OOP concepts: Encapsulation, Inheritance, Polymorphism""",
            'metadata': {'title': 'Python Classes', 'language': 'Python', 'type': 'tutorial'}
        },
        {
            'text': """JavaScript Promises: Handle asynchronous operations.

Example:
const promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("Success!"), 1000);
});

promise.then(result => console.log(result))
       .catch(error => console.error(error));

Modern syntax: async/await""",
            'metadata': {'title': 'JavaScript Promises', 'language': 'JavaScript', 'type': 'tutorial'}
        }
    ]
    
    return python_docs

def main():
    """Main initialization function"""
    print("="*60)
    print("CodeMentor - Vector Database Initialization")
    print("="*60)
    print()
    
    try:
        print("Step 1: Initializing RAG Engine...")
        rag_engine = RAGEngine()
        print("✅ RAG Engine initialized")
        print()
        
        print("Step 2: Loading sample documentation...")
        documents = load_sample_documents()
        print(f"✅ Loaded {len(documents)} documents")
        print()
        
        print("Step 3: Processing documents...")
        chunker = DocumentChunker()
        processed_docs = []
        
        for doc in documents:
            if len(doc['text']) > 1000:
                chunks = chunker.chunk_by_paragraphs(doc['text'], max_length=800)
                for i, chunk in enumerate(chunks):
                    processed_doc = {
                        'text': chunk,
                        'metadata': {**doc['metadata'], 'chunk': i + 1}
                    }
                    processed_docs.append(processed_doc)
            else:
                processed_docs.append(doc)
        
        print(f"✅ Processed into {len(processed_docs)} document chunks")
        print()
        
        print("Step 4: Adding documents to vector database...")
        rag_engine.add_documents(processed_docs)
        print("✅ Documents added successfully")
        print()
        
        print("Step 5: Database statistics...")
        stats = rag_engine.get_collection_stats()
        print(f"Collection: {stats['collection_name']}")
        print(f"Documents: {stats['document_count']}")
        print()
        
        print("="*60)
        print("✅ Initialization completed successfully!")
        print("="*60)
        print()
        print("Run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())