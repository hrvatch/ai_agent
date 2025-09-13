import os
from .config import MAX_CHARS

# Function that reads file contents. File must be inside the working_directory otherwise
# don't read the file and return an error message instead
def get_file_content(working_directory, file_path):
    relative_path = ""

    # Perform the following checks first:
    # - Check if file_path is inside working_directory, if not return an error message
    # - Check if file_path is a file and it exists, if not return an error message
    try:
        relative_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(relative_path)
        
        # Check if directory is inside permitted working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file argument is a valid file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as err:
        return f"Error: {err}"

    # Read the file and return its contents as a string
    # If the file is longer than MAX_CHARS characters truncate it to the MAX_CHARS
    try:
        with open(relative_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.fstat(f.fileno()).st_size > MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as err:
        return f"Error: {err}"


