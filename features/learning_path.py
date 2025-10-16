
"""
Learning Path Creator
"""

from typing import Dict, List, Any
from core.llm_handler import LLMHandler, PromptTemplate

class LearningPathCreator:
    """Creates personalized learning paths"""
    
    def __init__(self, llm_handler: LLMHandler):
        self.llm_handler = llm_handler
    
    def create_path(self, goal: str, current_level: str, timeframe: str,
                   time_commitment: int, current_knowledge: List[str]) -> Dict[str, Any]:
        """Create a personalized learning path"""
        knowledge_str = ", ".join(current_knowledge) if current_knowledge else "no prior knowledge"
        
        prompt = f"""Create a learning path for: "{goal}"

Student Profile:
- Level: {current_level}
- Timeframe: {timeframe}
- Hours/week: {time_commitment}
- Current Knowledge: {knowledge_str}

Provide:
1. Overview (2-3 sentences)
2. 4-6 learning phases with topics and projects
3. Key milestones
4. Success tips"""

        system_prompt = PromptTemplate.get_system_prompt("learning_path")
        
        try:
            response = self.llm_handler.generate(
                prompt=prompt, system_message=system_prompt
            )
            
            return {
                'overview': f'Learning path for: {goal}',
                'phases': [
                    {
                        'title': 'Foundation Phase',
                        'duration': '4 weeks',
                        'description': response[:300],
                        'topics': ['Core concepts', 'Basic syntax', 'Fundamentals'],
                        'projects': ['Starter project'],
                        'resources': []
                    }
                ],
                'milestones': ['Start learning', 'Complete basics', 'Build project', 'Achieve goal'],
                'success_tips': ['Practice daily', 'Build projects', 'Join communities', 'Stay consistent'],
                'goal': goal,
                'timeframe': timeframe,
                'estimated_hours': time_commitment * 12
            }
            
        except Exception as e:
            return {
                'overview': f'Error: {str(e)}',
                'phases': [],
                'milestones': [],
                'success_tips': [],
                'goal': goal,
                'timeframe': timeframe,
                'estimated_hours': 0
            }