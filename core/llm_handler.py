"""
LLM Handler - OpenAI API Integration
Handles all interactions with OpenAI's GPT models
"""

import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
import tiktoken
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMHandler:
    """
    Handler for OpenAI GPT models
    """
    
    def __init__(self, 
                 model: str = None,
                 temperature: float = 0.7,
                 max_tokens: int = 2000):
        """
        Initialize LLM Handler
        
        Args:
            model: OpenAI model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv('MODEL_NAME', 'gpt-4o')
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except:
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        print(f"✅ LLM Handler initialized with model: {self.model}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self,
                prompt: str,
                system_message: Optional[str] = None,
                temperature: Optional[float] = None,
                max_tokens: Optional[int] = None) -> str:
        """
        Generate text using OpenAI API
        
        Args:
            prompt: User prompt
            system_message: System message for context
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise
    
    def generate_with_context(self,
                            prompt: str,
                            context: List[str],
                            system_message: Optional[str] = None) -> str:
        """
        Generate text with context from RAG
        
        Args:
            prompt: User prompt
            context: Retrieved context documents
            system_message: System message
            
        Returns:
            Generated text with context
        """
        # Build context string
        context_str = "\n\n---\n\n".join([
            f"Document {i+1}:\n{doc}" 
            for i, doc in enumerate(context)
        ])
        
        # Build enhanced prompt
        enhanced_prompt = f"""Based on the following context, please answer the question.

Context:
{context_str}

Question: {prompt}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information, acknowledge this and provide your best answer based on your knowledge."""
        
        return self.generate(
            prompt=enhanced_prompt,
            system_message=system_message
        )
    
    def generate_streaming(self,
                          prompt: str,
                          system_message: Optional[str] = None):
        """
        Generate text with streaming response
        
        Args:
            prompt: User prompt
            system_message: System message
            
        Yields:
            Text chunks
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error in streaming: {str(e)}")
            raise
    
    def generate_json(self,
                     prompt: str,
                     system_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate JSON response
        
        Args:
            prompt: User prompt
            system_message: System message
            
        Returns:
            JSON response as dictionary
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            import json
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error generating JSON: {str(e)}")
            raise
    
    def chat(self,
            messages: List[Dict[str, str]],
            temperature: Optional[float] = None) -> str:
        """
        Multi-turn chat conversation
        
        Args:
            messages: List of message dictionaries
            temperature: Override default temperature
            
        Returns:
            Assistant's response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            raise


class PromptTemplate:
    """
    Template class for managing prompts
    """
    
    # System prompts for different features
    SYSTEM_PROMPTS = {
        "qa": """You are an expert programming tutor with deep knowledge of multiple programming languages and frameworks. 
Your role is to:
- Provide clear, accurate, and helpful answers to programming questions
- Use the provided documentation context when available
- Explain concepts in a way appropriate for the user's skill level
- Include practical examples when helpful
- Cite sources when referencing specific documentation
- Be encouraging and supportive""",
        
        "code_review": """You are a senior software engineer conducting a thorough code review.
Your role is to:
- Identify bugs, security issues, and performance problems
- Suggest improvements following best practices
- Explain the reasoning behind your suggestions
- Be constructive and educational in your feedback
- Consider the user's skill level in your explanations
- Provide refactored code examples when appropriate""",
        
        "exercise_gen": """You are a creative programming instructor designing educational exercises.
Your role is to:
- Create engaging and educational coding challenges
- Match difficulty to the user's skill level
- Include clear problem statements and examples
- Provide helpful hints without giving away the solution
- Create comprehensive test cases
- Explain the learning objectives""",
        
        "learning_path": """You are an experienced programming mentor creating personalized learning paths.
Your role is to:
- Design structured curriculum based on user goals
- Break down complex topics into manageable phases
- Suggest practical projects for hands-on learning
- Recommend high-quality learning resources
- Provide realistic timelines and milestones
- Offer motivational guidance and tips for success"""
    }
    
    @staticmethod
    def get_system_prompt(feature: str) -> str:
        """Get system prompt for a feature"""
        return PromptTemplate.SYSTEM_PROMPTS.get(feature, "")
    
    @staticmethod
    def build_qa_prompt(question: str, 
                       context: List[str], 
                       language: str,
                       level: str) -> str:
        """Build Q&A prompt with context"""
        context_str = "\n\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(context)])
        
        return f"""Programming Language: {language}
User Level: {level}

Context from Documentation:
{context_str}

Question: {question}

Please provide a comprehensive answer that:
1. Directly addresses the question
2. Uses information from the provided context when relevant
3. Is appropriate for a {level} level programmer
4. Includes practical examples if helpful
5. Cites the context sources using [1], [2], etc.
"""
    
    @staticmethod
    def build_code_review_prompt(code: str,
                                 language: str,
                                 review_type: str,
                                 level: str) -> str:
        """Build code review prompt"""
        return f"""Review the following {language} code written by a {level} level programmer.

Code:
```{language.lower()}
{code}
```

Please provide a {review_type} review that includes:
1. Overall quality assessment (score out of 100)
2. What the code does well (strengths)
3. Issues found (bugs, security, performance, style)
4. Specific suggestions for improvement
5. Refactored code example if significant improvements are possible

Format your response as JSON with keys: quality_score, summary, strengths, issues, suggestions, refactored_code
"""