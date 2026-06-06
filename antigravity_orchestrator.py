import os
import json
import time
import subprocess
import platform

# ==============================================================================
# 🛠️ CONFIGURATION: Set your Google Drive and project paths
# ==============================================================================

# By default, this script attempts to auto-detect your local Google Drive Desktop sync path.
# If the auto-detection does not match your system, replace the path below with your absolute path.
GOOGLE_DRIVE_PATH = "/Users/dr3/Library/CloudStorage/GoogleDrive-romerodeab@gmail.com/My Drive"

# The relative path from "My Drive" to your Agent Dropzone folder.
DROPZONE_RELATIVE_PATH = os.path.join("Work", "Agent Dropzone")

# Supported audio extensions for voice notes
AUDIO_EXTENSIONS = [".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac"]

# ==============================================================================
# Helper function to detect local Google Drive paths across OS platforms
# ==============================================================================
def detect_google_drive_path():
    if GOOGLE_DRIVE_PATH:
        return GOOGLE_DRIVE_PATH
    
    system = platform.system()
    home = os.path.expanduser("~")
    
    if system == "Windows":
        # Check G: (default sync drive for Google Drive Desktop)
        for drive in ["G", "H", "I", "F"]:
            path = f"{drive}:\\My Drive"
            if os.path.exists(path):
                return path
        path = os.path.join(home, "Google Drive", "My Drive")
        if os.path.exists(path):
            return path
            
    elif system == "Darwin": # macOS
        # macOS CloudStorage default
        cloud_storage = os.path.join(home, "Library", "CloudStorage")
        if os.path.exists(cloud_storage):
            for folder in os.listdir(cloud_storage):
                if folder.startswith("GoogleDrive-"):
                    path = os.path.join(cloud_storage, folder, "My Drive")
                    if os.path.exists(path):
                        return path
        path = os.path.join(home, "Google Drive", "My Drive")
        if os.path.exists(path):
            return path
            
    elif system == "Linux":
        path = os.path.join(home, "GoogleDrive", "My Drive")
        if os.path.exists(path):
            return path
            
    return None

# ==============================================================================
# Local Audio Transcription using Whisper
# ==============================================================================
def transcribe_audio(audio_path):
    try:
        import whisper
        print("🎙️ Loading Whisper model ('tiny' for high speed and low memory)...")
        # 'tiny' is recommended for rapid, lightweight local operations.
        # It will automatically download on your first run.
        model = whisper.load_model("tiny")
        print("🎙️ Transcribing audio file...")
        result = model.transcribe(audio_path)
        return result.get("text", "").strip()
    except ImportError:
        print("\n❌ Error: The 'openai-whisper' library is not installed.")
        print("   To enable voice-note transcription, run this in your Antigravity terminal:")
        print("   👉 pip install openai-whisper")
        return None
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None

def execute_tasks(task_package):
    package = task_package.get("agent_task_package", {})
    batch_id = package.get("batch_id", "unknown")
    priority = package.get("priority", "normal")
    tasks = package.get("tasks", [])
    
    print(f"\n🚀 [Batch {batch_id}] Processing {len(tasks)} tasks (Priority: {priority})...")
    
    for task in tasks:
        task_id = task.get("task_id", 0)
        task_type = task.get("type", "unknown")
        project = task.get("target_project", "")
        desc = task.get("description", "")
        steps = task.get("instructions", [])
        
        print(f"\n📌 Task #{task_id} [{task_type}] - Project: {project}")
        print(f"   Description: {desc}")
        print(f"   Executing {len(steps)} steps:")
        
        for step in steps:
            print(f"   👉 {step}")
            # If standard shell command execution is enabled:
            subprocess.run(step, shell=True)
            time.sleep(1) # Simulate execution delay
            
    print(f"\n✅ Batch {batch_id} completed successfully.")

def monitor_dropzone():
    drive_path = detect_google_drive_path()
    if not drive_path:
        print("❌ Error: Local Google Drive path could not be detected automatically.")
        print("   Please manually set the GOOGLE_DRIVE_PATH variable at the top of this script.")
        return
        
    dropzone_path = os.path.join(drive_path, DROPZONE_RELATIVE_PATH)
    print(f"✨ Google Antigravity Orchestrator 2.0 active.")
    print(f"📁 Monitoring local sync folder: {dropzone_path}")
    print("⏳ Waiting for audio notes or task files...")
    # Play a startup ping sound so the user knows the terminal is active and listening
    try:
        import subprocess
        subprocess.run("afplay /System/Library/Sounds/Glass.aiff", shell=True)
    except:
        pass
    
    while True:
        try:
            # 1. Scan for raw audio files to transcribe
            for file in os.listdir(dropzone_path):
                name, ext = os.path.splitext(file)
                if ext.lower() in AUDIO_EXTENSIONS and "_processed" not in name:
                    audio_file_path = os.path.join(dropzone_path, file)
                    print(f"\n🎙️ Found new raw audio file: {file}")
                    
                    # Transcribe the audio locally
                    transcript_text = transcribe_audio(audio_file_path)
                    
                    if transcript_text:
                        print(f"📝 Transcription complete: \"{transcript_text[:100]}...\"")
                        
                        # Save transcript as a text file
                        transcript_file_name = f"{name}_transcription.txt"
                        transcript_file_path = os.path.join(dropzone_path, transcript_file_name)
                        with open(transcript_file_path, "w", encoding="utf-8") as f:
                            f.write(transcript_text)
                        print(f"💾 Transcription text saved to: {transcript_file_name}")
                        
                        # Archive the audio file so we don't re-transcribe it
                        archive_name = f"{name}_processed{ext}"
                        os.rename(audio_file_path, os.path.join(dropzone_path, archive_name))
                        print(f"📦 Audio file archived to: {archive_name}")
            
            # 2. Scan for pending task files to execute
            for file in os.listdir(dropzone_path):
                if file.endswith('.json') and not file.startswith('instructions_processed') and not file.startswith('instructions_failed') and not file.startswith('instructions_template') and not file.startswith('instructions_old') and file != 'test_template.txt':
                    task_file_path = os.path.join(dropzone_path, file)
                    print(f"\n🔔 Found new JSON instructions file: {file}")
                    try:
                        with open(task_file_path, "r", encoding="utf-8") as f:
                            task_package = json.load(f)
                        
                        # Execute tasks
                        execute_tasks(task_package)
                        
                        # Archive the processed task file
                        archive_name = f"instructions_processed_{int(time.time())}_{file}"
                        archive_path = os.path.join(dropzone_path, archive_name)
                        os.rename(task_file_path, archive_path)
                        print(f"📦 Task file archived to: {archive_name}")
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON Parse Error in {file}: {e}")
                        # Archive as failed so we don't infinite loop
                        archive_name = f"instructions_failed_{int(time.time())}_{file}"
                        archive_path = os.path.join(dropzone_path, archive_name)
                        os.rename(task_file_path, archive_path)
                        print(f"📦 Bad task file archived to: {archive_name}")
                
        except Exception as e:
            print(f"❌ Error during loop execution: {e}")
            
        time.sleep(5) # Poll every 5 seconds

if __name__ == "__main__":
    try:
        monitor_dropzone()
    except KeyboardInterrupt:
        print("\n👋 Orchestrator stopped.")