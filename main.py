from LLMModel import LLMModel
from CodeBaseProcessor import CodeBaseProcessor
from utils import Prompt, get_user_choice, DIVIDE


def main():

    DIVIDE("Initialization", "=")
    prompt = Prompt()
    codebase = CodeBaseProcessor('root')
    llm = LLMModel()
    DIVIDE()

    # Initializing the LLM Model on codebase
    DIVIDE("Reading Codebase", "=")
    print("[INFO] Understanding existing codebase")
    init_prompt = prompt.fetch('codebase_init').format(codebase.read_content())
    result = llm.get(prompt=init_prompt, 
                     tool_choice='auto')
    print(result)
    DIVIDE()

    # Selecting the source file to generate tests
    DIVIDE("Selecting Source File", "=")
    source_file = get_user_choice(codebase.file_paths, "Select a source file to generate tests")
    print(f"[INFO] {source_file} chosen for generating test cases")
    source_file_content = codebase._readFile(source_file)
    DIVIDE()

    # Looking through existing test files
    DIVIDE("Selecting Test File", "=")    
    test_file = get_user_choice(codebase.test_files, "Select an existing test file")
    test_file_content = codebase._readFile(test_file)
    print(f"[INFO] {test_file} chosen for existing test cases")

    # Calling the LLM to generate the tests
    generate_tests_prompt = prompt.fetch('generate_test').format(source_file, source_file_content, test_file, test_file_content)

    result = llm.get(prompt=generate_tests_prompt,
                     tool_choice='auto')
    
    print(result)

    DIVIDE()
    DIVIDE()

if __name__=='__main__':
    main()

