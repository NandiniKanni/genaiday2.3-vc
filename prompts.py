def get_code_generation_prompt(task: str, language: str, skill_level: str) -> str:
    base_prompt = f"""
You are a {skill_level.lower()}-level programming tutor. 
Generate {language} code for: "{task}"
IMPORTANT RULES:
- Write code appropriate for {skill_level} level programmers
- Include comments suitable for this skill level
- Use coding style typical for {skill_level} developers
"""
    if skill_level == "Beginner":
        specific_prompt = """
BEGINNER REQUIREMENTS:
- Use simple, readable variable names
- Comment every line
- Break complex operations into simple steps
- Use basic language features
- Include example usage
- Explain each part in plain English
"""
    elif skill_level == "Intermediate":
        specific_prompt = """
INTERMEDIATE REQUIREMENTS:
- Clean, meaningful variable and function names
- Comment complex logic only
- Follow coding conventions
- Use appropriate data structures
- Include error handling
- Write modular, reusable code
"""
    else:  # Advanced
        specific_prompt = """
ADVANCED REQUIREMENTS:
- Optimized, efficient code
- Advanced language features
- Minimal but meaningful comments
- Consider edge cases and performance
- Apply relevant design patterns
- Focus on maintainability and scalability
"""
    return base_prompt + specific_prompt


def get_explanation_prompt(code: str, language: str, skill_level: str) -> str:
    base_prompt = f"""
You are a {skill_level.lower()}-level programming tutor.
Explain this {language} code in a way that a {skill_level} programmer would understand:

{code}

EXPLANATION REQUIREMENTS:
"""
    if skill_level == "Beginner":
        specific_prompt = """
- Explain every line
- Use simple, non-technical language
- Define programming terms
- Show output
- Explain WHY
- Compare to real-world analogies
"""
    elif skill_level == "Intermediate":
        specific_prompt = """
- Explain overall logic
- Highlight key concepts
- Explain complex parts
- Mention alternatives briefly
- Point out good practices
"""
    else:  # Advanced
        specific_prompt = """
- Focus on algorithm complexity
- Discuss design patterns or architecture
- Analyze performance
- Suggest optimizations
- Compare alternatives
"""
    return base_prompt + specific_prompt


def get_debug_prompt(code: str, error: str, language: str, skill_level: str) -> str:
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
Identify what is wrong (simple terms)

Explain WHY

Show corrected code with comments

Explain how to avoid this

Provide a simple test case
"""
elif skill_level == "Intermediate":
specific_prompt = """

Identify root cause

Explain underlying concept

Provide corrected code

Suggest debugging techniques

Mention related concepts
"""
else:
specific_prompt = """

Analyze technical root cause

Discuss performance/design implications

Provide optimized solution

Suggest refactoring

Recommend debugging tools
"""
return base_prompt + specific_prompt











