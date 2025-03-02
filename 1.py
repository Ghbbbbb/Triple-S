import socket

# 生成要发送的代码
generated_code = """
pri.grab('hexagon_block')\nblack_pos, black_quat = pri.get_obj_pose('black_mug')\ntarget_pos = black_pos + np.array([0, 0, 0.1])\npri.move(target_pos, black_quat)\npri.gripper_ctrl('open')\npri.grab('circle_block')\nhexagon_pos, hexagon_quat = pri.get_obj_pose('hexagon_block')\ntarget_pos = hexagon_pos + np.array([0, 0, 0.1])\npri.move(target_pos, hexagon_quat)\npri.gripper_ctrl('open')\npri.grab('red_block')\ncircle_pos, circle_quat = pri.get_obj_pose('circle_block')\ntarget_pos = circle_pos + np.array([0, 0, 0.1])\npri.move(target_pos, circle_quat)\npri.gripper_ctrl('open')\ncurrent_pos, current_quat = pri.get_current_pose()\ntarget_pos = current_pos + np.array([0, 0.15, 0])\npri.move(target_pos, current_quat)
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


