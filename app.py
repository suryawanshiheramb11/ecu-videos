import streamlit as st
import generator
import renderer
import os

st.set_page_config(page_title="GenEdu: AI-Powered Math & Algo Visualizer", layout="wide")

st.title("GenEdu: AI-Powered Math & Algo Visualizer")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    subject_mode = st.selectbox(
        "Subject Mode",
        ["General", "Mathematics (LaTeX)", "Computer Science (Algorithms)"]
    )
    
    quality = st.selectbox(
        "Video Quality",
        ["Low", "Medium", "High"],
        index=0,
        help="Low: 480p (Fast), Medium: 720p, High: 1080p (Slow)"
    )
    
    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        st.warning("Please set your GOOGLE_API_KEY in the .env file.")

# Main input area
prompt = st.text_area("Enter your prompt:", height=150, placeholder="e.g., Show the chain rule derivation or Visualize Bubble Sort")

if st.button("Generate Animation"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating Manim code with Gemini..."):
            code = generator.generate_manim_code(prompt, subject_mode)
        
        if code.startswith("# Error"):
            st.error(code)
        else:
            with st.expander("Inspect Generated Logic", expanded=False):
                st.code(code, language='python')
            
            with st.spinner(f"Rendering video ({quality} quality)..."):
                video_path = renderer.render_video(code, quality)
            
            if video_path:
                st.success("Video generated successfully!")
                st.video(video_path)
            else:
                st.error("Video rendering failed. Check the console logs for details.")
