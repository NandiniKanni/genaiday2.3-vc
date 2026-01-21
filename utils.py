"""
Utility functions for the Vibe Code Editor.
This file contains helper functions that are used across the application.
"""

import streamlit as st
import re
from typing import Dict, Any

def get_skill_level_description(level: str) -> str:
    """
    Returns description for each skill level.
    This helps users understand what each level means.
    """
    descriptions = {
        "Beginner": "Simple syntax, lots of comments, basic concepts",
        "Intermediate": "Clean code, moderate complexity, good practices", 
        "Advanced": "Optimized solutions, design patterns, minimal comments"
    }
    return descriptions.get(level, "Unknown level")

def get_supported_languages() -> list:
    """
    Returns list of supported programming languages.
    Easy to extend for more languages later.
    """
    return ["Java", "Python", "JavaScript", "C++"]

def format_code_output(code: str, language: str) -> str:
    """
    Formats code with proper syntax highlighting.
    Streamlit automatically handles syntax highlighting.
    """
    return f"```{language.lower()}\n{code}\n```"

def validate_user_input(task: str, language: str, skill_level: str) -> Dict[str, Any]:
    """
    Validates user input and returns validation result.
    Prevents empty submissions and invalid selections.
    """
    errors = []
    
    if not task.strip():
        errors.append("Task description cannot be empty")
    
    if len(task.strip()) < 5:
        errors.append("Task description too short (minimum 5 characters)")
        
    if language not in get_supported_languages():
        errors.append("Unsupported programming language")
        
    if skill_level not in ["Beginner", "Intermediate", "Advanced"]:
        errors.append("Invalid skill level")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def extract_code_from_response(response: str) -> str:
    """
    Extracts code blocks from LLM response.
    Uses regex to find code between ``` markers.
    """
    # Look for code blocks marked with ```
    code_pattern = r'```(?:\w+)?\n?(.*?)\n?```'
    matches = re.findall(code_pattern, response, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # If no code blocks found, return the response as-is
    return response.strip()

def show_loading_message(message: str):
    """
    Shows a loading spinner with custom message.
    Makes the app feel more responsive.
    """
    return st.spinner(message)
