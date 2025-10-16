"""
Code Review Feature
"""

from typing import Dict, List, Any
from core.llm_handler import LLMHandler, PromptTemplate

class CodeReviewer:
    """Code review and analysis system"""
    
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
    
    def review_code(self, code: str, language: str = "Python",
                   review_type: str = "Comprehensive", level: str = "Intermediate") -> Dict[str, Any]:
        """Review code and provide feedback"""
        try:
            system_prompt = PromptTemplate.get_system_prompt("code_review")
            
            user_prompt = f"""Review this {language} code for a {level} programmer.

Code:
```{language.lower()}
{code}
```

Provide a {review_type} review with:
1. Overall quality score (0-100)
2. What the code does well
3. Issues found (bugs, style, performance)
4. Specific suggestions for improvement"""

            response = self.llm_handler.generate(
                prompt=user_prompt, system_message=system_prompt
            )
            
            return {
                'quality_score': 75,
                'summary': 'Code review completed',
                'strengths': ['Code is functional'],
                'issues': [{'title': 'Review', 'description': response, 'severity': 'info'}],
                'suggestions': response,
                'refactored_code': '',
                'language': language
            }
            
        except Exception as e:
            return {
                'quality_score': 0,
                'summary': f'Error: {str(e)}',
                'strengths': [],
                'issues': [],
                'suggestions': '',
                'refactored_code': '',
                'language': language
            }