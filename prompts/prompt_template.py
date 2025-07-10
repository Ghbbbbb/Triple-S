import os

try:
    from langchain.prompts.chat import PromptTemplate
except:
    from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

class PromptLoader:
    def __init__(self, prompt_doc: str) -> None:
        #Get the current file's directory
        current_dir = os.path.dirname(__file__)
        # Construct the base directory path
        self.dir_path = os.path.join(current_dir, prompt_doc)

    @property
    def pri_prompt(self) -> str:
        with open(os.path.join(self.dir_path, "primitives.txt")) as f:
            prompt = f.read()
        return prompt

    @property
    def sce_prompt(self) -> str:
        with open(os.path.join(self.dir_path, "scene.txt")) as f:
            prompt = f.read()
        return prompt

    @property
    def sys_prompt(self) -> str:
        with open(os.path.join(self.dir_path, "system.txt")) as f:
            prompt = f.read()
        return prompt
    
    @property
    def settings_prompt(self) -> str:
        with open(os.path.join(self.dir_path, "task_settings.txt")) as f:
            prompt = f.read()
        return prompt
    



def get_qa_template_gpt(prompt_doc: str,question:str):
    prompt_loader = PromptLoader(prompt_doc)

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """


    _DEFAULT_QA_TEMPLATE_BAICHUAN1 = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and to perform the user's command.
-----------
Human: {question}
You:"""
    
    QA_TEMPLATE_BAICHUAN = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_BAICHUAN1,
    )

    return QA_TEMPLATE_BAICHUAN



def get_qa_template_llama(prompt_doc: str,question:str):
    prompt_loader = PromptLoader(prompt_doc)

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """


    _DEFAULT_QA_TEMPLATE_LLAMA1 = "<|system|>"+_ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and to perform the user's command.
-----------
<|user|>
Human: {question}
<|assistant|>
You:"""


    QA_TEMPLATE_LLAMA = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_LLAMA1,
    )

    return QA_TEMPLATE_LLAMA