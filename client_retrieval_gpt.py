import os
import logging
import socket
import re

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from prompts.prompt_template import get_qa_template_baichuan
import commons.embedding_utils as eu
from commons.utils import *

logging.basicConfig(level=logging.INFO)


class GPTAssistant:
    """ Load ChatGPT config and your custom pre-prompts. """

    def __init__(self, verbose=False, prompt_doc="dcpd1_base") -> None:
        

        logging.info("Initialize LLM...")
        self.llm = ChatOpenAI(
            api_key="sk-6hOFtkVOJsEp5PwdD7B38c94C8A44a54Bb2b68105fB17aB6",
            openai_api_base="https://api.gpts.vin/v1",
            # openai_api_base="https://api.xiaoai.plus/v1",
            model="gpt-3.5-turbo-16k-0613",
            temperature=0.2,
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

        os.system("cls")
        streaming_print_banner()

    def ask(self, question, id):
        # Dynamically generate the prompt template with the current question
        qa_template = get_qa_template_baichuan(self.prompt_doc, question,id)
        
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
        
def write_to_file(file_path, question, result, response):
    """
    将问题、结果和响应写入指定的文本文件。
    """
    state = "error" if response.startswith("ERROR:") else "succeed"
    record = {
        "state": state,
        "User": question,
        "Robot": result
    }
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(record) + '\n')

def extract_python_code(content):
    """Extract the first python code block from the input content and remove comments.
    :param content: message contains the code from GPT's reply.
    :return(str): python code without comments if the content is correct
    """
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
    # 使用正则表达式提取'{}'中的内容
    extracted_phrases = re.findall(r'\{([^{}]+)\}', input_str)

    # 将提取的内容用"then"连接
    joined_phrases = ' then '.join(extracted_phrases)

    # 去掉标点符号
    formatted_result = re.sub(r'[^\w\s]', '', joined_phrases)

    return formatted_result

def main(IS_DEBUG = False, IS_DOC = False, PROMPT_DOC = "dcpd1_base", TASK = "dcpd1-1"):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    gpt = GPTAssistant(
        verbose=False,prompt_doc=PROMPT_DOC
    )
    if not IS_DEBUG:
        HOST = 'localhost'
        PORT = 5003
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server.")
    id = 0
    while not IS_DOC:
        question = input(colors.YELLOW + "User> " + colors.ENDC)
        id += 1
        if question == "!quit" or question == "!exit":
            break
        if question == "!clear":
            os.system("cls")
            continue
        # _, simplify_question = simplify(question)
        result,context = gpt.ask(question,id)  # Ask a question
        code = extract_python_code(result)
        print(colors.GREEN + "Assistant> " + colors.ENDC + f"{result}")
        if not IS_DEBUG:
            s.sendall(code.encode()[:1300])

            # 等待确认消息或错误消息
            response = s.recv(1024).decode()
            feedback, error_message = gpt.handle_response(response, question, context)
            feedback_code = extract_python_code(feedback)
            print(colors.RED + "Error> " + colors.ENDC + f"{error_message}")
            print(colors.GREEN + "Feedback> " + colors.ENDC + f"{feedback}")

            if error_message:
                s.sendall(feedback_code.encode()[:1300])

                # 等待确认消息或错误消息
                response = s.recv(1024).decode()
                if response.startswith("ERROR:"):
                    print(colors.RED + "Final Error> " + colors.ENDC + f"{response[len('ERROR:'):]}")
                else:
                    print(colors.GREEN + "Final Result> " + colors.ENDC + f"{response}")

    # 2.文件输入
    if IS_DOC:
        with open(f"dataset/{TASK}.json", "r") as file:
            data = json.load(file)
            num_entries = len(data)
        start = time.time()
        for entry in data:
            id += 1
            question = entry.get("instruction")  # 获取问题
            # simplify_question = extract_and_format(get_summary_line(f"prompts/simplify_{TASK}.txt",id))
            # _, simplify_question = simplify(question)
            result,context = gpt.ask(question,id)  # 调用函数获取答案
            code = extract_python_code(result)
            print('\033[31m'"question:",question)
            # print('\033[31m'"simplify_question:",simplify_question)
            print('\033[32m'"result:",result,'\n')

            if not IS_DEBUG:
                s.sendall(code.encode()[:1300])

                # 等待确认消息或错误消息
                response = s.recv(1024).decode()
                feedback, error_message = gpt.handle_response(response, question, context)
                feedback_code = extract_python_code(feedback)
                print(colors.RED + "Error> " + colors.ENDC + f"{error_message}")
                print(colors.GREEN + "Feedback> " + colors.ENDC + f"{feedback}")
                write_to_file(f"output/qa/gpt3.5_{TASK}", question, result, response)

                if error_message:
                    s.sendall(feedback_code.encode()[:1300])

                    # 等待确认消息或错误消息
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
    parser.add_argument("--prompt", type=str, default="dcpd1_base", help="Specify the prompt directory")
    parser.add_argument("--task", type=str, default="dcpd1-1", help="Specify the dataset directory")

    args = parser.parse_args()
    main(IS_DEBUG=args.debug, IS_DOC=args.doc, PROMPT_DOC=args.prompt, TASK=args.task)
