from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any
import json

class LLM():
    def __init__(self, model_name="gpt-4o", systemPrompt=None, codebase=None):
        print(f"[INFO] Initiating LLM Model ({model_name})")
        load_dotenv()

        self.model = OpenAI()
        self.model_name = model_name
        self.messages = []

        f = open('tools.json', 'r')
        self.tools = json.load(f)

        self.codebase = codebase
        if self.codebase is None:
            raise Exception("No RAG Database provided")

        if systemPrompt: 
            self._append(systemPrompt, 'system')
        
    
    def get(self, prompt: str=None, tool_choice='required') -> str:
        
        if prompt: self._append(prompt, 'user')

        completion = self.model.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            tool_choice=tool_choice,
            tools=self.tools
        )        

        tool_calls = completion.choices[0].message.tool_calls

        if tool_calls:
            self.messages.append(completion.choices[0].message)
            return self._function_call(tool_calls)
        else:
            response = completion.choices[0].message.content
            return response
    
    def _append(self, content: str, role: str):
        self.messages.append({'role': role, 'content': content})
        
    def _function_call(self, tool_calls) -> str:

        for tool_call in tool_calls:
            if tool_call.function.name == 'write_file':
                function_args = json.loads(tool_call.function.arguments)

                function_response = self.codebase.write_file(
                    file_path=function_args.get("file_path"),
                    content=function_args.get("content"),
                )

            elif tool_call.function.name == 'retriever':
                function_args = json.loads(tool_call.function.arguments)

                function_response = self.codebase.retrieve(
                    file_path=function_args.get("file_path"),
                    name=function_args.get("name"),
                )

            elif tool_call.function.name == 'get_coverage':
                function_args = json.loads(tool_call.function.arguments)

                function_response = self.codebase.get_coverage(
                    file_path=function_args.get("file_path"),
                    name=function_args.get("name"),
                )

            self.messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_call.function.name,
                "content": function_response,
            })

        return self.get(tool_choice='auto')

    # def _retriever(self, file_path, name):
    #     print(f"[RAG] Retrieving {name} from {file_path}")
    #     if file_path in self.db.keys():
            
    #         if name in self.db[file_path].keys():
    #             return self.db[file_path][name]
    #         else: 
    #             return f"Error: {name} does not exist in {file_path}."

    #     else: 
    #         return f"Error: {file_path} does not exist."

if __name__ == '__main__':
    from CodeBaseProcessor import CodeBaseProcessor
    from prompts import systemPrompt

    codebase = CodeBaseProcessor('src')

    repo_tree = codebase.get_tree()
    system_prompt = systemPrompt.format(repo_tree=repo_tree)

    llm = LLM(systemPrompt=system_prompt)