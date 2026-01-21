"""
Prompt templates for different modes and skill levels.
This is the brain of our application - it tells the AI exactly what we want.
"""

def get_code_generation_prompt(task: str, language: str, skill_level: str) -> str:
    """
    Creates a prompt for code generation based on skill level.
    This is where the magic happens - different prompts for different levels!
    """
    
    # Base prompt that applies to all levels
    base_prompt = f"""
You are a {skill_level.lower()}-level programming tutor. 
Generate {language} code for: "{task}"

IMPORTANT RULES:
- Write code appropriate for {skill_level} level programmers
- Include comments suitable for this skill level
- Use coding style typical for {skill_level} developers
"""
    
    # Skill-specific instructions
    if skill_level == "Beginner":
        specific_prompt = """
BEGINNER REQUIREMENTS:
- Use very simple, readable variable names
- Add comments explaining EVERY line of code
- Break complex operations into multiple simple steps
- Use basic language features only
- Include example usage
- Explain what each part does in plain English
"""
    
    elif skill_level == "Intermediate":
        specific_prompt = """
INTERMEDIATE REQUIREMENTS:
- Use clean, meaningful variable and function names
- Add comments for complex logic only
- Follow standard coding conventions
- Use appropriate data structures
- Include error handling where relevant
- Write modular, reusable code
"""
    
    else:  # Advanced
        specific_prompt = """
ADVANCED REQUIREMENTS:
- Write optimized, efficient code
- Use advanced language features appropriately
- Minimal but meaningful comments
- Consider edge cases and performance
- Apply relevant design patterns
- Focus on maintainability and scalability
"""
    
    return base_prompt + specific_prompt


def get_explanation_prompt(code: str, language: str, skill_level: str) -> str:
    """
    Creates a prompt for explaining code based on skill level.
    Different levels need different depths of explanation.
    """
    
    base_prompt = f"""
You are a {skill_level.lower()}-level programming tutor.
Explain this {language} code in a way that a {skill_level} programmer would understand:

{code}

EXPLANATION REQUIREMENTS:
"""
    
    if skill_level == "Beginner":
        specific_prompt = """
- Explain every single line of code
- Use simple, non-technical language
- Define any programming terms you use
- Show what the output would look like
- Explain WHY each step is necessary
- Compare to real-world analogies where helpful
"""
    
    elif skill_level == "Intermediate":
        specific_prompt = """
- Explain the overall logic and approach
- Highlight important programming concepts used
- Explain complex parts in detail
- Mention alternative approaches briefly
- Point out good coding practices demonstrated
"""
    
    else:  # Advanced
        specific_prompt = """
- Focus on algorithm complexity and efficiency
- Discuss design patterns or architectural decisions
- Analyze performance implications
- Suggest potential optimizations
- Compare with alternative implementations
"""
    
    return base_prompt + specific_prompt


def get_debug_prompt(code: str, error: str, language: str, skill_level: str) -> str:
    """
    Creates a prompt for debugging code based on skill level.
    """
    
    error_section = f"\nError message: {error}" if error.strip() else ""

    base_prompt = f"""
You are a {skill_level.lower()}-level programming debugging tutor.

User Code:
```{language}
{code}








