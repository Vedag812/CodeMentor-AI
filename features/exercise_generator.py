"""
Exercise Generator
"""

from typing import Dict, List, Any
from core.llm_handler import LLMHandler, PromptTemplate

class ExerciseGenerator:
    """Generates personalized coding exercises"""
    
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
    
    def generate_exercise(self, topic: str, language: str = "Python",
                         difficulty: str = "Medium", exercise_type: str = "Coding Challenge",
                         user_level: str = "Intermediate") -> Dict[str, Any]:
        """Generate a coding exercise"""
        prompt = f"""Create a {difficulty} {exercise_type} in {language} about {topic}.

Include:
1. Clear problem statement
2. 3-5 specific requirements
3. 2 input/output examples
4. 3 progressive hints
5. A complete solution with explanation

Make it appropriate for a {user_level} programmer."""

        system_prompt = PromptTemplate.get_system_prompt("exercise_gen")
        
        try:
            response = self.llm_handler.generate(
                prompt=prompt, system_message=system_prompt
            )
            
            return {
                'problem_statement': f"Exercise on {topic}",
                'requirements': [f"Solve the {topic} problem"],
                'examples': [{'input': 'Example input', 'output': 'Example output'}],
                'hints': ['Think step by step', 'Break down the problem', 'Test edge cases'],
                'test_cases': f'# Test cases for {topic}',
                'solution': response,
                'explanation': 'See solution above',
                'topic': topic,
                'language': language,
                'difficulty': difficulty
            }
            
        except Exception as e:
            return {
                'problem_statement': f'Error: {str(e)}',
                'requirements': [],
                'examples': [],
                'hints': [],
                'test_cases': '',
                'solution': '',
                'explanation': '',
                'topic': topic,
                'language': language,
                'difficulty': difficulty
            }