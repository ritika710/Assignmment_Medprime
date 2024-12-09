import os
import logging
from pathlib import Path

try:
    import pyzipper
except ImportError:
    pyzipper = None
    logging.warning("pyzipper module not found. Password-protected zipping is disabled.")

def zip_folder(folder_path, zip_name=None, password=None):
    try:
        # Validate folder path
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            raise ValueError("The provided folder path is invalid or does not exist.")

        # Default zip name
        if not zip_name:
            zip_name = folder_path.name

        zip_file = folder_path.parent / f"{zip_name}.zip"

        if password and pyzipper:
            # Ensure non-empty password
            if not password.strip():
                raise ValueError("Password cannot be empty for password-protected zipping.")

            # Create password-protected zip
            with pyzipper.AESZipFile(zip_file, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
                zipf.setpassword(password.encode())  # Set password
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(folder_path)
                        zipf.write(file_path, arcname)
                logging.info(f"Password-protected zip file created at: {zip_file}")
        elif password:
            # pyzipper not installed but password provided
            raise ImportError("pyzipper is required for password-protected zipping.")
        else:
            # Create standard zip without password
            import zipfile
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(folder_path)
                        zipf.write(file_path, arcname)
                logging.info(f"Standard zip file created at: {zip_file}")

        return zip_file

    except ImportError as e:
        logging.error("Required module not available.")
        print(f"Error: {str(e)}")
    except ValueError as e:
        logging.error("Invalid input provided.")
        print(f"Error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"An error occurred: {str(e)}")

    return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # User input
    folder_path = input("Enter the path to the folder you want to zip: ").strip()
    if not folder_path:
        print("Error: Folder path cannot be empty.")
    else:
        zip_name = input("Enter custom name for the zip file (leave empty for default): ").strip() or None
        password = input("Enter a password for the zip file (leave empty for no password): ").strip()

        zip_file = zip_folder(folder_path, zip_name, password)
        if zip_file:
            print(f"Zip file successfully created: {zip_file}")
        else:
            print("Failed to create the zip file.")
