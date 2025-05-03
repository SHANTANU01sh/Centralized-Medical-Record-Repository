import os
from datetime import datetime

UPLOAD_DIR = "uploads"

CATEGORIES = ["lab_results", "mri_scans", "clinical_notes"]

def save_uploaded_file(username, category, uploaded_file):
    # Ensure upload path exists
    user_path = os.path.join(UPLOAD_DIR, username, category)
    os.makedirs(user_path, exist_ok=True)

    # Timestamped filename to avoid collisions
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(user_path, filename)

    # Save file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath
