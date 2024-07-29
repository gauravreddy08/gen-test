import os
from typing import List

class CodeBaseProcessor():
    def __init__(self, directory: str):
        print(f"[INFO] Initiating codebase ({directory})")
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"{directory} is not a directory.")

        self.directory = directory
        self.file_paths = self._getFilePaths(self.directory, ignore_test=True)

        print(f"[INFO] Reading codebase ({directory})")

        self.test_directory = os.path.join(self.directory, 'test')
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
            print(f"[INFO] No existing test files found at {self.test_directory}")
            print(f"[INFO] Created test directory: {self.test_directory}")
        
        self.test_files = self._getFilePaths(self.test_directory)
        self.test_files.append(self.test_directory)
        
    def _readFile(self, filepath: str) -> str:
        if not os.path.isfile(filepath): return None
        try:
            with open(filepath, 'r', errors=None) as file:
                    content = file.read()
        except FileNotFoundError:
            print(f"## File \"{filepath}\" cannot be found")
        return content

    def read_content(self) -> str:
        content = ""

        for file in self.file_paths:
            content += f'File Path: {file}\n```\n{self._readFile(file)}\n```\n\n'

        return content

    def _getFilePaths(self, directory: str, ignore_test=False) -> List[str]:
        file_paths = []

        # Walk through the directory
        for root, _, files in os.walk(directory):
            if ignore_test and root.endswith('test'):
                continue
            for file in files:
                # Create the full file path and add it to the list
                if not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)

        return file_paths
