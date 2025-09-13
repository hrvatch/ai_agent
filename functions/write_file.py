import os

def write_file(working_directory, file_path, content):
    try:
        relative_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(relative_path)
        
        # Check if directory is inside permitted working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check path exists, if not create it
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path))

        with open(relative_path, "w") as f:
            f.write(content)

    except Exception as err:
        return f"Error: {err}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
