import numpy as np
import time
import json

from robopal.envs import RobotEnv
from robopal.robots.diana_med import DianaGraspMultiObjs,DianaGraspMultiObjs_Partobservable

def primitive(func, checker=None):
    """ primitive flag, no practical effect. """

    def primitive_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return primitive_wrapper

with open("./commons/info.json", "r") as f:
    blocks_info = json.load(f)

name_map = {block["shape"]: block["color"] for block in blocks_info}

class GraspingEnv(RobotEnv):
    def __init__(self,
                 ENV_TYPE,
                 render_mode='human',
                 control_freq=100,
                 enable_camera_viewer=False,
                 controller='CARTIK',
                 is_interpolate=False,
                #  camera_name='cam'
                 ):
        if ENV_TYPE == 1:
            robot = DianaGraspMultiObjs()
        if ENV_TYPE == 2:
            robot = DianaGraspMultiObjs_Partobservable()
        super().__init__(
            robot=robot,
            render_mode=render_mode,
            control_freq=control_freq,
            enable_camera_viewer=enable_camera_viewer,
            controller=controller,
            is_interpolate=is_interpolate,
            # camera_name = camera_name
        )

        self.init_pos, self.init_rot = self.controller.forward_kinematics(self.robot.get_arm_qpos())
        self.action = self.init_pos

    @primitive
    def reset_robot(self):
        self.move(self.init_pos, self.init_rot)

    @primitive
    def get_obj_pose(self, obj_name):
        key_name = obj_name.replace("_block", "")  
        target_obj_name = key_name if key_name.endswith("mug") else f"{name_map.get(key_name, key_name)}_block"
        pos = self.mj_data.body(target_obj_name).xpos.copy()
        pos[2] -= 0.31
        quat = self.mj_data.body(target_obj_name).xquat.copy()
        return pos, quat

    @primitive
    def move(self, pos, quat):
        start_time = time.time()
        def checkArriveState(state):
            current_pos, current_quat = self.get_current_pose()
            error = np.sum(np.abs(state[:3] - current_pos)) + np.sum(np.abs(state[3:] - current_quat))
            error2 = 2*np.sum(np.abs(state[:3] - current_pos)) + np.sum(np.abs(state[3:] - current_quat)/2.5)        #run Simulation
            end_time = time.time()
            elapsed_time  = end_time - start_time
            # print("time:",elapsed_time)
            if error2 <= 0.05 or elapsed_time  > 30:
                return True
            return False

        while True:
            self.action = np.concatenate((pos, quat), axis=0)
            self.step(self.action)
            if self.render_mode == "human":
                self.render()
            if checkArriveState(self.action):
                break

    @primitive
    def grab(self, obj_name):
        self.gripper_ctrl("open")
        obj_pos, obj_quat = self.get_obj_pose(obj_name)
        self.move(np.add(obj_pos, np.array([0, 0, 0.1])), obj_quat)
        self.move(obj_pos, obj_quat)
        self.gripper_ctrl("close")
        end_pos, end_quat = self.get_current_pose()
        self.move(np.add(end_pos, np.array([0, 0, 0.1])), end_quat)

    @primitive
    def gripper_ctrl(self, cmd: str):
        if cmd == "open":
            self.mj_data.actuator("0_gripper_l_finger_joint").ctrl = 20
        elif cmd == "close":
            self.mj_data.actuator("0_gripper_l_finger_joint").ctrl = -20
        step = 0
        while True:
            step += 1
            self.step(self.action)
            if self.render_mode == "human":
                self.render()
            if step > 100:
                break
    @primitive       
    def get_gripper_status(self):
        """
        get gripper state
        
        :return: gripper state: "open" or "close"。
        """

        if self.mj_data.actuator("0_gripper_l_finger_joint").ctrl == 20:
            return "open"
        elif self.mj_data.actuator("0_gripper_l_finger_joint").ctrl == -20:
            return "close"
        else:
            return "initial"

    @primitive
    def get_current_pose(self):
        return self.controller.forward_kinematics(self.robot.get_arm_qpos())
    
    @primitive
    def say(self,conversation):
        print(conversation)


    @primitive
    def get_obj_mass(self, name: str) -> float:
        """ Get obj mass from obj name.

        :param name: obj name
        :return: obj mass
        """
        self.grab(name)
        self.mj_data.actuator("0_gripper_l_finger_joint").ctrl = 0
        # Get the object's ID
        body_id = self.mj_model.body(name).id
        # Get the object's mass
        body_mass = self.mj_model.body_mass[body_id]
        return body_mass



######################env1_skill_update#####################
    @primitive
    def move_gripper_orientation(self,direction,distance):
        """
        This function moves the gripper to the corresponding position based on direction and distance. The direction is chosen from 'forward', 'backward', 'left', 'right', 'upward', 'downward', and the distance is measured in centimeters.
        """
        current_pos, current_quat = self.get_current_pose()
        
        direction_map = {
            'forward': np.array([1, 0, 0]),
            'backward': np.array([-1, 0, 0]),
            'left': np.array([0, 1, 0]),
            'right': np.array([0, -1, 0]),
            'upward': np.array([0, 0, 1]),
            'downward': np.array([0, 0, -1])
        }
        
        if direction in direction_map:
            move_vector = direction_map[direction] * distance
        else:
            raise ValueError("Invalid direction")
        
        target_pos = current_pos + move_vector
        self.move(target_pos, current_quat)

    @primitive
    def stack_object_on_object(self, top_object_name, base_object_name):
        """
        This function stack top_object on base_object. It grabs the top_object, moves it above the base_object, and 
    then places it on the base_object.
        """
        # Grab the top block
        self.grab(top_object_name)

        # Get the position and quaternion of the base block
        base_pos, base_quat = self.get_obj_pose(base_object_name)

        # Calculate the new position for placing the top block on the base block
        new_pos = np.array([base_pos[0], base_pos[1], base_pos[2]])
        if "mug" in base_object_name:
            # Move the gripper (with the top block) to the position above the base block
            self.move(np.add(new_pos, np.array([0, 0, 0.15])), base_quat)
        else:
            self.move(np.add(new_pos, np.array([0, 0, 0.1])), base_quat)

        # # Place the top block on the base block
        # self.move(new_pos, base_quat)

        # Release the top block
        self.gripper_ctrl("open")

        # # Move the gripper slightly up after placing the block
        # self.move(np.add(new_pos, np.array([0, 0, 0.1])), base_quat)

    @primitive
    def pick_and_place_next_to(self, obj_to_pick, obj_reference, direction, distance):
        """
        Picks up an object and places it next to another object in the specified direction and distance.        

        Parameters:
            obj_to_pick (str): Name of the object to pick.
            obj_reference (str): Name of the reference object next to which the picked object will be placed.   
            direction (str): Direction to place the picked object relative to the reference object. Options: 'left', 'right', 'forward', 'backward'.
            distance (float): Distance in meters from the reference object.
        """
        self.grab(obj_to_pick)
        reference_pos, reference_quat = self.get_obj_pose(obj_reference)

        direction_map = {
            'left': np.array([0, 1, 0]),
            'right': np.array([0, -1, 0]),
            'forward': np.array([1, 0, 0]),
            'backward': np.array([-1, 0, 0])
        }

        if direction in direction_map:
            displacement = direction_map[direction] * distance
        else:
            raise ValueError("Invalid direction")

        place_position = reference_pos + displacement
        self.move(np.add(place_position, np.array([0, 0, 0.1])), reference_quat)
        self.gripper_ctrl("open")
    
######################env2_skill_update#####################
    @primitive       
    def get_sorted_weight_block_names(self):
        """ 
        Get the names of blocks sorted by their weight in ascending order. 
        """
        # Get the mass of each block
        block_masses = {
            'block1': self.get_obj_mass('block1'),
            'block2': self.get_obj_mass('block2'),
            'block3': self.get_obj_mass('block3'),
            'block4': self.get_obj_mass('block4')
        }
        
        # Sort the blocks by mass
        sorted_blocks = sorted(block_masses.items(), key=lambda x: x[1])
        
        # Extract the block names in sorted order
        lightest_movable_block = sorted_blocks[0][0]
        medium_weight_movable_block = sorted_blocks[1][0]
        heaviest_movable_block = sorted_blocks[2][0]
        fixed_block = sorted_blocks[3][0]
        
        # Return the sorted block names
        return lightest_movable_block, medium_weight_movable_block, heaviest_movable_block, fixed_block



def make_env():
    env = GraspingEnv(
        render_mode="human",
        control_freq=200,
    )
    return env
