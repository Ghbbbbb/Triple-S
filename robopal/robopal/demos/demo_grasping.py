import numpy as np
import time

from robopal.envs import RobotEnv
from robopal.robots.diana_med import DianaGraspMultiObjs


class GraspingEnv(RobotEnv):

    def __init__(self,
                 robot=DianaGraspMultiObjs(),
                 render_mode='human',
                 control_freq=200,
                 enable_camera_viewer=True,
                 controller='CARTIK',
                 is_interpolate=False,
                camera_name='cam'
                 ):
        super().__init__(
            robot=robot,
            render_mode=render_mode,
            control_freq=control_freq,
            enable_camera_viewer=enable_camera_viewer,
            controller=controller,
            is_interpolate=is_interpolate,
            camera_name=camera_name
        )
        

if __name__ == "__main__":
    env = GraspingEnv()
    env.reset()

    # def move(pos, quat):
    #     def checkArriveState(state):
    #         current_pos, current_quat = env.controller.forward_kinematics(env.robot.get_arm_qpos())
    #         print(current_pos,current_quat)
    #         print(state[:3],state[3:])
    #         error = np.sum(np.abs(state[:3] - current_pos)) + np.sum(np.abs(state[3:] - current_quat))
    #         print(current_pos)
    #         print(error)
    #         if error <= 0.02:
    #             return True
    #         return False

    #     while True:
    #         env.action = np.concatenate((pos, quat), axis=0)
    #         env.step(env.action)
    #         if env.render_mode == "human":
    #             env.render()
    #         if checkArriveState(env.action):
    #             break
    

    # move([0.5,0.1,0.21],[1,0,0,0])
    obj_name = "red_block"
    print(env.get_body_pos(obj_name))
    # env.set_object_pose("red_block:joint",np.array([0.5,-0.1,0.46,1,0,0,0.5]))
    action = env.get_body_pos(obj_name) - np.array([0.0, 0.00, 0.2])
    

    for t in range(int(100)):  #夹爪打开，HOME移动到过渡点
        env.mj_data.actuator('0_gripper_l_finger_joint').ctrl[0] = 0.03
        env.mj_data.actuator('0_gripper_r_finger_joint').ctrl[0] = 0.03
        env.step(np.concatenate([action, np.array([1, 0, 0, 0.5])]))
    action = env.get_body_pos(obj_name) - np.array([0.0, 0.00, 0.32])

    for t in range(int(100)):  #夹爪打开，过渡点到抓取点
        env.step(np.concatenate([action, np.array([1, 0, 0, 0.5])]))

    for t in range(int(100)):   #夹爪关闭
        env.mj_data.actuator('0_gripper_l_finger_joint').ctrl[0] = -0.02
        env.mj_data.actuator('0_gripper_r_finger_joint').ctrl[0] = -0.02
        env.step(np.concatenate([action, np.array([1, 0, 0, 0.5])]))
    action = env.get_body_pos(obj_name)

    for t in range(int(100)):  #夹爪关闭，上升到过渡点
        env.step(np.concatenate([action, np.array([1, 0, 0, 0.5])]))
    
    action = env.get_body_pos("white_mug") - np.array([0.0, 0.00, 0.15])
    for t in range(int(100)):  
        env.step(np.concatenate([action, np.array([1, 0, 0, 0])]))
    for t in range(int(100)):  
        env.mj_data.actuator('0_gripper_l_finger_joint').ctrl[0] = 0.03
        env.mj_data.actuator('0_gripper_r_finger_joint').ctrl[0] = 0.03
        env.step(np.concatenate([action, np.array([1, 0, 0, 0])]))
        action = env.get_body_pos("white_mug")
    print(env.get_body_pos(obj_name))
    env.close()
