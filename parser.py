"""
Parser module to clean and structure LLM responses.
This ensures consistent output format regardless of which LLM we use.
"""

import re
from typing import Dict, Any

class ResponseParser:
    """
    Handles parsing and formatting of LLM responses.
    This class makes sure we get clean, structured output.
    """
    
    def __init__(self):
        # Patterns for extracting different types of content
        self.code_pattern = r'```(?:\w+)?\n?(.*?)\n?```'
        self.explanation_sections = [
            'explanation', 'overview', 'summary', 
            'what this code does', 'how it works'
        ]
    
    def parse_code_generation(self, response: str) -> Dict[str, Any]:
        """
        Parses code generation response into structured format.
        Separates code from explanations and comments.
        """
        
        # Extract code blocks
        code_matches = re.findall(self.code_pattern, response, re.DOTALL | re.IGNORECASE)
        
        # Get the main code (usually the longest block)
        main_code = ""
        if code_matches:
            main_code = max(code_matches, key=len).strip()
        
        # Extract explanation (everything not in code blocks)
        explanation = re.sub(self.code_pattern, '', response, flags=re.DOTALL | re.IGNORECASE)
        explanation = explanation.strip()
        
        return {
            'code': main_code,
            'explanation': explanation,
            'has_code': bool(main_code),
            'has_explanation': bool(explanation)
        }
    
    def parse_explanation(self, response: str) -> Dict[str, Any]:
        """
        Parses code explanation response.
        Structures the explanation into readable sections.
        """
        
        # Split into paragraphs for better readability
        paragraphs = [p.strip() for p in response.split('\n\n') if p.strip()]
        
        # Try to identify key sections
        overview = ""
        details = []
        
        for paragraph in paragraphs:
            # Check if this paragraph looks like an overview
            lower_para = paragraph.lower()
            if any(section in lower_para for section in self.explanation_sections):
                if not overview:  # Take the first overview-like paragraph
                    overview = paragraph
            else:
                details.append(paragraph)
        
        return {
            'overview': overview,
            'details': details,
            'full_explanation': response,
            'paragraph_count': len(paragraphs)
        }
    
    def parse_debug_response(self, response: str) -> Dict[str, Any]:
        """
        Parses debugging response into structured sections.
        Separates problem identification, explanation, and solution.
        """
        
        # Extract corrected code if present
        corrected_code = ""
        code_matches = re.findall(self.code_pattern, response, re.DOTALL | re.IGNORECASE)
        if code_matches:
            # Usually the corrected code is the last or longest code block
            corrected_code = code_matches[-1].strip()
        
        # Remove code blocks from explanation
        explanation = re.sub(self.code_pattern, '\n[CODE BLOCK REMOVED]\n', response, flags=re.DOTALL | re.IGNORECASE)
        explanation = explanation.strip()
        
        # Try to identify problem description (usually at the beginning)
        paragraphs = [p.strip() for p in explanation.split('\n\n') if p.strip()]
        problem_description = paragraphs[0] if paragraphs else ""
        
        return {
            'problem_description': problem_description,
            'corrected_code': corrected_code,
            'full_explanation': explanation,
            'has_corrected_code': bool(corrected_code),
            'solution_steps': paragraphs
        }
    
    def clean_response(self, response: str) -> str:
        """
        General cleanup of LLM responses.
        Removes extra whitespace and formatting issues.
        """
        
        # Remove excessive newlines
        cleaned = re.sub(r'\n{3,}', '\n\n', response)
        
        # Remove trailing/leading whitespace
        cleaned = cleaned.strip()
        
        # Fix common formatting issues
        cleaned = re.sub(r'```(\w+)\n\n+', r'```\1\n', cleaned)
        
        return cleaned
