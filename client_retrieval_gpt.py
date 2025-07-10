import os
import logging
import socket
import re

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from prompts.prompt_template import get_qa_template_gpt
import commons.embedding_utils as eu
from commons.utils import *

logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)


class GPTAssistant:
    """ Load ChatGPT config and your custom pre-prompts. """

    def __init__(self, verbose=False, prompt_doc="LDIP1_v1/BASELINE") -> None:
        

        logging.info("Initialize LLM...")
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            openai_api_base="https://api.gpts.vin/v1",
            temperature=0,
            max_tokens=2048,
        )
        logging.info(f"Done.")


        logging.info("Initialize tools...")
        self.embedding_model = eu.init_embedding_model()
        self.vector_store = eu.init_vector_store(self.embedding_model, prompt_doc)
        logging.info(f"Done.")

        self.prompt_doc = prompt_doc
        self.verbose = verbose
        self.retriever = self.vector_store.as_retriever(search_kwargs={'k': 4})

        os.system("clear")
        streaming_print_banner()

    def ask(self, question):
        # Dynamically generate the prompt template with the current question
        qa_template = get_qa_template_gpt(self.prompt_doc, question)
        
        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=self.retriever,
            chain_type_kwargs={"prompt": qa_template, "verbose": self.verbose},
            return_source_documents=True
        )

        result_dict = chain(question)
        result = result_dict['result']
        # Extract context and question from result_dict
        source_documents = result_dict.get('source_documents', [])
        context_parts = [doc.page_content for doc in source_documents]
        context = "\n".join(context_parts)
        extracted_question = result_dict.get('query', question)
        
        # Fill the qa_template with context and question
        complete_prompt = qa_template.template.format(context=context, question=extracted_question)
        complete_prompt += result_dict.get("result", "")
        return result,complete_prompt
    
    def handle_response(self, response, question, context):
        if response.startswith("ERROR:"):
            # error_message = response[len("ERROR:"):]
            info = context + "\nHowever, your code has the following error:\n" + response + "\nPlease re-code this task '{}' based on the above information".format(question)+"\n"+"Modified Code:"
            result = self.llm.predict(info)
            return result, response
        else:
            return response, None
    

def extract_python_code(content):
    code_block_regex = re.compile(r"```(?:python)?(.*?)```", re.DOTALL | re.IGNORECASE)
    match = code_block_regex.search(content)
    if match:
        full_code = match.group(1).strip()
        # Remove full line and inline comments while preserving indentation
        code_lines = full_code.split('\n')
        code_without_comments = []
        for line in code_lines:
            stripped_line = line.strip()
            # Remove full line comments
            if not stripped_line.startswith('#'):
                # Remove inline comments
                line_without_inline_comments = re.sub(r'#.*', '', line)
                code_without_comments.append(line_without_inline_comments.rstrip())
        cleaned_code = '\n'.join(code_without_comments)
        return cleaned_code
    else:
        return "Not extract code"
    
def get_summary_line(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if line_number < 1 or line_number > len(lines):
            raise ValueError("Invalid line number")
        return lines[line_number - 1].strip()  # line_number is 1-based
        
def extract_and_format(input_str):
    # Use regular expressions to extract the content within '{}'
    extracted_phrases = re.findall(r'\{([^{}]+)\}', input_str)

    # Join the extracted content with "then"
    joined_phrases = ' then '.join(extracted_phrases)

    # Remove punctuation
    formatted_result = re.sub(r'[^\w\s]', '', joined_phrases)

    return formatted_result

def main(IS_DEBUG = False, IS_DOC = False, PROMPT_DOC = "BASELINE", TASK = "LDIP1_v1"):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    gpt = GPTAssistant(
        verbose=False,prompt_doc=TASK+"/"+PROMPT_DOC
    )
    if not IS_DEBUG:
        HOST = 'localhost'
        PORT = 5001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server.")
    id = 0
    # 1. Debug mode
    while not IS_DOC:
        question = input(colors.YELLOW + "User> " + colors.ENDC)
        if question == "!quit" or question == "!exit":
            break
        if question == "!clear":
            os.system("clear")
            continue
        result,context = gpt.ask(question)  # Ask a question
        code = extract_python_code(result)
        print(colors.GREEN + "Assistant> " + colors.ENDC + f"{result}")
        if not IS_DEBUG:
            payload = {"code": code, "task": TASK}
            s.sendall(json.dumps(payload).encode()[:1300])

            # Wait for a confirmation message or an error message
            response = s.recv(1024).decode()
            feedback, error_message = gpt.handle_response(response, question, context)
            feedback_code = extract_python_code(feedback)
            payload = {"code": feedback_code, "task": TASK}
            print(colors.RED + "Error> " + colors.ENDC + f"{error_message}")
            print(colors.GREEN + "Feedback> " + colors.ENDC + f"{feedback}")

            if error_message:
                s.sendall(json.dumps(payload).encode()[:1300])

                # Wait for a confirmation message or an error message
                response = s.recv(1024).decode()
                if response.startswith("ERROR:"):
                    print(colors.RED + "Final Error> " + colors.ENDC + f"{response[len('ERROR:'):]}")
                else:
                    print(colors.GREEN + "Final Result> " + colors.ENDC + f"{response}")

    # 2. Documentation mode
    if IS_DOC:
        Simplify = True  #Set it to `False` without going through Simplify LLM
        with open(f"dataset/{TASK}.json", "r") as file:
            data = json.load(file)
            num_entries = len(data)
        start = time.time()
        for entry in data:
            question = entry.get("instruction")  # acquire question
            id += 1
            if Simplify:
                simplify_question = extract_and_format(get_summary_line(f"prompts/{TASK}/simplify_result.txt",id)) #In order to save token costs, we directly read simplified tasks that have been predicted in advance
                result,context = gpt.ask(simplify_question)  # answer the question with simplify
                code = extract_python_code(result)
            else:
                result,context = gpt.ask(question)           # answer the question without simplify
                code = extract_python_code(result)
            print('\033[31m'"question:",question)
            if Simplify: print('\033[31m'"simplify_question:",simplify_question)
            print('\033[32m'"result:",result,'\n')

            if not IS_DEBUG:
                payload = {"code": code, "task": TASK}
                s.sendall(json.dumps(payload).encode()[:1300])

                # Wait for a confirmation message or an error message
                response = s.recv(1024).decode()
                feedback, error_message = gpt.handle_response(response, question, context)
                feedback_code = extract_python_code(feedback)
                payload = {"code": feedback_code, "task": TASK}
                print(colors.RED + "Error> " + colors.ENDC + f"{error_message}")
                print(colors.GREEN + "Feedback> " + colors.ENDC + f"{feedback}")

                if error_message:
                    s.sendall(json.dumps(payload).encode()[:1300])

                    # Wait for a confirmation message or an error message
                    response = s.recv(1024).decode()
                    if response.startswith("ERROR:"):
                        print(colors.RED + "Final Error> " + colors.ENDC + f"{response[len('ERROR:'):]}")
                    else:
                        print(colors.GREEN + "Final Result> " + colors.ENDC + f"{response}")

        end = time.time()
        print("mean_time:",(end-start)/num_entries)
        s.shutdown(socket.SHUT_RDWR)
        s.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Run the GPTAssistant")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--doc", action="store_true", help="Enable documentation mode")
    parser.add_argument("--prompt", type=str, default="BASELINE", help="Specify the prompt directory")
    parser.add_argument("--task", type=str, default="LDIP1_v1", help="Specify the dataset directory")

    args = parser.parse_args()
    main(IS_DEBUG=args.debug, IS_DOC=args.doc, PROMPT_DOC=args.prompt, TASK=args.task)
