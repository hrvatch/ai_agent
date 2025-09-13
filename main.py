import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Main function
def main():
    options = {}
    options["verbose"] = False

    # Check input arguments
    if len(sys.argv) <= 1:
        print(INVALID_ARGS_MESSAGE)
        sys.exit(1)
    
    # Load .env and get the API key from the GEMINI_API_KEY environment variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key == "":
        print("Invalid API key! Check if GEMINI_API_KEY environment variable is set!")
        sys.exit(1)
    options["api_key"] = api_key

    # Parse the arguments
    # 1. Remove the first argument (file name)
    # 2. Create a list of -- arguments
    # 3. Parse rest of the arguments and assume those are user prompts
    cmdline_args = sys.argv[1:]
    cmdline_options = list(filter(lambda s: len(s) > 2 and s[0:2] == "--", cmdline_args))
    cmdline_prompts = list(filter(lambda s: not (len(s) > 2 and s[0:2] == "--"), cmdline_args))

    # We shouldn't have more than one prompt
    if len(cmdline_prompts) > 1:
        print("More than one prompt given!")
        for prompt in cmdline_prompts:
            print(f"  {prompt}")
        sys.exit(1)
    
    # Create list of options. If invalid argument (options) is passed, display an error message and exit
    for option in cmdline_options:
        if option == "--verbose":
            options["verbose"] = True
        else:
            print(f"Invalid argument: {option}")
            sys.exit(1)
    
    options["prompt"] = cmdline_prompts[0]

    # Send the user prompt to the LLM
    llm_give_prompt_generate_response(options)   

# Calls function requested by the LLM
def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    response = {}
    match function_call_part.name:
        case "get_files_info":
            response["result"] = get_files_info("./calculator", **function_call_part.args)
        case "get_file_content":
            response["result"] = get_file_content("./calculator", **function_call_part.args)
        case "write_file":
            response["result"] = write_file("./calculator", **function_call_part.args)
        case "run_python_file":
            response["result"] = run_python_file("./calculator", **function_call_part.args)
        case _:
            # Invalid function name/non-existent function
            response["error"] = f"Unknown function: {function_name}"

    # Return types.Content with a from_function_response describing the result of the function call:
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=response,
            )
        ],
    )

def llm_give_prompt_generate_response(options):
    api_key = ""
    user_prompt = ""
    verbose = False

    if "api_key" in options:
        api_key = options["api_key"]
    if api_key == "":
        print("Empty api_key!")
        return

    if "prompt" in options:
        user_prompt = options["prompt"]
    
    if user_prompt == "":
        print("Empty user prompt!")
        return

    if "verbose" in options:
        verbose = options["verbose"]

    # Create new instance of gemini client
    client = genai.Client(api_key=api_key)

    # How does an LLM actually call a function?
    # Well the answer is that... it doesn't. At least not directly. It works like this:
    # 1. We tell the LLM which functions are available to it
    # 2. We give it a prompt
    # 3. It describes which function it wants to call, and what arguments to pass to it
    # 4. We call that function with the arguments it provided
    # 5. We return the result to the LLM
    # 
    # We're using the LLM as a decision-making engine, but we're still the ones running the code.
    #
    # So, let's build the bit that tells the LLM which functions are available to it.
    # We are using types.FunctionDeclaration to build the "declaration" or "schema" for a function.
    
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description=(
            "Reads content of a file. If file is larger then 10000 bytes, the output is constrained"
            "10000 bytes. After truncating a string is appended to the output to inform about the"
            "content truncation. Reading of a file is constrained to the working directory."),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to read contents from, relative to the working directory.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description=(
            "Writes content to a file. If writing was succesfull it will return a message containing file path"
            "and number of characters written. Writing to a file is constrained to the working directory."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write contents to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content that will be written to a file."
                ),
            },
        ),
    )
    
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description=(
            "Runs (executes) a Python file. File execution is limited to"
            "the files located in the working directory. Function returns text written to the stdout and "
            "stderr by the Python file that was executed. Run time is limited to 30 seconds."
            "Additional running arguments can be specified, but this is optional."
            "If no additional arguments are specified, Python file will be executed without additional arguments."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The name of the Python file that function will run."
                ),
                "args": types.Schema(
                    type=types.Type.STRING,
                    description="Optional list of arguments that will be passed to the Python file."
                ),
            },
        ),
    )

    # Using the types.Tool to create a list of all available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    # Store responses as a list of messages
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # Generate response from the command line argument as a content
    system_prompt = SYSTEM_PROMPT
    if verbose:
        print(f"System prompt: {system_prompt}")
        print(f"User prompt: {user_prompt}")
    
    loop_cnt = 0
    while (loop_cnt < 20):
        loop_cnt += 1
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)

        for candidate in response.candidates:
            messages.append(candidate.content)

        # The types.Content that we return from call_function should have a .parts[0].function_response.response within.
        # If it doesn't, raise a fatal exception of some sort.
        # If it does, and verbose was set, print the result of the function call like this:

        if response.function_calls != None and len(response.function_calls) > 0:
            for call in response.function_calls:
                function_call_result = call_function(call, verbose)
                valid_result = False

                if function_call_result != None and function_call_result.parts[0] != None:
                    if function_call_result.parts[0].function_response != None:
                        if function_call_result.parts[0].function_response.response != None:
                            valid_result = True
                            function_call_result.role = "user"
                            messages.append(function_call_result)
                            if verbose:
                                print(f"-> {function_call_result.parts[0].function_response.response}")

                if not valid_result:
                    raise Exception("Invalid function call result!")
        else:
            print(response.text)
            break

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
