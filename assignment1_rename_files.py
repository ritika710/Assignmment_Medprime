#Assignment 1
import os

def list_files_in_folder(folder_path, recursive=False):
    """List all regular files in a folder."""
    if recursive:
        # Walk through all directories and list files
        for root, _, files in os.walk(folder_path):
            for file in files:
                yield os.path.join(root, file)
    else:
        # Only list files in the given folder (non-recursive)
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                yield full_path

def rename_files(folder_path, reverse=False, preview=False):
    """Rename files sequentially, preserving extensions."""
    try:
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        # List files in folder and sort
        files = sorted(list(list_files_in_folder(folder_path)), reverse=reverse)
        if not files:
            print("The folder is empty. No files to rename.")
            return

        # Rename files
        print("Renaming files...")
        for i, file_path in enumerate(files, start=1):
            folder = os.path.dirname(file_path)
            _, ext = os.path.splitext(file_path)
            new_name = os.path.join(folder, f"{i}{ext}")

            if preview:
                print(f"File '{os.path.basename(file_path)}' will be renamed to '{os.path.basename(new_name)}'")
            else:
                try:
                    os.rename(file_path, new_name)
                    print(f"File '{os.path.basename(file_path)}' renamed to '{os.path.basename(new_name)}'")
                except PermissionError:
                    print(f"Error: Unable to rename file '{os.path.basename(file_path)}' due to permission issues.")
                except FileExistsError:
                    print(f"Error: File '{new_name}' already exists. Skipping.")

        if preview:
            print("Preview completed. No changes have been made.")
        else:
            print("Renaming completed.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    folder_path = input("Please enter the path to the folder: ").strip()
    recursive = input("Do you want to rename files in subdirectories (yes/no)? ").strip().lower() == "yes"
    reverse = input("Do you want to rename files in reverse order (yes/no)? ").strip().lower() == "yes"
    preview = input("Do you want to preview changes before renaming (yes/no)? ").strip().lower() == "yes"

    rename_files(folder_path, reverse=reverse, preview=preview)

if __name__ == "__main__":
    main()
