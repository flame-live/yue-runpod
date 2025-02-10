import os
import base64
import runpod
import torch
import tempfile
from pathlib import Path
import torchaudio
from huggingface_hub import login

def save_base64_audio(b64_string, output_path):
    audio_bytes = base64.b64decode(b64_string)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

def audio_to_base64(audio_path):
    with open(audio_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def write_text_file(content, file_path):
    with open(file_path, 'w') as f:
        f.write(content)

def handler(event):
    try:
        # Setup HF token if provided
        if "HF_TOKEN" in os.environ:
            login(os.environ["HF_TOKEN"])
            stage1_model = os.environ.get("STAGE1_MODEL", "m-a-p/YuE-s1-7B-anneal-en-cot")
            stage2_model = os.environ.get("STAGE2_MODEL", "m-a-p/YuE-s2-1B-general")
        else:
            # Fallback to public models or raise error
            raise ValueError("HF_TOKEN environment variable is required")

        # Create temp directory for this run
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract inputs
            input_data = event["input"]
            
            # Required inputs
            genre_text = input_data["genre"]
            lyrics_text = input_data["lyrics"]
            
            # Write text inputs to files
            genre_path = os.path.join(temp_dir, "genre.txt")
            lyrics_path = os.path.join(temp_dir, "lyrics.txt")
            write_text_file(genre_text, genre_path)
            write_text_file(lyrics_text, lyrics_path)
            
            # Handle optional audio prompt
            audio_args = []
            if "audio_prompt" in input_data:
                audio_path = os.path.join(temp_dir, "prompt.mp3")
                save_base64_audio(input_data["audio_prompt"], audio_path)
                audio_args = [
                    "--use_audio_prompt",
                    "--audio_prompt_path", audio_path,
                    "--prompt_start_time", str(input_data.get("start_time", 0)),
                    "--prompt_end_time", str(input_data.get("end_time", 30))
                ]
            
            # Set up output directory
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            # Run inference
            cmd_args = [
                "--cuda_idx", "0",
                "--stage1_model", stage1_model,
                "--stage2_model", stage2_model,
                "--genre_txt", genre_path,
                "--lyrics_txt", lyrics_path,
                "--run_n_segments", str(input_data.get("segments", 2)),
                "--stage2_batch_size", str(input_data.get("batch_size", 4)),
                "--output_dir", output_dir,
                "--max_new_tokens", str(input_data.get("max_tokens", 3000)),
                "--repetition_penalty", str(input_data.get("repetition_penalty", 1.1))
            ] + audio_args

            # Import and run inference
            import infer
            infer.main(cmd_args)

            # Get output files
            output_files = {}
            for root, _, files in os.walk(output_dir):
                for f in files:
                    if f.endswith(('.mp3', '.wav')):
                        path = os.path.join(root, f)
                        output_files[f] = audio_to_base64(path)

            return {
                "output": output_files
            }

    except Exception as e:
        return {"error": str(e)}

runpod.serverless.start({"handler": handler}) 