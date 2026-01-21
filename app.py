  Initialize LLM using Streamlit Secrets
        Priority: Groq → OpenAI
        """

        groq_key = st.secrets.get("GROQ_API_KEY", None)
        openai_key = st.secrets.get("OPENAI_API_KEY", None)

        if groq_key:
            
            self.llm_client = Groq(api_key=groq_key, timeout=30)

            self.llm_provider = "groq"
            self.model_name = "mixtral-8x7b-32768"

        elif openai_key:
            self.llm_client = OpenAI(api_key=openai_key)
            self.llm_provider = "openai"
            self.model_name = "gpt-3.5-turbo"

        else:
            st.error("❌ Add GROQ_API_KEY or OPENAI_API_KEY in Streamlit Secrets")
            st.stop()
@@ -60,7 +55,6 @@ def call_llm(self, prompt: str) -> str:
        """
        Unified LLM call handler
        """

        try:
            if self.llm_provider == "groq":
                response = self.llm_client.chat.completions.create(
@@ -105,7 +99,7 @@ def render_mode_selection(self):

        mode = st.sidebar.radio(
            "Choose:",
            ["🔧 Generate Code", "📚 Explain Code", "🐛 Debug Code","⚡ Optimize Code"]
            ["🔧 Generate Code", "📚 Explain Code", "🐛 Debug Code", "⚡ Optimize Code"]
        )

        return mode.split(" ", 1)[1]
@@ -244,8 +238,9 @@ def render_debug_mode(self, skill):

            st.subheader("💡 Explanation")
            st.markdown(parsed["full_explanation"])
                def render_optimize_mode(self, skill_level: str):
             st.header("⚡ Optimize Code (Time & Space Complexity)")

    def render_optimize_mode(self, skill_level: str):
        st.header("⚡ Optimize Code (Time & Space Complexity)")
        st.markdown(
            "Paste your code and I will analyze its **time & space complexity** "
            "and suggest an **optimized version**."
@@ -301,7 +296,6 @@ def render_optimize_mode(self, skill_level: str):
                if response:
                    st.success("✅ Optimization Analysis Complete!")
                    st.markdown(response)
        

    # ---------------- RUN ---------------- #

@@ -318,9 +312,9 @@ def run(self):
        elif mode == "Debug Code":
            self.render_debug_mode(skill)
        elif mode == "Optimize Code":
            self.render_optimize_mode(skill_level)

            self.render_optimize_mode(skill)


if __name__ == "__main__":
    VibeCodeEditor().run()

