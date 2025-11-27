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

def generate_manim_code(prompt, subject_mode):
    """
    Generates Manim code using Google Gemini based on the prompt and subject mode.
    """
    model = genai.GenerativeModel('gemini-2.0-flash') # Updated to a supported model

    system_prompt = (
        "You are an expert educational animator using the Manim library. "
        f"Subject Mode: {subject_mode}. "
        "If Subject is Math: Use `MathTex` class with raw LaTeX strings (r'\\frac{d}{dx}'). "
        "If Subject is CS: Use `Square`, `VGroup`, or `Matrix` to visualize arrays/graphs. "
        "Output ONLY valid, runnable Python code. "
        "Do NOT use Markdown backticks (```). "
        "Define a class named `GenScene(Scene)`. "
        "Always import manim. "
        "Make animations smooth (use `run_time`). "
        "IMPORTANT: Do NOT pass Mobjects directly to `self.play()`. "
        "Example: `self.play(circle.animate.set_fill(RED))` instead of `self.play(circle.set_fill(RED))`."
        "Double-check your Python syntax, especially matching parentheses and brackets."
    )

    full_prompt = f"{system_prompt}\n\nUser Request: {prompt}"

    try:
        response = model.generate_content(full_prompt)
        code = sanitize_code(response.text)
        return code
    except Exception as e:
        return f"# Error generating code: {e}"
