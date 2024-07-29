from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any
from utils import write_file
import json

class LLMModel():
    def __init__(self, model_name="gpt-4o"):
        print(f"[INFO] Initiating LLM Model ({model_name})")
        load_dotenv()
        self.model = OpenAI()
        self.model_name = model_name
        self.messages = []

        self.edit_tool = {"type": "function", "function": {"name": "write_file"}}

        f = open('tools.json', 'r')
        self.tools = json.load(f)
    
    def get(self, prompt: List[Dict[str, str]], tool_choice='none') -> str:
        
        self._expandconvo(prompt, 'user')

        if tool_choice=='edit':
            tool_choice = self.edit_tool

        result = self.model.chat.completions.create(
            model=self.model_name,
            messages=self.messages,
            tool_choice=tool_choice,
            tools=self.tools
        )

        if tool_choice != 'none':
            if result.choices[0].message.content:
                print(result.choices[0].message.content)
            response = self._function_call(result.choices[0].message.tool_calls)
        else:
            response = result.choices[0].message.content
             
        self._expandconvo(response, 'assistant')
        return response
    
    def _expandconvo(self, content: str, role: str):
        self.messages.append({'role': role, 'content': content})
         

    def _function_call(self, calls) -> str:
        response = ""
        for call in calls:
                if call.function.name == 'write_file':
                    response += write_file(file_path=json.loads(call.function.arguments)['file_path'],
                                         content=json.loads(call.function.arguments)['content'])
                    response += '\n'
        
        return response
                     


