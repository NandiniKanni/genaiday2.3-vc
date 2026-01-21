"""
Main Streamlit application for Vibe Code Editor + AI Debugger
GenAI Hackathon Ready 🚀
"""

import streamlit as st
from groq import Groq
from openai import OpenAI

from prompts import (
    get_code_generation_prompt,
    get_explanation_prompt,
    get_debug_prompt
)
from parser import ResponseParser
from utils import (
    get_skill_level_description,
    get_supported_languages,
    validate_user_input,
    show_loading_message
)


class VibeCodeEditor:
    """
    Main application class.
    Handles Generate, Explain, Debug modes.
    """

    def __init__(self):
        self.parser = ResponseParser()
        self.setup_llm()

    def setup_llm(self):
    """
    Initialize LLM using Streamlit Secrets
    Priority: Groq → OpenAI
    """
    groq_key = st.secrets.get("GROQ_API_KEY", None)
    openai_key = st.secrets.get("OPENAI_API_KEY", None)

    if groq_key:
        self.llm_client = Groq(api_key=groq_key, timeout=30)
        self.llm_provider = "groq"
        self.model_name = "llama-3.1-70b-versatile"          # ← fixed: remove the bad second assignment
    elif openai_key:
        self.llm_client = OpenAI(api_key=openai_key)
        self.llm_provider = "openai"
        self.model_name = "gpt-4o-mini"                      # better default in 2025/2026
    else:
        st.error("❌ Add GROQ_API_KEY or OPENAI_API_KEY in Streamlit Secrets")
        st.stop()
    # ---------------- UI ---------------- #

    def render_header(self):
        st.set_page_config(
            page_title="Vibe Code Editor",
            page_icon="🚀",
            layout="wide"
        )

        st.title("🚀 Vibe Code Editor + AI Debugger")
        st.markdown(
            "**Skill-adaptive AI coding assistant for learning, building & debugging.**"
        )

        st.sidebar.info(f"🤖 Provider: **{self.llm_provider.upper()}**")

    def render_mode_selection(self):
    st.sidebar.title("🎯 Mode")

    mode = st.sidebar.radio(
        "Choose:",
        ["🔧 Generate Code", "📚 Explain Code", "🐛 Debug Code", "⚡ Optimize Code"]
    )

    # Fixed: proper mapping
    mode_map = {
        "🔧 Generate Code": "Generate",
        "📚 Explain Code":  "Explain",
        "🐛 Debug Code":    "Debug",
        "⚡ Optimize Code": "Optimize"
    }
    return mode_map[mode]

    def render_skill_selection(self):
        st.sidebar.markdown("---")
        st.sidebar.title("📊 Skill Level")

        skill = st.sidebar.selectbox(
            "Your level:",
            ["Beginner", "Intermediate", "Advanced"]
        )

        st.sidebar.info(
            f"**{skill}** — {get_skill_level_description(skill)}"
        )

        return skill

    # ---------------- MODES ---------------- #

    def render_generate_mode(self, skill):
        st.header("🔧 Generate Code")

        col1, col2 = st.columns([3, 1])

        with col1:
            task = st.text_area(
                "What do you want to build?",
                placeholder="Create a Java program to reverse an array"
            )

        with col2:
            language = st.selectbox(
                "Language",
                get_supported_languages()
            )

        if st.button("🚀 Generate", type="primary"):
            validation = validate_user_input(task, language, skill)

            if not validation["is_valid"]:
                for err in validation["errors"]:
                    st.error(err)
                return

            with show_loading_message("Generating code..."):
                prompt = get_code_generation_prompt(task, language, skill)
                response = self.call_llm(prompt)

            if response:
                parsed = self.parser.parse_code_generation(response)

                if parsed["has_code"]:
                    st.subheader("📝 Code")
                    st.code(parsed["code"], language=language.lower())

                    if parsed["has_explanation"]:
                        st.subheader("💡 Explanation")
                        st.markdown(parsed["explanation"])
                else:
                    st.warning("Could not extract code")
                    st.markdown(response)

    def render_explain_mode(self, skill):
        st.header("📚 Explain Code")

        col1, col2 = st.columns([3, 1])

        with col1:
            code = st.text_area(
                "Paste code",
                height=220
            )

        with col2:
            language = st.selectbox(
                "Language",
                get_supported_languages()
            )

        if st.button("📖 Explain", type="primary"):
            if not code.strip():
                st.error("Paste some code first")
                return

            with show_loading_message("Explaining..."):
                prompt = get_explanation_prompt(code, language, skill)
                response = self.call_llm(prompt)

            parsed = self.parser.parse_explanation(response)

            st.subheader("📝 Code")
            st.code(code, language=language.lower())

            st.subheader("💡 Explanation")
            if parsed["overview"]:
                st.markdown(f"**Overview:** {parsed['overview']}")

            for i, step in enumerate(parsed["details"], 1):
                st.markdown(f"**Step {i}:** {step}")

    def render_debug_mode(self, skill):
        st.header("🐛 Debug Code")

        col1, col2 = st.columns([3, 1])

        with col1:
            code = st.text_area("Buggy Code", height=220)
            error = st.text_area("Error Message (optional)", height=100)

        with col2:
            language = st.selectbox(
                "Language",
                get_supported_languages()
            )

        if st.button("🔍 Debug", type="primary"):
            if not code.strip():
                st.error("Paste code to debug")
                return

            with show_loading_message("Debugging..."):
                prompt = get_debug_prompt(code, error, language, skill)
                response = self.call_llm(prompt)

            parsed = self.parser.parse_debug_response(response)

            st.subheader("❌ Issue")
            if parsed["problem_description"]:
                st.error(parsed["problem_description"])

            if parsed["has_corrected_code"]:
                st.subheader("✅ Fixed Code")
                st.code(parsed["corrected_code"], language=language.lower())

            st.subheader("💡 Explanation")
            st.markdown(parsed["full_explanation"])

  # Replace your existing render_optimize_mode with this improved version
def render_optimize_mode(self, skill_level: str):
    st.header("⚡ Optimize Code")

    col1, col2 = st.columns([3, 1])

    with col1:
        code = st.text_area(
            "Paste your code here",
            height=240,
            placeholder="Paste your function / solution...",
            key="optimize_code_input"
        )
        problem_desc = st.text_area(
            "Problem / Goal (optional but very helpful)",
            height=110,
            placeholder="→ Find two numbers that sum to target\n→ Sort array without extra space\n→ etc.",
            key="optimize_problem"
        )

    with col2:
        language = st.selectbox(
            "Language",
            get_supported_languages(),
            key="optimize_lang"
        )

    if st.button("⚡ Analyze & Optimize", type="primary", use_container_width=True):
        if not code.strip():
            st.error("Please paste some code first.")
            return

        with st.spinner("Analyzing complexity + searching for better approach..."):
            prompt = self._get_optimization_prompt(code, problem_desc, language, skill_level)
            raw_response = self.call_llm(prompt)

        if not raw_response:
            st.error("No response from model. Check API key / rate limits.")
            return

        # Very simple structured rendering (you can later use better parser)
        st.success("Analysis ready!")

        # Try to extract code block if present
        code_block = extract_code_from_response(raw_response)  # from utils.py

        sections = raw_response.split("\n\n")
        in_code = False
        current_section = []

        for line in sections:
            if "```" in line and not in_code:
                in_code = True
                st.subheader("Optimized Version")
                st.code(code_block or "No code block found", language=language.lower())
                continue
            if "```" in line and in_code:
                in_code = False
                continue

            if not in_code:
                current_section.append(line)

        if current_section:
            st.markdown("\n\n".join(current_section))
Add this helper method inside the class (or in prompts.py):
Pythondef _get_optimization_prompt(self, code, problem_desc, language, skill):
    return f"""You are an expert algorithms engineer.

Language: {language}
User skill: {skill}
Problem / goal (if provided): {problem_desc or "not provided — analyze the code anyway"}

Code to optimize:
```python
{code}

    # ---------------- RUN ---------------- #

    def run(self):
        self.render_header()

        mode = self.render_mode_selection()
        skill = self.render_skill_selection()

        if mode == "Generate Code":
            self.render_generate_mode(skill)
        elif mode == "Explain Code":
            self.render_explain_mode(skill)
        elif mode == "Debug Code":
            self.render_debug_mode(skill)
        elif mode == "Optimize Code":
            self.render_optimize_mode(skill)


if __name__ == "__main__":
    VibeCodeEditor().run()
