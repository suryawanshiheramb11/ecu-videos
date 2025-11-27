import subprocess
import os

def render_video(code_string, quality="Low"):
    """
    Saves the code to a file and runs Manim to render the video.
    Returns the path to the generated video file.
    """
    filename = "generated_scene.py"
    
    # Save the code to a file
    with open(filename, "w") as f:
        f.write(code_string)

    # Ensure LaTeX is in the PATH
    tex_path = "/Library/TeX/texbin"
    if tex_path not in os.environ["PATH"]:
        os.environ["PATH"] += f":{tex_path}"

    # Map quality to Manim flags and output folders
    quality_map = {
        "Low": ("-ql", "480p15"),
        "Medium": ("-qm", "720p30"),
        "High": ("-qh", "1080p60")
    }
    
    flag, folder_name = quality_map.get(quality, ("-ql", "480p15"))

    command = ["manim", flag, "-o", "output_video.mp4", filename, "GenScene"]

    try:
        # Run the command with the updated environment
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env=os.environ # Explicitly pass the environment
        )
        
        # Construct the expected output path
        # Manim default output structure: media/videos/{filename}/{quality_folder}/output_video.mp4
        output_path = os.path.join("media", "videos", "generated_scene", folder_name, "output_video.mp4")
        
        if os.path.exists(output_path):
            return output_path
        else:
            # Fallback: search for the file if it's not in the expected path
            for root, dirs, files in os.walk("media"):
                if "output_video.mp4" in files:
                    return os.path.join(root, "output_video.mp4")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Manim Error: {e.stderr}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
