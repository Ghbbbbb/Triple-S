import os
from .tool import generate_role

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
        # 获取当前文件所在目录
        current_dir = os.path.dirname(__file__)
        # 构建base目录路径
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
    

def get_memory_conversation_template(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """
    _TASK_SETTINGS_PROMPT_TEMPLATE = f"""
    Here are some rules you need to note:

    {prompt_loader.settings_prompt}
    ----------
    """

    _DEFAULT_MEMORY_CONVERSATION_TEMPLATE = B_INST + B_SYS + _ROBOT_PROMPT_TEMPLATE + _TASK_SETTINGS_PROMPT_TEMPLATE + E_SYS + """
    Use the above context to answer the user's question and perform the user's command.
    -----------
    Current conversation:
    {history}
    Last line:
    Human: {input}
    You:""" + E_INST

    MEMORY_CONVERSATION_TEMPLATE = PromptTemplate(
        input_variables=["history", "input"],
        template=_DEFAULT_MEMORY_CONVERSATION_TEMPLATE,
    )

    return MEMORY_CONVERSATION_TEMPLATE


def get_memory_conversation_template_2(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """
    _TASK_SETTINGS_PROMPT_TEMPLATE = f"""
    Here are some rules you need to note:

    {prompt_loader.settings_prompt}
    ----------
    """

    system_template = B_SYS + _ROBOT_PROMPT_TEMPLATE + _TASK_SETTINGS_PROMPT_TEMPLATE + E_SYS + """
    Use the above context to answer the user's question and perform the user's command.
    -----------
    Current conversation:
    {history}
    """
    # 构建初始 messages 列表，这里可以理解为是 openai 传入的 messages 参数
    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(B_INST + '{input}' + E_INST)
    ]
    MEMORY_CONVERSATION_TEMPLATE_2 = ChatPromptTemplate.from_messages(messages)

    return MEMORY_CONVERSATION_TEMPLATE_2


def get_qa_template(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """
    _DEFAULT_QA_TEMPLATE = B_INST + B_SYS + _ROBOT_PROMPT_TEMPLATE + "{context}" + E_SYS + """
    Use the above context to answer the user's question and perform the user's command.
    -----------
    Human: {question}
    You:""" + E_INST

    QA_TEMPLATE = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE,
    )

    return QA_TEMPLATE


def get_qa_template_baichuan(prompt_doc: str,question:str,id):
    prompt_loader = PromptLoader(prompt_doc)

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """


    def get_summary_line(file_path, line_number):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if line_number < 1 or line_number > len(lines):
                raise ValueError("Invalid line number")
            return lines[line_number - 1].strip()  # line_number is 1-based
        
    #通过调用文件生成(提前通过gpt生成)
    SUMMARY = get_summary_line("E:/Git/Git/gitclone/MRoP/prompts/api_select_env1_level3.txt", id)
    #通过gpt生成
    # SUMMARY = api_select(question)
    ROLE = generate_role(question)


    ##################有RAG#####################
    _DEFAULT_QA_TEMPLATE_BAICHUAN1 = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and to perform the user's command.
-----------
Human: {question}
You:"""

    ##################RAG+API###################
    _DEFAULT_QA_TEMPLATE_BAICHUAN2 = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and perform the user's command.
-----------
Human: {question}"""+"\n"+SUMMARY+"""
You:"""

    ##################RAG+ROLE###################
    _DEFAULT_QA_TEMPLATE_BAICHUAN3 = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and perform the user's command.
-----------
Human: {question}"""+"\n"+ROLE+"""
You:"""

    ##################RAG+API+ROLE###################
    _DEFAULT_QA_TEMPLATE_BAICHUAN4 = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and perform the user's command.
-----------
Human: {question}"""+"\n"+SUMMARY+"\n"+ROLE+"""
You:"""
    
    QA_TEMPLATE_BAICHUAN = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_BAICHUAN1,
    )

    return QA_TEMPLATE_BAICHUAN




def get_qa_template_baichuan_abb(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """


    ##################有RAG#####################
    _DEFAULT_QA_TEMPLATE_BAICHUAN_ABB = _ROBOT_PROMPT_TEMPLATE + "{context}" + """
Use the above context to answer the user's question and to perform the user's command.
-----------
Human: {question}
You:"""
    
    QA_TEMPLATE_BAICHUAN = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_BAICHUAN_ABB,
    )

    return QA_TEMPLATE_BAICHUAN



def get_qa_template_mistral(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    B_INST, E_INST = "[INST]", "[/INST]"

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """
    _DEFAULT_QA_TEMPLATE_MISTRAL = B_INST + _ROBOT_PROMPT_TEMPLATE + "{context}" + """
    Use the above context to answer the user's question and perform the user's command.
    -----------
    Human: {question}
    You:""" + E_INST

    QA_TEMPLATE_MISTRAL = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_MISTRAL,
    )

    return QA_TEMPLATE_MISTRAL


def get_qa_mem_template(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    _ROBOT_PROMPT_TEMPLATE = f"""
    {prompt_loader.sys_prompt}

    {prompt_loader.sce_prompt}

    {prompt_loader.pri_prompt}

    """
    _DEFAULT_QA_TEMPLATE = B_INST + B_SYS + _ROBOT_PROMPT_TEMPLATE + "{context}" + E_SYS + """
    Use the above context to answer the user's question and perform the user's command.
    -----------
    {chat_history}
    Human: {question}
    You:""" + E_INST

    QA_MEM_TEMPLATE = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=_DEFAULT_QA_TEMPLATE,
    )

    return QA_MEM_TEMPLATE


def get_qa_template_zephyr(prompt_doc: str):
    prompt_loader = PromptLoader(prompt_doc)

    _DEFAULT_QA_TEMPLATE_ZEPHYR = '<|system|>\n' + "{context}" + """
    Use the above context to answer the user's question and perform the user's command.
    """ + "\n<|user|>\n{question}""" + """\n<|assistant|>"""

    QA_TEMPLATE_ZEPHYR = PromptTemplate(
        input_variables=["context", "question"],
        template=_DEFAULT_QA_TEMPLATE_ZEPHYR,
    )

    return QA_TEMPLATE_ZEPHYR