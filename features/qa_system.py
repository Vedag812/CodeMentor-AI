"""
Q&A System - Question Answering with RAG
"""

from typing import Dict, List, Any, Optional
from core.rag_engine import RAGEngine
from core.llm_handler import LLMHandler, PromptTemplate

class QASystem:
    """
    Question Answering system with RAG
    """
    
    def __init__(self, rag_engine: RAGEngine, llm_handler: LLMHandler):
        self.rag_engine = rag_engine
        self.llm_handler = llm_handler
    
    def answer_question(self,
                       question: str,
                       language: str = "Python",
                       level: str = "Intermediate",
                       include_examples: bool = True,
                       n_context_docs: int = 5) -> Dict[str, Any]:
        """
        Answer a programming question using RAG
        
        Args:
            question: User's question
            language: Programming language context
            level: User's skill level
            include_examples: Whether to include code examples
            n_context_docs: Number of context documents to retrieve
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            # Retrieve relevant documentation
            retrieved_docs = self.rag_engine.semantic_search(
                query=question,
                language=language,
                n_results=n_context_docs
            )
            
            # Extract context
            context = [doc['content'] for doc in retrieved_docs]
            
            # Build prompt
            system_prompt = PromptTemplate.get_system_prompt("qa")
            user_prompt = PromptTemplate.build_qa_prompt(
                question=question,
                context=context,
                language=language,
                level=level
            )
            
            if include_examples:
                user_prompt += "\n\nPlease include practical code examples in your answer."
            
            # Generate answer
            answer = self.llm_handler.generate(
                prompt=user_prompt,
                system_message=system_prompt
            )
            
            # Format sources
            sources = [
                {
                    'title': doc.get('metadata', {}).get('title', 'Documentation'),
                    'content': doc['content'][:200] + "...",
                    'relevance': doc['relevance'],
                    'url': doc.get('metadata', {}).get('url', '')
                }
                for doc in retrieved_docs[:3]
            ]
            
            return {
                'answer': answer,
                'sources': sources,
                'language': language,
                'level': level
            }
            
        except Exception as e:
            print(f"Error answering question: {str(e)}")
            return {
                'answer': f"I encountered an error processing your question: {str(e)}",
                'sources': [],
                'language': language,
                'level': level
            }
    
    def get_related_questions(self, 
                             question: str,
                             n_questions: int = 3) -> List[str]:
        """
        Generate related questions based on the input question
        
        Args:
            question: Original question
            n_questions: Number of related questions to generate
            
        Returns:
            List of related questions
        """
        prompt = f"""Given this programming question: "{question}"

Generate {n_questions} related questions that a learner might want to ask next. 
These should be:
- Slightly different in scope or depth
- Related to the same topic
- Progressively more advanced

Return only the questions, numbered 1-{n_questions}."""

        try:
            response = self.llm_handler.generate(prompt=prompt)
            # Parse numbered questions
            questions = [
                line.strip()[3:] for line in response.split('\n') 
                if line.strip() and line.strip()[0].isdigit()
            ]
            return questions[:n_questions]
        except:
            return []
    
    def explain_concept(self,
                       concept: str,
                       language: str = "Python",
                       level: str = "Beginner") -> str:
        """
        Explain a programming concept in detail
        
        Args:
            concept: Concept to explain
            language: Programming language context
            level: User's skill level
            
        Returns:
            Detailed explanation
        """
        prompt = f"""Explain the concept of "{concept}" in {language} programming for a {level} level programmer.

Your explanation should include:
1. A clear definition
2. Why it's important
3. How it works
4. Practical examples
5. Common use cases
6. Common pitfalls or mistakes

Make it engaging and easy to understand."""

        system_prompt = PromptTemplate.get_system_prompt("qa")
        
        try:
            explanation = self.llm_handler.generate(
                prompt=prompt,
                system_message=system_prompt
            )
            return explanation
        except Exception as e:
            return f"Error generating explanation: {str(e)}"