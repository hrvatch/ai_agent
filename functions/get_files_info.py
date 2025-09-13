import os

def get_files_info(working_directory, directory="."):
    relative_path = ""
    full_path = ""
    try:
        relative_path = os.path.join(working_directory, directory)
        full_path = os.path.join(os.getcwd(), relative_path)

        abs_working_directory = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(relative_path)

        # Check if directory is inside permitted working directory
        if abs_working_directory not in abs_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # Check if directory argument is a valid directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
    except Exception as err:
        return f"Error: {err}"

    # Create a string representing the contents of the full_path directory
    try:
        dir_contents_list = os.listdir(relative_path)
        dir_contents_str = ""
        for item in dir_contents_list:
            relative_item = relative_path + "/" + item
            dir_contents_str += f"- {item}: file_size={os.path.getsize(relative_item)} bytes, is_dir={os.path.isdir(relative_item)}\n"
        return dir_contents_str
    except Exception as err:
        return f"Error {err}"

