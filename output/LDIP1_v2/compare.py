import numpy as np
import json
import argparse

# Set command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True, type=str, help="Path to the input file")
args = parser.parse_args()

def load_txt_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    return [json.loads(line) for line in lines]

def load_json_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return [item['goal_pos'] for item in data]

def calculate_error(pos1, pos2):
    pos1_arr = np.array(pos1)
    pos2_arr = np.array(pos2)
    return np.sum(np.abs(pos1_arr - pos2_arr))

def compare_positions(txt_data, json_data, threshold=0.05):
    correct_count = 0
    sum_error = 0
    total_count = len(txt_data)
    incorrect_lines = []
    detailed_errors = []
    
    for i, (txt_item, json_item) in enumerate(zip(txt_data, json_data)):
        json_item = json.loads(json_item)
        gripper_pos_error = calculate_error(txt_item['goal_pos']['gripper_pos'], json_item['gripper_pos'])
        red_goal_error = calculate_error(txt_item['goal_pos']['red_goal'], json_item['red_goal'])
        blue_goal_error = calculate_error(txt_item['goal_pos']['blue_goal'], json_item['blue_goal'])
        green_goal_error = calculate_error(txt_item['goal_pos']['green_goal'], json_item['green_goal'])
        yellow_goal_error = calculate_error(txt_item['goal_pos']['yellow_goal'], json_item['yellow_goal'])

        if txt_item['goal_pos']['gripper_state'] == json_item['gripper_state']:
            gripper_state_error = 0
        else:
            gripper_state_error = 0.05

        total_entry_error = gripper_pos_error + red_goal_error + blue_goal_error + green_goal_error + yellow_goal_error + gripper_state_error


        sum_error += total_entry_error

        if total_entry_error < threshold:
            correct_count += 1
        else:
            incorrect_lines.append(i + 1)  # Store the line number (1-based)
            error_details = {
                'line': i + 1,
                'gripper_pos_error': gripper_pos_error,
                'gripper_state_error': gripper_state_error,
                'total_error': total_entry_error
            }

            error_details.update({
                'red_goal_error': red_goal_error,
                'blue_goal_error': blue_goal_error,
                'green_goal_error': green_goal_error,
                'yellow_goal_error': yellow_goal_error
            })

            detailed_errors.append(error_details)
    
    accuracy = correct_count / total_count
    mean_error = sum_error / total_count
    return accuracy, incorrect_lines, detailed_errors, mean_error

# Choose the appropriate JSON file path based on the environment
json_file_path = '../../dataset/LDIP1_v2.json'

txt_data = load_txt_data(args.file)
json_data = load_json_data(json_file_path)
accuracy, incorrect_lines, detailed_errors, mean_error = compare_positions(txt_data, json_data)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Mean error: {mean_error}")
if incorrect_lines:
    print(f"Incorrect lines: {incorrect_lines}")
    for error_detail in detailed_errors:
        print(f"{error_detail['line']}:{error_detail['total_error']}")
else:
    print("All lines are correct.")
