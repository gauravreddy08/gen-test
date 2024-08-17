from LLM import LLM
from CodeBaseProcessor import CodeBaseProcessor
from prompts import systemPrompt, generaionPrompt, existingTestPrompt
from utils import get_user_choice, DIVIDE, get_target_coverage
import sys

def main(directory):

    codebase = CodeBaseProcessor(directory)
    codebase.open_report()

    while True:
    
        repo_tree = codebase.get_tree()
        DIVIDE()

        # Initializing the LLM Model on codebase
        system_prompt = systemPrompt.format(repo_tree=repo_tree)
        llm = LLM(systemPrompt=system_prompt,
                codebase=codebase)
        DIVIDE()

        # Selecting the source file to generate tests
        source_file = get_user_choice(codebase.file_paths, "Select a source file to generate tests")
        source_block = get_user_choice(codebase.database[source_file], "Select a block to generate tests for")
        block_content = codebase.retrieve(source_file, source_block)
        print(f"[USER] {source_block} chosen for generating test cases")
        DIVIDE()

        test_file = get_user_choice(codebase.test_files, "Select a existing test file to enhance", addNone=True)
        print(f"[USER] {test_file} chosen as existing test code")
        DIVIDE()

        desired_coverage = get_target_coverage()

        DIVIDE()
        
        prompt = generaionPrompt.format(file_path = source_file, 
                                        name=source_block, 
                                        code_block=block_content, 
                                        desired_coverage=desired_coverage)
        if test_file:
            prompt += existingTestPrompt.format(file_path=test_file, code_block = codebase.read_file(test_file))

        response = llm.get(prompt)
        DIVIDE()
        print(response)
        DIVIDE()

        continue_processing = input("Would you like to process another file? (yes/no): ").strip().lower()

        if continue_processing not in ["yes", "no"]:
            continue_processing = "no"

        if continue_processing=='no': break

    codebase.open_report()

if __name__=='__main__':
    args = sys.argv
    main(args[1])