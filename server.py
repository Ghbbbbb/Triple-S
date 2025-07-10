import errno
import os
import sys
import re
import json
import logging
import socket
import numpy as np
import colorama
colorama.init(autoreset=True)

logging.basicConfig(level=logging.INFO)

sys.path.append(os.path.dirname(__file__))
from demo_env import GraspingEnv


def extract_python_code(content):
    """ Extract the first python code block from the input content.
    :param content: message contains the code from gpt's reply.
    :return(str): python code if the content is correct
    """
    code_block_regex = re.compile(r"```(?:python)?(.*?)```", re.DOTALL | re.IGNORECASE)
    match = code_block_regex.search(content)
    if match:
        full_code = match.group(1).strip()
        return full_code
    else:
        return None


def execute_python_code(pri, code, ENV_TYPE, TASK):
    """ Execute python code with the input content.
    :param pri(Class): class name in prompts.
    :param content(str): full content including the code block.
    """
    if code == "Not extract code":
        return False, "Not extract code, write the code in the format ```python\n[your code]\n```"

    print("\n"'\033[34m'"Please wait while I run the code in Sim...")
    print("\033[34m""code:" + code)

    try:
        exec(code)
        print('\033[32m'"Done!\n")
        return True, None
    except Exception as e:
        print('\033[31m'"Found error while running the code: {}".format(e))
        if str(e) =="Invalid action length.":
            e="`move()` func should input parameters: position, quaternion"
        if "Invalid direction" in str(e):
            e = "direction only chosen from 'left', 'right', 'forward', 'backward'"
        if "Invalid name" in str(e):
            if ENV_TYPE == 2:
                e = str(e).split(".")[0] + ". Valid names: ['block1', 'block2', 'block3', 'block4', 'white_mug', 'black_mug']"
            else:
                if TASK == "LDIP1_v1":
                    e = str(e).split(".")[0] + ". Valid names: ['red_block', 'blue_block', 'green_block', 'yellow_block', 'white_mug', 'black_mug'.]"
                if TASK == "LDIP1_v2":
                    e = str(e).split(".")[0] + ". Valid names: ['red_block', 'blue_block', 'green_block', 'yellow_block', 'triangle_block', 'circle_block', 'square_block', 'hexagon_block', 'white_mug', 'black_mug'.]"
                # more valid_names in the future...
        exec("pri.reset_robot()")
        return False, str(e)


def write_goal_positions_to_json(env, filename):
    try:
        gripper_pos, _ = env.get_current_pose()
        gripper_state = env.get_gripper_status()
        red_goal = env.get_body_pos('red_block')
        blue_goal = env.get_body_pos('blue_block')
        green_goal = env.get_body_pos('green_block')
        yellow_goal = env.get_body_pos('yellow_block')

        gripper_pos_list = gripper_pos.tolist()
        red_goal_list = red_goal.tolist()
        blue_goal_list = blue_goal.tolist()
        green_goal_list = green_goal.tolist()
        yellow_goal_list = yellow_goal.tolist()

        goal_pos = {
            "gripper_pos": gripper_pos_list,
            "gripper_state": gripper_state,
            "red_goal": red_goal_list,
            "blue_goal": blue_goal_list,
            "green_goal": green_goal_list,
            "yellow_goal": yellow_goal_list
        }

        data = {
            "goal_pos": goal_pos
        }

        with open(filename, 'a') as file:
            file.write(json.dumps(data, separators=(',', ':')))
            file.write('\n')
        print("Goal positions written to {} file.".format(filename))
    except Exception as e:
        print(f"An error occurred while writing goal positions to JSON file: {e}")


def write_goal_positions_to_json2(env, filename):
    try:
        gripper_pos, _ = env.get_current_pose()
        gripper_state = env.get_gripper_status()
        block1_goal = env.get_body_pos('block1')
        block2_goal = env.get_body_pos('block2')
        block3_goal = env.get_body_pos('block3')
        block4_goal = env.get_body_pos('block4')

        gripper_pos_list = gripper_pos.tolist()
        block1_goal_list = block1_goal.tolist()
        block2_goal_list = block2_goal.tolist()
        block3_goal_list = block3_goal.tolist()
        block4_goal_list = block4_goal.tolist()

        goal_pos = {
            "gripper_pos": gripper_pos_list,
            "gripper_state": gripper_state,
            "block1_goal": block1_goal_list,
            "block2_goal": block2_goal_list,
            "block3_goal": block3_goal_list,
            "block4_goal": block4_goal_list
        }

        data = {
            "goal_pos": goal_pos
        }

        with open(filename, 'a') as file:
            file.write(json.dumps(data, separators=(',', ':')))
            file.write('\n')

        print("Goal positions written to {} file.".format(filename.split('/')[-1]))
    except Exception as e:
        print(f"An error occurred while writing goal positions to JSON file: {e}")


def main(WRITE="GPT3.5-BASELINE", IS_DOC=False, ENV_TYPE=1):
    logging.info("Initializing TCP...")
    HOST = ''
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, 5001))
    ss.listen(1)
    ss.setblocking(0)
    logging.info("Done.")

    logging.info("Initializing Simulator...")
    env = GraspingEnv(ENV_TYPE)
    env.reset()
    logging.info("Done.")

    while True:
        try:
            logging.info("Waiting for connection...")
            conn, addr = ss.accept()
            conn.setblocking(0)
            logging.info(f"Connected by {addr}")

            while True:
                first_attempt = True  # Reset the 'first_attempt' flag for each task

                while True:
                    try:
                        data = json.loads(conn.recv(10000))
                        TASK = data["task"]
                        code = data["code"]
        
                        # data,TASK = conn.recv(10000)
                        if not code:
                            break
                        success, error_message = execute_python_code(env, code, ENV_TYPE, TASK)
                        # success, error_message = execute_python_code(env, data.decode(),IS_ENV2)
                        if WRITE and success:
                            if ENV_TYPE == 2:
                                write_goal_positions_to_json2(env,f'output/{TASK}/{WRITE}.txt')
                            else:
                                write_goal_positions_to_json(env,f'output/{TASK}/{WRITE}.txt')

                        if success:
                            first_attempt = True
                            if IS_DOC:
                                env.step(env.action)
                                env.reset()
                            else:
                                env.step(env.action)
                            conn.sendall("ACK".encode())
                        else:
                            if first_attempt:
                                env.reset()          # Consider the case where the robotic arm stops midway due to a code error, requiring an environment reset
                                conn.sendall(f"ERROR:{error_message}".encode())
                                first_attempt = False
                            else:
                                env.reset()          # Consider the case where the robotic arm stops midway due to a code error, requiring an environment reset
                                if WRITE:
                                    if ENV_TYPE == 2:
                                        write_goal_positions_to_json2(env,f'output/{TASK}/{WRITE}.txt')
                                    else:
                                        write_goal_positions_to_json(env,f'output/{TASK}/{WRITE}.txt')
                                conn.sendall("ERROR:Final Error".encode())
                                first_attempt = True

                    except socket.error as e:
                        if e.errno == errno.EWOULDBLOCK:
                            pass
                        else:
                            raise
        except socket.error as e:
            if e.errno == errno.EWOULDBLOCK:
                pass
            else:
                raise


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Server for interacting with robot via various input methods.")
    parser.add_argument("--write", type=str, default="GPT3.5-BASELINE", help="Specify the write directory")
    parser.add_argument("--doc", action="store_true", help="Run in document mode else in debug mode")
    parser.add_argument("--env", type=int, default=1, help="Set the environment type, 1 is observable, 2 is particially observable")
    args = parser.parse_args()
    main(WRITE=args.write, IS_DOC=args.doc, ENV_TYPE=args.env)