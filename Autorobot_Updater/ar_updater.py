import subprocess
import sys
import zipfile
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os

load_dotenv()
encryption_key = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(encryption_key.encode())

current_dir = os.path.dirname(__file__)

# Construct a path to the parent directory
parent_directory = os.path.join(current_dir, "..")
master_app_directory = os.path.join(parent_directory, "content")


def update_and_launch():
    # Download the new version (you can use your Update class)
    # Extract the contents to a temporary directory
    # Replace the existing executable with the new one
    patch = os.path.join(master_app_directory, cipher_suite.decrypt(os.getenv("UPDATE_SAVE_PATH").encode()).decode())
    with zipfile.ZipFile(patch, "r") as zip_ref:
        zip_ref.extractall()
    # Launch the updated application
    os.remove(patch)
    subprocess.Popen(["Autorobot.exe"])
    # print(current_dir)
    sys.exit()


if __name__ == "__main__":
    update_and_launch()
