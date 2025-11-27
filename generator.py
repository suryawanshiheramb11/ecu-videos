import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def sanitize_code(code_string):
    """Removes markdown code block delimiters."""
    code_string = code_string.replace("```python", "").replace("```", "")
    return code_string.strip()

def generate_manim_code(prompt, subject_mode, feedback_instruction=None, video_theme="Dark", voice_style="American (Default)"):
    """
    Generates Manim code using Gemini based on the user's prompt and configuration.
    """
    model = genai.GenerativeModel('gemini-2.0-flash') # Updated to a supported model

    # Voice Style Logic (gTTS TLDs)
    tld = 'com' # Default US
    if voice_style == "British":
        tld = 'co.uk'
    elif voice_style == "Australian":
        tld = 'com.au'
    elif voice_style == "Indian":
        tld = 'co.in'

    # Theme Logic
    theme_instruction = ""
    if video_theme == "Light":
        theme_instruction = (
            "   - **THEME**: Light Mode. You MUST set `config.background_color = WHITE` in `construct`.\n"
            "   - **Colors**: Use `BLACK` or dark colors (e.g., `DARK_BLUE`, `DARK_GREY`) for all Text, MathTex, and Lines. Do NOT use White or Yellow on a White background.\n"
        )
    else:
        theme_instruction = (
            "   - **THEME**: Dark Mode (Default). Background is Black.\n"
            "   - **Colors**: Use `WHITE`, `YELLOW`, `BLUE`, `TEAL` for high contrast.\n"
        )

    # Subject Specific Instructions
    subject_instruction = ""
    if subject_mode == "Mathematics (LaTeX)":
        subject_instruction = "Use `MathTex` class with raw LaTeX strings (r'\\frac{d}{dx}'). Focus on derivations."
    elif subject_mode == "Computer Science (Algorithms)":
        subject_instruction = (
            "**VISUAL STYLE (The 'Perfect Teacher' Look)**:\n"
            "   - **Arrays**: Use `Square` or `Rectangle` objects arranged linearly. Put values inside.\n"
            "   - **Graphs**: Use `Circle` for nodes and `Line` for edges.\n"
            "   - **Matrices/DP**: Use `VGroup` of squares.\n"
            "   - **Color Coding** (Mandatory):\n"
            "       - `BLUE`/`WHITE`: Default state.\n"
            "       - `YELLOW`: 'Looking at' or 'Comparing' (Active state).\n"
            "       - `GREEN`: 'Sorted', 'Confirmed', or 'Found' (Final state).\n"
            "       - `RED`: 'Mismatch' or 'Swapping' (Action state).\n"
            "   - **Narrative**: \n"
            "       1. **Setup**: Initialize data structure. Title at top.\n"
            "       2. **Logic**: Step-by-step. Highlight items `YELLOW` when comparing. Wait 0.5s. Change color based on result. If swapping, use `CyclicReplace` or smooth `MoveTo`.\n"
            "       3. **Completion**: Turn the whole structure `GREEN`."
        )
    elif subject_mode == "Geometry":
        subject_instruction = (
            "**VISUAL STYLE (The 'Draftsman' Look)**:\n"
            "   - **Tools**: You MUST visualize the drawing process. \n"
            "       - Create a 'Ruler' (long thin Rectangle) for drawing lines.\n"
            "       - Create a 'Compass' (VGroup of lines/dots) for drawing circles/arcs.\n"
            "   - **Animation**: \n"
            "       - Move the Ruler to the start point -> Rotate it to alignment -> Animate Ruler moving along the path while `Create(line)` plays.\n"
            "       - Move Compass to center -> Animate rotation while `Create(circle)` plays.\n"
            "   - **Precision**: Use `RightAngle`, `Brace`, and `DecimalNumber` for measurements.\n"
            "   - **Construction**: Step-by-step. Draw line, then arc, then intersection."
        )
    elif subject_mode == "Logic Puzzles":
        subject_instruction = (
            "Use `NumberPlane`, `Grid`, or `Table` to organize information. "
            "Visualize logical steps clearly. Use `SurroundingRectangle` to highlight focus areas."
        )
    else:
        subject_instruction = "General educational animation."

    system_prompt = (
        "You are an expert educational animator using the Manim library. "
        f"Subject Mode: {subject_mode}. {subject_instruction}\n"
        "Output ONLY valid, runnable Python code. "
        "Do NOT use Markdown backticks (```). "
        "Define a class named `GenScene(Scene)`. "
        "Always import manim. "
        "Make animations smooth (use `run_time`). "
        "IMPORTANT: Do NOT pass Mobjects directly to `self.play()`. "
        "Example: `self.play(circle.animate.set_fill(RED))` instead of `self.play(circle.set_fill(RED))`."
        "Double-check your Python syntax, especially matching parentheses and brackets.\n"
        "For `RightAngle`, use `RightAngle(line1, line2, length=0.2)`. \n"
        "   - **CRITICAL**: `line1` and `line2` MUST be `Line` Mobjects. Do NOT pass coordinates (numpy arrays) or points.\n"
        "   - If using a `Polygon`, do NOT try to access `.lines`. Instead, create separate `Line` objects for the sides you need.\n"
        "   - **Vector Safety**: ALL vectors for `shift`, `move_to`, `next_to` MUST be 3D (e.g., `[1, 2, 0]` or `RIGHT * 2`). NEVER use 2D vectors like `[1, 2]`.\n\n"
        
        "CRITICAL REQUIREMENTS FOR HIGH QUALITY:\n"
        f"1. **Voiceover**: You MUST use `manim_voiceover`. Import `VoiceoverScene` from `manim_voiceover` and `GTTSService` from `manim_voiceover.services.gtts`. Inherit from `VoiceoverScene` instead of `Scene`. Initialize `self.set_speech_service(GTTSService(lang='en', tld='{tld}'))` in `construct`. Wrap animations in `with self.voiceover(text='...') as tracker:` blocks. Ensure `run_time` of animations inside the block is either omitted (to match audio) or set to `tracker.duration`.\n"
        "2. **Duration (STRICT)**: The animation MUST be at least 60 seconds long. \n"
        "   - **EXPAND THE TOPIC**: If the request is simple, you MUST add examples, detailed breakdowns, or slow-paced explanations to fill the time.\n"
        "   - Use `self.wait(2)` or `self.wait(3)` frequently to let the viewer process information.\n"
        "   - **NEVER** produce a short 10-second clip. It WILL be rejected.\n"
        "3. **Captions (CLEAN STYLE)**: \n"
        "   - **NO BOX**: Do NOT create a background rectangle for captions.\n"
        "   - **Style**: Use `Text(..., font_size=32, stroke_width=2, stroke_color=BLACK)`. The stroke ensures readability on any background.\n"
        "   - **Position**: Fix the text at the VERY BOTTOM (`.to_edge(DOWN, buff=0.5)`).\n"
        "   - **Update**: Update this text synchronously with animations using `Transform`.\n"
        "4. **Alignment & Layout**: \n"
        "   - Create a `main_content` VGroup for the primary animation elements.\n"
        "   - Always center `main_content` using `.move_to(ORIGIN)` or `.arrange(DOWN, center=True)`.\n"
        "   - **CRITICAL**: Shift `main_content` UP (`.shift(UP * 1)`) to avoid the bottom caption area.\n"
        "   - **Text Visibility**: Use `.scale_to_fit_width(config.frame_width - 2)` for large text blocks.\n"
        "   - Use `VGroup` to keep related objects together.\n"
        "5. **Professional Styling**: \n"
        f"{theme_instruction}"
        "   - Use `Text` with a clean font (e.g., sans-serif) for explanations.\n"
        "   - Ensure text is readable (not too small, not overlapping).\n"
        "6. **Depth**: Explain the 'Why' and 'How', not just the 'What'. For algorithms, show variables updating. For math, show intermediate steps.\n"
        "7. **Geometry Best Practices**: \n"
        "   - **Positioning**: Shift the main geometric figure to the LEFT (`.shift(LEFT * 2)`) to create space for text on the right.\n"
        "   - **Construction**: When adding shapes to edges (e.g., squares on a triangle), use the edge's normal vector to ensure they point OUTWARD.\n"
        "   - **Layering**: Always set `z_index` of Text/MathTex higher than shapes (e.g., `text.set_z_index(10)`). Use `fill_opacity=0.5` for shapes to keep background visible.\n"
        "   - **Labels**: Shift labels slightly away from edges (`.next_to(..., buff=0.2)`) to prevent overlapping.\n"
        "   - **Alignment**: Ensure start and end states are perfectly aligned. Use `Transform` to morph shapes without jumping."
    )

    full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"
    
    if feedback_instruction:
        full_prompt += f"\n\nFEEDBACK FROM PREVIOUS ATTEMPT: {feedback_instruction}"

    try:
        response = model.generate_content(full_prompt)
        code = sanitize_code(response.text)
        return code
    except Exception as e:
        return f"# Error generating code: {e}"

def fix_manim_code(code, error_message):
    """
    Asks Gemini to fix the provided Manim code based on the error message.
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = (
        "You are an expert Manim developer. The following code generated an error.\n\n"
        f"CODE:\n```python\n{code}\n```\n\n"
        f"ERROR:\n{error_message}\n\n"
        "Please fix the code to resolve the error. "
        "Output ONLY the fixed, valid, runnable Python code. "
        "Do NOT use Markdown backticks."
    )
    
    try:
        response = model.generate_content(prompt)
        fixed_code = sanitize_code(response.text)
        return fixed_code
    except Exception as e:
        return f"# Error fixing code: {e}"
