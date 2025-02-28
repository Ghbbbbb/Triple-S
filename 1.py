import socket

# 生成要发送的代码
generated_code = """
pri.grab('yellow_block')\nblack_pos, black_quat = pri.get_obj_pose('white_mug')\ntarget_pos = black_pos + np.array([0., 0., 0.1])\npri.move(target_pos, black_quat)\npri.gripper_ctrl('open')\npri.stack_object_on_object("red_block","yellow_block")\npri.reset_robot()
"""
# ```pri.grab('red_mug')```
# ```pri.move(np.array([10, 0, 0]), np.array([1, 0, 0]))```
# 连接到服务端
HOST = 'localhost'
PORT = 5001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # 发送代码
    s.sendall(generated_code.encode())

# import json
# import socket

# # 读取 JSON 文件并遍历其中的数据
# with open('robot.json', 'r') as file:
#     data = json.load(file)
#     for item in data:
#         # 生成要发送的代码
#         generated_code = item["answer"]

#         # 连接到服务端
#         HOST = 'localhost'
#         PORT = 5001
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((HOST, PORT))
#             # 发送代码
#             s.sendall(generated_code.encode())


