import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    relative_path = ""
    abs_working_directory = ""
    abs_file_path = ""

    try:
        relative_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(relative_path)
        
        # Check if directory is inside permitted working directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file argument is a valid file
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

    except Exception as err:
        return f"Error: {err}"
    
    # Check if it has Python extension
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
 
    try:
        process = subprocess.run(
            args = ["python3", file_path] + args,
            timeout = 30, # 30 seconds
            capture_output = True,
            cwd = abs_working_directory,
            text = True
        )
    except Exception as err:
        return f"Error: executing Python file: {err}"

    return_string = ""
    if process.stdout == "" and process.stderr == "" and process.returncode == 0:
        return_string = "No output produced."
    else:
        return_string = f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"
        if process.returncode != 0:
            return_string += f"\nProcess exited with code {process.returncode}"
    return return_string
