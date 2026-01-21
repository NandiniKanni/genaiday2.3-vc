"""
Main Streamlit application for Vibe Code Editor + AI Debugger.
This is the user interface that ties everything together.
"""

import streamlit as st
import os
from dotenv import load_dotenv
import openai
from groq import Groq
from prompts import get_code_generation_prompt, get_explanation_prompt, get_debug_prompt
from parser import ResponseParser
from utils import (
    get_skill_level_description, 
    get_supported_languages, 
    validate_user_input,
    show_loading_message
)

# Load environment variables
load_dotenv()

class VibeCodeEditor:
    """
    Main application class for the Vibe Code Editor.
    Handles all the different modes: Generate, Explain, Debug.
    """
    
    def __init__(self):
        self.parser = ResponseParser()
        self.setup_llm()
    
    def setup_llm(self):
        """
        Initialize the LLM client based on available API keys.
        Try Groq first (faster), fallback to OpenAI.
        """
        
        groq_key = os.getenv('GROQ_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if groq_key:
            self.llm_client = Groq(api_key=groq_key)
            self.llm_provider = "groq"
            self.model_name = "groq/compound"
        elif openai_key:
            self.llm_client = openai.OpenAI(api_key=openai_key)
            self.llm_provider = "openai" 
            self.model_name = "gpt-3.5-turbo"
        else:
            st.error("Please set GROQ_API_KEY or OPENAI_API_KEY in your .env file")
            st.stop()
    
    def call_llm(self, prompt: str) -> str:
        """
        Makes API call to the configured LLM.
        Handles different providers with unified interface.
        """
        
        try:
            if self.llm_provider == "groq":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "openai":
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
        except Exception as e:
            st.error(f"LLM API Error: {str(e)}")
            return ""
    
    def render_header(self):
        """
        Renders the application header with title and description.
        """
        st.set_page_config(
            page_title="Vibe Code Editor", 
            page_icon="🚀",
            layout="wide"
        )
        
        st.title("🚀 Vibe Code Editor + AI Debugger")
        st.markdown("""
        **Your skill-adaptive coding companion!** 
        Generate, explain, and debug code that matches your expertise level.
        """)
        
        # Show current LLM provider
        st.sidebar.info(f"🤖 Powered by: {self.llm_provider.upper()}")
    
    def render_mode_selection(self):
        """
        Renders the mode selection sidebar.
        """
        st.sidebar.title("🎯 Choose Your Mode")
        
        mode = st.sidebar.radio(
            "What would you like to do?",
            ["🔧 Generate Code", "📚 Explain Code", "🐛 Debug Code","optimize code"],
            help="Select the mode based on what you want to accomplish"
        )
        
        return mode.split(" ", 1)[1]  # Remove emoji, return just the text
    
    def render_skill_selection(self):
        """
        Renders skill level selection with descriptions.
        """
        st.sidebar.markdown("---")
        st.sidebar.title("📊 Your Skill Level")
        
        skill_level = st.sidebar.selectbox(
            "Choose your programming level:",
            ["Beginner", "Intermediate", "Advanced"],
            help="This affects how code and explanations are presented to you"
        )
        
        # Show description of selected level
        description = get_skill_level_description(skill_level)
        st.sidebar.info(f"**{skill_level}**: {description}")
        
        return skill_level
    
    def render_generate_mode(self, skill_level: str):
        """
        Renders the code generation interface.
        """
        st.header("🔧 Generate Code")
        st.markdown("Describe what you want to build, and I'll create code for your skill level!")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            task = st.text_area(
                "What do you want to build?",
                placeholder="e.g., Create a function to reverse an array",
                help="Be as specific as possible for better results"
            )
        
        with col2:
            language = st.selectbox(
                "Programming Language:",
                get_supported_languages()
            )
        
        # Generate button
        if st.button("🚀 Generate Code", type="primary"):
            # Validate input
            validation = validate_user_input(task, language, skill_level)
            
            if not validation['is_valid']:
                for error in validation['errors']:
                    st.error(error)
                return
            
            # Generate code
            with show_loading_message(f"Generating {skill_level.lower()}-level {language} code..."):
                prompt = get_code_generation_prompt(task, language, skill_level)
                response = self.call_llm(prompt)
                
                if response:
                    parsed = self.parser.parse_code_generation(response)
                    
                    # Display results
                    if parsed['has_code']:
                        st.success("✅ Code generated successfully!")
                        
                        # Show the code
                        st.subheader("📝 Generated Code")
                        st.code(parsed['code'], language=language.lower())
                        
                        # Show explanation if available
                        if parsed['has_explanation']:
                            st.subheader("💡 Explanation")
                            st.markdown(parsed['explanation'])
                    
                    else:
                        st.warning("⚠️ Could not extract code from response. Here's the full response:")
                        st.markdown(response)
    
    def render_explain_mode(self, skill_level: str):
        """
        Renders the code explanation interface.
        """
        st.header("📚 Explain Code")
        st.markdown("Paste your code here, and I'll explain it at your skill level!")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            code = st.text_area(
                "Paste your code here:",
                height=200,
                placeholder="// Paste your code here\nfor (int i = 0; i < array.length; i++) {\n    // Your code\n}"
            )
        
        with col2:
            language = st.selectbox(
                "Code Language:",
                get_supported_languages()
            )
        
        # Explain button
        if st.button("📖 Explain Code", type="primary"):
            if not code.strip():
                st.error("Please paste some code to explain!")
                return
            
            # Generate explanation
            with show_loading_message(f"Generating {skill_level.lower()}-level explanation..."):
                prompt = get_explanation_prompt(code, language, skill_level)
                response = self.call_llm(prompt)
                
                if response:
                    parsed = self.parser.parse_explanation(response)
                    
                    st.success("✅ Explanation generated!")
                    
                    # Show original code
                    st.subheader("📝 Your Code")
                    st.code(code, language=language.lower())
                    
                    # Show explanation
                    st.subheader("💡 Explanation")
                    
                    if parsed['overview']:
                        st.markdown(f"**Overview:** {parsed['overview']}")
                    
                    if parsed['details']:
                        for i, detail in enumerate(parsed['details'], 1):
                            if len(parsed['details']) > 1:
                                st.markdown(f"**Step {i}:** {detail}")
                            else:
                                st.markdown(detail)
    
    def render_debug_mode(self, skill_level: str):
        """
        Renders the debugging interface.
        """
        st.header("🐛 Debug Code")
        st.markdown("Having trouble with your code? I'll help you find and fix the issue!")
        
        # Input form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            code = st.text_area(
                "Paste your buggy code here:",
                height=200,
                placeholder="// Paste your code with issues here\nfor (int i = 0; i <= array.length; i++) {\n    System.out.println(array[i]);\n}"
            )
            
            error_msg = st.text_area(
                "Error message (optional):",
                height=100,
                placeholder="Paste any error messages you're getting..."
            )
        
        with col2:
            language = st.selectbox(
                "Code Language:",
                get_supported_languages()
            )
        
        # Debug button
        if st.button("🔍 Debug Code", type="primary"):
            if not code.strip():
                st.error("Please paste some code to debug!")
                return
            
            # Generate debug analysis
            with show_loading_message(f"Analyzing code for {skill_level.lower()}-level debugging..."):
                prompt = get_debug_prompt(code, error_msg, language, skill_level)
                response = self.call_llm(prompt)
                
                if response:
                    parsed = self.parser.parse_debug_response(response)
                    
                    st.success("✅ Debug analysis complete!")
                    
                    # Show original code
                    st.subheader("🔍 Original Code")
                    st.code(code, language=language.lower())
                    
                    # Show problem description
                    if parsed['problem_description']:
                        st.subheader("❌ Problem Identified")
                        st.error(parsed['problem_description'])
                    
                    # Show corrected code
                    if parsed['has_corrected_code']:
                        st.subheader("✅ Fixed Code")
                        st.code(parsed['corrected_code'], language=language.lower())
                    
                    # Show full explanation
                    st.subheader("💡 Detailed Explanation")
                    st.markdown(parsed['full_explanation'])
    
    def run(self):
        """
        Main application entry point.
        """
        self.render_header()
        
        # Get user selections
        mode = self.render_mode_selection()
        skill_level = self.render_skill_selection()
        
        # Render appropriate mode
        if mode == "Generate Code":
            self.render_generate_mode(skill_level)
        elif mode == "Explain Code":
            self.render_explain_mode(skill_level)
        elif mode == "Debug Code":
            self.render_debug_mode(skill_level)

# Run the application
if __name__ == "__main__":
    app = VibeCodeEditor()
    app.run()
