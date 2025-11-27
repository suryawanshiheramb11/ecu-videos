import streamlit as st
import generator
import renderer
import os
from dotenv import load_dotenv
import github_storage

load_dotenv()

# Set page title and layout
st.set_page_config(page_title="OnlyStudies - AI Math Visualizer", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'feedback_instruction' not in st.session_state:
    st.session_state.feedback_instruction = None
if 'last_prompt' not in st.session_state:
    st.session_state.last_prompt = None
if 'last_subject' not in st.session_state:
    st.session_state.last_subject = None
if 'last_quality' not in st.session_state:
    st.session_state.last_quality = None

# --- THEME MANAGEMENT ---
def set_ui_theme(theme_name):
    """
    Sets the UI theme in .streamlit/config.toml and reruns if changed.
    theme_name: "light" or "dark"
    """
    config_dir = ".streamlit"
    config_path = f"{config_dir}/config.toml"
    
    # Ensure directory exists to prevent errors
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    content = ""
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            content = f.read()
    
    current_is_dark = 'base = "dark"' in content
    target_is_dark = theme_name == "dark"
    
    # If the file exists and theme matches, do nothing
    if current_is_dark == target_is_dark and os.path.exists(config_path):
        return 

    if target_is_dark:
        # NOTE: Updated backgroundColor to #030616 (RGB: 3, 6, 22)
        new_theme = """[theme]
                    base = "dark"
                    primaryColor = "#4F46E5"
                    backgroundColor = "#030616"
                    secondaryBackgroundColor = "#0F172A"
                    textColor = "#F8FAFC"
                    """
    else:
        # OnlyStudies Light Theme (White/Slate-50 + Indigo-600)
        new_theme = """[theme]
                    base = "light"
                    primaryColor = "#4F46E5"
                    backgroundColor = "#FFFFFF"
                    secondaryBackgroundColor = "#F8FAFC"
                    textColor = "#0F172A"
                    """
    
    with open(config_path, "w") as f:
        f.write(new_theme)
    
    st.rerun()

def apply_custom_css():
    st.markdown("""
        <style>
        /* OnlyStudies Custom CSS */
        
        /* Buttons */
        .stButton > button {
            border-radius: 0.75rem;
            font-weight: 600;
            border: none;
            transition: all 0.2s ease;
        }
        
        /* Primary Button Style (Indigo) */
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06);
        }

        /* Inputs */
        .stTextArea > div > div > textarea {
            border-radius: 0.75rem;
            border-color: #E2E8F0;
        }
        
        /* Dark Mode Specifics for Text Areas */
        [data-theme="dark"] .stTextArea > div > div > textarea {
            background-color: #0F172A;
            border-color: #1E293B;
            color: #F8FAFC;
        }
        
        /* Sidebar Border */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(148, 163, 184, 0.1);
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.025em;
        }
        
        /* --- BACKGROUND COLOR SETTINGS --- */
        /* NOTE: Setting the main app background to #030616 (RGB 3, 6, 22) */
        .stApp {
            background-color: #030616 !important;
        }

        /* NOTE: I have commented out the gradients below. 
           If you leave them enabled, they will look like a purple haze 
           over your specific background color. Keeping them OFF ensures 
           the exact RGB(3, 6, 22) is visible. */
        
        /*
        [data-theme="dark"] .stApp {
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(79, 70, 229, 0.08) 0%, transparent 25%),
                radial-gradient(circle at 80% 40%, rgba(168, 85, 247, 0.08) 0%, transparent 25%);
            background-attachment: fixed;
        }
        */
        </style>
    """, unsafe_allow_html=True)

# Apply CSS immediately
apply_custom_css()

# Check for Theme Query Parameter (Sync with Frontend)
if "theme" in st.query_params:
    target_theme = st.query_params["theme"]
    if target_theme in ["light", "dark"]:
        set_ui_theme(target_theme)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    # Check for User Login (Mock Auth)
    if "user" in st.query_params:
        user_name = st.query_params["user"]
        st.success(f"👋 Welcome, {user_name}!")
        st.divider()

    st.header("Configuration")
    subject_mode = st.selectbox(
        "Subject Mode", 
        ["General", "Mathematics (LaTeX)", "Computer Science (Algorithms)", "Geometry", "Logic Puzzles"]
    )
    quality = st.selectbox("Video Quality", ["Low", "Medium", "High"], index=0)
    video_theme = st.selectbox("Video Theme", ["Dark", "Light"], index=0)
    voice_style = st.selectbox("Voice Style", ["American (Default)", "British", "Australian", "Indian"], index=0)
    
    st.divider()
    
    # UI Theme Toggle
    if st.button("🌗 Toggle UI Theme"):
        config_path = ".streamlit/config.toml"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                is_dark = 'base = "dark"' in f.read()
            set_ui_theme("light" if is_dark else "dark")
        else:
            # Default to creating dark mode if config doesn't exist
            set_ui_theme("dark")

    st.divider()
    with st.expander("How to Use"):
        st.markdown("""
        1. **Select Mode**: Choose Math for equations, CS for code/graphs, Geometry for shapes.
        2. **Select Theme**: Dark is classic, Light is good for printing/slides.
        3. **Enter Prompt**: Be specific! (e.g., "Prove Pythagoras Theorem").
        4. **Generate**: Click the button.
        5. **Refine**: Use Thumbs Up/Down to guide the AI.
        """)

# --- MAIN INPUT SECTION ---
st.title("OnlyStudies")
st.markdown("### Turn Text into Perfect Math Lessons")
st.caption("Generate professional Python Manim animations with AI voiceovers in seconds.")

with st.form("generation_form"):
    prompt = st.text_area("Enter your topic:", height=100, placeholder="e.g., 'Explain Pythagorean Theorem', 'Bubble Sort Visualization'")
    generate_btn = st.form_submit_button("Generate Animation")

# --- GENERATION LOGIC ---
if generate_btn and prompt:
    # Save state variables for regeneration
    st.session_state.feedback_instruction = None 
    st.session_state.last_prompt = prompt 
    st.session_state.last_subject = subject_mode
    st.session_state.last_quality = quality
    st.session_state.last_theme = video_theme
    st.session_state.last_voice = voice_style

    with st.spinner("Generating Manim code with Gemini..."):
        code = generator.generate_manim_code(prompt, subject_mode, video_theme=video_theme, voice_style=voice_style)
        st.session_state.generated_code = code
    
    with st.expander("Inspect Generated Logic", expanded=False):
        st.code(code, language='python')
    
    with st.spinner(f"Rendering video ({quality} quality)..."):
        video_path, error_message = renderer.render_video(code, quality)
    
    if error_message:
        # Silent Error Recovery: Try to fix code once
        with st.spinner("Refining animation logic..."):
            fixed_code = generator.fix_manim_code(code, error_message)
            st.session_state.generated_code = fixed_code 
        
        with st.spinner(f"Finalizing video ({quality} quality)..."):
            video_path, error_message = renderer.render_video(fixed_code, quality)

    if video_path:
        # Upload to GitHub
        try:
            with st.spinner("Uploading to GitHub..."):
                repo_name = os.getenv("GITHUB_REPO")
                if not repo_name:
                    st.error("GITHUB_REPO not set in .env")
                else:
                    github_url = github_storage.upload_video(video_path, repo_name)
                    st.session_state.video_path = github_url
        except Exception as e:
            st.error(f"Failed to upload to GitHub: {e}")
            # Fallback to local path if upload fails (though Render won't persist it)
            st.session_state.video_path = video_path
    else:
        st.error(f"Video rendering failed after retry. Error: {error_message}")
        st.session_state.video_path = None

# --- DISPLAY SECTION (PERSISTENT) ---
if st.session_state.video_path:
    st.success("Video generated successfully!")
    st.video(st.session_state.video_path)
    
    # Feedback UI
    st.divider()
    st.subheader("Feedback & Refinement")
    
    col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 2])
    
    with col_fb1:
        if st.button("👍 Good"):
            st.session_state.feedback_instruction = None
            st.toast("Thanks! We'll keep this style.")
            
    with col_fb2:
        if st.button("👎 Bad"):
            st.session_state.feedback_instruction = "The user disliked the previous output. Try a COMPLETELY DIFFERENT visual style, layout, and color scheme."
            st.toast("Noted. Next attempt will be different.")
            
    with col_fb3:
        if st.button("🔄 Regenerate"):
            pass # Trigger logic is handled below

# --- REGENERATION LOGIC (OUTSIDE FORM) ---
# Handles both "Regenerate" button inside feedback and the general need to re-run
if st.session_state.get('video_path') and (st.button("🔄 Regenerate Video", key="regen_main") or (st.session_state.get('feedback_instruction') is not None and st.button("Regenerate with Feedback", key="regen_with_feedback"))):
    if st.session_state.get('last_prompt'):
        prompt_for_regen = st.session_state.last_prompt
        subject_for_regen = st.session_state.last_subject
        quality_for_regen = st.session_state.last_quality
        theme_for_regen = st.session_state.get('last_theme', 'Dark')
        feedback_for_regen = st.session_state.feedback_instruction
        
        with st.spinner(f"Regenerating... (Feedback: {'Yes' if feedback_for_regen else 'None'})"):
            code = generator.generate_manim_code(prompt_for_regen, subject_for_regen, feedback_for_regen, video_theme=theme_for_regen)
            st.session_state.generated_code = code
            
            video_path, error_message = renderer.render_video(code, quality_for_regen)
            
            if error_message:
                 st.warning(f"Regeneration rendering failed: {error_message}. Attempting to fix code...")
                 fixed_code = generator.fix_manim_code(code, error_message)
                 st.session_state.generated_code = fixed_code
                 video_path, error_message = renderer.render_video(fixed_code, quality_for_regen)
            
            if video_path:
                # Upload to GitHub
                try:
                    with st.spinner("Uploading to GitHub..."):
                        repo_name = os.getenv("GITHUB_REPO")
                        if not repo_name:
                            st.error("GITHUB_REPO not set in .env")
                        else:
                            github_url = github_storage.upload_video(video_path, repo_name)
                            st.session_state.video_path = github_url
                except Exception as e:
                    st.error(f"Failed to upload to GitHub: {e}")
                    st.session_state.video_path = video_path

                st.session_state.feedback_instruction = None # Reset feedback after use
                st.rerun() 
            else:
                st.error(f"Regeneration failed: {error_message}")
    else:
        st.warning("No previous prompt found to regenerate. Please generate an animation first.")

