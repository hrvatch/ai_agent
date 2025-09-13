import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    test_run_python_file()

def test_run_python_file():
    test_items = [
        ["calculator", "main.py"],
        ["calculator", "main.py", ["3 + 5"]],
        ["calculator", "tests.py"],
        ["calculator", "../main.py"],
        ["calculator", "nonexistent.py"],
        ["calculator", "lorem.txt"]
    ]
    for item in test_items:
        print(run_python_file(*item))

def test_file_write():
    test_items = [
        ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
        ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["calculator", "/tmp/temp.txt", "this should not be allowed"]
    ]

    for item in test_items:
        print(write_file(*item))

def test_file_content():
    test_items = [
        ["calculator", "main.py"],
        ["calculator", "pkg/calculator.py"],
        ["calculator", "/bin/cat"],
        ["calculator", "pkg/does_not_exist.py"]
    ]

    #content = get_file_content("calculator", "lorem.txt")
    for item in test_items:
        print(get_file_content(*item))


def test_files_info():
    test_items = [
        (
            ["calculator", "."], 
            (
                "- main.py: file_size=719 bytes, is_dir=False\n" 
                "- pkg: file_size=44 bytes, is_dir=True\n"
                "- tests.py: file_size=1331 bytes, is_dir=False\n" 
             ),
            ["main.py", "pkg", "tests.py"]
        ),
        (
            ["calculator", "pkg"],
            (
                "- calculator.py: file_size=1721 bytes, is_dir=False\n"
                "- render.py: file_size=376 bytes, is_dir=False\n"
            ),
            ["calculator.py", "render.py"]
        ),
        (
            ["calculator", "/bin"],
            'Error: Cannot list "/bin" as it is outside the permitted working directory',
            ['Error: Cannot list "/bin" as it is outside the permitted working directory']
        ),
        (
            ["calculator", "../"],
            'Error: Cannot list "../" as it is outside the permitted working directory',
            ['Error: Cannot list "../" as it is outside the permitted working directory']
        )
    ]
    
    for item in test_items:
        passfail = True
        print("="*50)
        print(f'Calling get_files_info("{item[0][0]}", "{item[0][1]}")')
        expected = item[1]
        print(f"Expected:\n{expected}")
        actual = get_files_info(*item[0])
        print(f"Actual:\n{actual}")
        for must_be_present in item[2]:
            if must_be_present not in actual:
                passfail = False
                break
        if passfail:
            print("PASS")
        else:
            print("FAIL")

def run_files_info():
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))

main()
