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
{error_section}

<PROBLEM> Explain what is wrong in simple terms. </PROBLEM>

<CORRECTED_CODE>
Provide corrected code only inside code block.
</CORRECTED_CODE>

<EXPLANATION> Explain the fix in simple terms. </EXPLANATION>

DEBUGGING REQUIREMENTS:
"""
if skill_level == "Beginner":
    specific_prompt = """
1.Identify what is wrong (in simple terms)

2.Explain WHY this error happens (like explaining to a friend)

3.Show the corrected code with comments

4.Explain how to avoid this mistake in the future

5.Provide a simple test case to verify the fix

Use beginner-friendly language and be very patient in your explanation.
"""
elif skill_level == "Intermediate":
    specific_prompt = """
1.Identify the root cause of the issue

2.Explain the underlying programming concept involved

3.Provide the corrected code with good practices

4.Suggest debugging techniques for similar issues

5.Mention related concepts to be aware of
Assume familiarity with basic programming but explain advanced concepts.
"""
else:  # Advanced
    specific_prompt = """
1.Analyze the technical root cause

2.Discuss performance/design implications of the bug

3.Provide an optimized, robust solution

4.Suggest refactoring opportunities

5.Recommend debugging tools/techniques for production
Focus on architectural and performance considerations.
"""
return base_prompt + specific_prompt

---

# ✅ After this fix
Your app will not crash anymore due to syntax error.

---

# 🔥 Next Step (if you want)
Once this is fixed, you can test your app again and I will help you fix the **LLM model decommissioned** error.

Just tell me:  
**“Now I’m getting model decommissioned error”** and I’ll guide you.









