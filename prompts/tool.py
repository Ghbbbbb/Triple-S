from openai import OpenAI
import re
from typing import List, Dict

class LDIPProcessor:
    def __init__(self, base_url: str = "https://api.gpts.vin/v1"):
        self.client = OpenAI(base_url=base_url)
        self.messages_simple = []
        self.messages_summary = []
        
    def read_content_from_file(self, file_path: str) -> str:
        """Read content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return ""
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return ""

    def load_prompts(self):
        """Load all prompt files."""
        # Define file paths
        prompt_files = {
            'sim_LDIP1_v1': 'LDIP1_v1/simplify_prompt.txt',
            'sim_LDIP1_v2': 'LDIP1_v2/simplify_prompt.txt',
            'sim_LDIP2': 'LDIP2/simplify_prompt.txt',
            'sum_LDIP1_v1': 'LDIP1_v1/summary_prompt.txt',
            'sum_LDIP1_v2': 'LDIP1_v2/summary_prompt.txt',
            'sum_LDIP2': 'LDIP2/summary_prompt.txt'
        }

        # Read all files
        prompts = {name: self.read_content_from_file(path) 
                  for name, path in prompt_files.items()}

        # Initialize message lists
        self.messages_simple = [
            {"role": "system", "content": prompts['sim_LDIP1_v2']},
        ]
        
        self.messages_summary = [
            {"role": "system", "content": prompts['sum_LDIP1_v1']},
        ]

    def simplify(self, user_input: str, model: str = "gpt-4-turbo") -> str:
        """Simplify user input using LLM, with fresh context each time."""
        try:
            # Reset messages to only system prompt + current input
            current_messages = [
                {"role": "system", "content": self.messages_simple[0]["content"]},
                {"role": "user", "content": user_input}
            ]
            response = self.client.chat.completions.create(
                model=model,
                messages=current_messages,  # Use fresh context
                stream=False,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during simplification: {str(e)}")
            return ""

    def summary(self, user_input: str, model: str = "gpt-3.5-turbo-16k") -> str:
        """Generate summary using LLM."""
        try:
            current_messages = [
                {"role": "system", "content": self.messages_simple[0]["content"]},
                {"role": "user", "content": user_input}
            ]
            response = self.client.chat.completions.create(
                model=model,
                messages=current_messages,
                stream=False,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error during summarization: {str(e)}")
            return ""

    @staticmethod
    def save_to_file(content: str, file_name: str = "output.txt"):
        """Save content to a file."""
        try:
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(content + "\n")
        except Exception as e:
            print(f"Error writing to file {file_name}: {str(e)}")

def main():
    processor = LDIPProcessor()
    processor.load_prompts()
    
    print("LDIP Processor initialized. Choose mode:")
    print("1. Simplify mode")
    print("2. Summary mode")
    
    # mode = input("Enter mode (1 or 2): ")
    # output_file = input("Enter output file name (default: output.txt): ") or "output.txt"
    mode = "1"
    output_file = "output2.txt"
    
    if mode == "1":
        print("Simplify mode activated. Enter questions (type 'quit' to exit):")
        while True:
            user_input = input("Question: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            result = processor.simplify(user_input)
            print(result)
            print("\n")
            processor.save_to_file(result, output_file)
    elif mode == "2":
        print("Summary mode activated. Enter questions (type 'quit' to exit):")
        while True:
            user_input = input("Question: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            result = processor.summary(user_input)
            print(result)
            processor.save_to_file(result, output_file)
    else:
        print("Invalid mode selected. Exiting.")

if __name__ == "__main__":
    main()