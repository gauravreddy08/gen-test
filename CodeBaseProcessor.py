import os
from tree_sitter_languages import get_parser
from typing import List

from GradleSetup import GradleSetup
from CodeCoverage import CodeCoverage

import warnings
warnings.filterwarnings("ignore")

class CodeBaseProcessor():
    def __init__(self, directory: str, language='java'):
        self.directory = directory

        print(f"[INFO] Initiating codebase ({self.directory})")
        if not os.path.isdir(self.directory):
            raise NotADirectoryError(f"{self.directory} is not a directory.")
        
        self.gradleHelper = GradleSetup(self.directory)
        self.source_path = self.gradleHelper.src

        self.coverageHelper = CodeCoverage(self.directory)

        self.directory = directory
        self.code_directory = os.path.join(self.source_path, 'main')

        self.file_paths = self._getFilePaths(self.source_path)

        print(f"[INFO] Reading codebase ({directory})")

        self.test_directory = os.path.join(self.source_path, 'test')
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
            print(f"[INFO] No existing test files found at {self.test_directory}")
            print(f"[INFO] Created test directory: {self.test_directory}")
        
        self.test_files = self._getFilePaths(self.test_directory)

        self.parser = get_parser(language)

        self.database = {}

        self.read_content()

    def _getFilePaths(self, directory: str) -> List[str]:
        file_paths = []

        # Walk through the directory
        for root, _, files in os.walk(directory):
            for file in files:
                # Create the full file path and add it to the list
                if not file.startswith('.') and file.endswith('java'):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)

        return file_paths

    def read_content(self):
        self.repo_tree = ""

        for file_path in self.file_paths:
            self.repo_tree += f'File Path: {file_path}\n'
            if file_path.endswith('.java'):
                self.repo_tree += self._parse_code(file_path) + "\n"
            self.repo_tree+='\n'
    
    def get_tree(self):
        if self.repo_tree is None: 
            self.read_content()
        return self.repo_tree 

    def _parse_code(self, filepath):

        file_content = self.read_file(filepath)

        root_node = self._parse_content(file_content)
        code_dict, body = self._extract_body(file_content, root_node)
        self.database[filepath] = code_dict
        return body
    
    def read_file(self, filepath):
        with open(filepath, 'r') as file:
            return file.read()
    
    def _parse_content(self, content):
        tree = self.parser.parse(bytes(content, "utf8"))
        return tree.root_node

    def _extract_body(self, content, node):
        code_dict = {}
        details = []

        def extract_nodes(node, depth):
            indent = '    ' * depth
            if node.type == 'class_declaration':
                class_name = node.child_by_field_name('name').text.decode('utf8')
                class_body = content[node.start_byte:node.end_byte]
                code_dict[class_name] = class_body
                details.append(f"{indent}class {class_name}")
                for child in node.children:
                    extract_nodes(child, depth + 1)
            elif node.type == 'method_declaration':
                method_name = node.child_by_field_name('name').text.decode('utf8')
                parameters = node.child_by_field_name('parameters').text.decode('utf8')
                return_type = node.child_by_field_name('type').text.decode('utf8')
                method_body = content[node.start_byte:node.end_byte]
                code_dict[method_name] = method_body
                details.append(f"{indent}{return_type} {method_name}{parameters}")
            else:
                for child in node.children:
                    extract_nodes(child, depth)
            

        extract_nodes(node, 0)
        return code_dict, '\n'.join(details)

    def retrieve(self, file_path, name):
        if self.database is None:
            return "Database not initialized."
        
        print(f"[RAG] Retrieving {name} from {file_path}")

        if file_path in self.database.keys():
            
            if name in self.database[file_path].keys():
                return self.database[file_path][name]
            else: 
                return f"Error: {name} does not exist in {file_path}."

        else: 
            return f"Error: {file_path} does not exist."
    
    def get_coverage(self, name, file_path):
        self.gradleHelper.test()
        counts = self.coverageHelper.get_coverage(name, file_path)
        if not isinstance(counts, dict):
            return f"{name} not found. Try again."

        current_coverage = self.coverageHelper.get_percentage(counts)

        coverage_report = f"Coverage Summary for {name}:\n"
    
        for category, counts in counts.items():
            coverage_report += f"\n- {category}:\n"
            coverage_report += f"  - Missed: {counts['missed']}\n"
            coverage_report += f"  - Covered: {counts['covered']}\n"

        coverage_report+= f"\n**Total Coverage: {current_coverage}%**"

        return coverage_report
    
    def write_file(self, file_path: str, content: str) -> str:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w+') as file:
                file.write(content)
            response = f"Changed {file_path}"
            print(f'->  [INFO] {response}')
        except FileNotFoundError:
            response = "The file does not exist."
        except Exception as e:
            response = f"An unexpected error occurred: {e}"
        
        return response

    def open_report(self):
        html_file = self.coverageHelper.html_file
        os.system(f'open {os.path.realpath(html_file)}')

if __name__=='__main__':
    codebase = CodeBaseProcessor('root')
    