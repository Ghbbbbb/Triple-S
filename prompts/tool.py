from openai import OpenAI
import re

def read_content_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

file_api_path = 'E:/Git/Git/gitclone/MRoP/prompts/api.txt'
specified_api_content = read_content_from_file(file_api_path)

file_simp_path = 'E:/Git/Git/gitclone/MRoP/prompts/simplify2.txt'
specified_simp_content = read_content_from_file(file_simp_path)

file_sum_path = 'E:/Git/Git/gitclone/MRoP/prompts/summary2.txt'
specified_sum_content = read_content_from_file(file_sum_path)

messages_api = [
    {"role": "system", "content": specified_api_content},
]

messages_simple = [
    {"role": "system", "content": specified_simp_content},
]

messages_summary = [
    {"role": "system", "content": specified_sum_content},
]

client = OpenAI(base_url="https://api.gpts.vin/v1",
                api_key="sk-stvOGguPzkrr50Sf6e9d874d59534d638cE92e897956E4A2")
#sk-ico5RYynS4XU4mi6F51b984aF71f458f8eDcFcD5BeC64d25 $5

def extract_and_format(input_str):
    # 使用正则表达式提取'{}'中的内容
    extracted_phrases = re.findall(r'\{([^{}]+)\}', input_str)

    # 将提取的内容用"then"连接
    joined_phrases = ' then '.join(extracted_phrases)

    # 去掉标点符号
    formatted_result = re.sub(r'[^\w\s]', '', joined_phrases)

    return formatted_result

# ######### 1.手动总结
# while True:
#     user_input = input("question:")

#     def summary(user_input:str):
#         messages_api.append({"role": "user", "content": user_input})
#         response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_api, stream=False,temperature=0)
#         print(response.choices[0].message.content)
#         return response.choices[0].message.content
#     summary(user_input)
# 2.自动总结
# def api_select(user_input:str):
#     messages_api.append({"role": "user", "content": user_input})
#     response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_api, stream=False,temperature=0)
#     return response.choices[0].message.content

###########3.手动简化

# def simplify(user_input:str):
#     messages_simple.append({"role": "user", "content": user_input})
#     response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_simple, stream=False,temperature=0)
#     raw_sim = response.choices[0].message.content
#     # extract_sim = extract_and_format(raw_sim)
#     return raw_sim

# # # 指定要写入的文件名
# file_name = "prompts\simplify_dcpd2.txt"

# while True:
#     user_input = input("question:")
#     result = simplify(user_input)
#     print(result)
    
#     # 将结果写入指定的文件中，每次写入一行
#     with open(file_name, "a", encoding="utf-8") as file:
#         file.write(result + "\n")



#4.规则生成
def generate_role(input_str):
    outputs = ["For this task, following rules may be help:"]
    rules = []

    if "facing" in input_str:
        rules.append("Considering relative positions, if I am facing you, then my left side is your right side. If we are both facing the same direction, then my left side is still your left side.")
    if "color" in input_str:
        rules.append("Think about what color does those object like and then match the object with the following items in the table scene:'red_block', 'green_block', 'green_block', 'yellow_block', 'white_mug' and 'black_mug'.")
    if "left" in input_str:
        rules.append("If current position is cur_pos, then move 10cm left --> ```cur_pos + np.array([0, 0.1, 0])```")
    if "right" in input_str:
        rules.append("If current position is cur_pos, then move 10cm right --> ```cur_pos + np.array([0, -0.1, 0])```")
    if "forward" in input_str or "front" in input_str:
        rules.append("If current position is cur_pos, then move 10cm forward --> ```cur_pos + np.array([0.1, 0, 0])```")
    if "behind" in input_str or "backward" in input_str:
        rules.append("If current position is cur_pos, then move 10cm backwards --> ```cur_pos + np.array([-0.1, 0, 0])```")
    if "over" in input_str or "above" in input_str:
        rules.append("If current position is cur_pos, then move 10cm above --> ```cur_pos + np.array([0, 0, 0.1])```")
    if "farthest" in input_str or "closest" in input_str:
        rules.append("First to get the obj pose use ```pri.get_obj_pose()```, then calculate the distance between the objects using ```np.linalg.norm()```")
    if not rules:
        return ""
    
    for idx, rule in enumerate(rules, 1):
        outputs.append(f"{idx}.{rule}")
    
    return "\n".join(outputs)


# # 2.手动更新
# while True:
#     user_input = input("question:")

#     def summary(user_input:str):
#         messages_api.append({"role": "user", "content": user_input})
#         response = client.chat.completions.create(model="gpt-4-turbo", messages=messages_summary, stream=False,temperature=0)
#         print(response.choices[0].message.content)
#         return response.choices[0].message.content
#     summary(user_input)
# # 2.自动更新
# def api_select(user_input:str):
#     messages_api.append({"role": "user", "content": user_input})
#     response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_api, stream=False,temperature=0)
#     return response.choices[0].message.content