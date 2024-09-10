from openai import OpenAI
import re

def read_content_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


file_simp_path = 'E:/Git/Git/gitclone/MRoP/prompts/simplify.txt'
specified_simp_content = read_content_from_file(file_simp_path)

file_sum_path = 'E:/Git/Git/gitclone/MRoP/prompts/summary.txt'
specified_sum_content = read_content_from_file(file_sum_path)


messages_simple = [
    {"role": "system", "content": specified_simp_content},
]

messages_summary = [
    {"role": "system", "content": specified_sum_content},
]

client = OpenAI(
    # base_url="https://api.gpts.vin/v1",
    )

def extract_and_format(input_str):
    # Use regular expressions to extract the content within '{}'
    extracted_phrases = re.findall(r'\{([^{}]+)\}', input_str)

    # Join the extracted content with "then"
    joined_phrases = ' then '.join(extracted_phrases)

    # Remove punctuation
    formatted_result = re.sub(r'[^\w\s]', '', joined_phrases)

    return formatted_result

# ######### 
# Stage1.Simplify LLM
def simplify(user_input:str):
    messages_simple.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_simple, stream=False,temperature=0)
    raw_sim = response.choices[0].message.content
    # extract_sim = extract_and_format(raw_sim)
    return raw_sim

file_name = "test.txt"
while True:
    user_input = input("question:")
    result = simplify(user_input)
    print(result)
    
    # Write the results to the specified file, one line at a time
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(result + "\n")



# # # # Stage3. Summary LLM
# def summary(user_input:str):
#     messages_summary.append({"role": "user", "content": user_input})
#     response = client.chat.completions.create(model="gpt-3.5-turbo-0613", messages=messages_summary, stream=False,temperature=0)
#     print(response.choices[0].message.content)
#     return response.choices[0].message.content

# file_name = "test.txt"
# while True:
#     user_input = input("question:")
#     result = summary(user_input)
#     print(result)
    
#     # Write the results to the specified file, one line at a time
#     with open(file_name, "a", encoding="utf-8") as file:
#         file.write(result + "\n")