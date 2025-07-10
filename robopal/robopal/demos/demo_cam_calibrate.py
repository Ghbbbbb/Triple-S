import numpy as np
import json
import logging

from robopal.envs.robot import RobotEnv
import robopal.commons.cv_utils as cv
from robopal.robots.diana_med import DianaCalib,DianaGraspMultiObjs


class CamCalibEnv(RobotEnv):
    """ Camera calibration environment.
    In this case, we will show the detail process of hand-eye calibration.
    Press 'Enter' to take a picture.
    """
    def __init__(self,
                 robot=None,
                 render_mode='human',
                 control_freq=200,
                 controller='CARTIK',
                 is_interpolate=False,
                 enable_camera_viewer=True,
                 camera_name=None
                 ):
        super().__init__(
            robot=robot,
            render_mode=render_mode,
            control_freq=control_freq,
            controller=controller,
            is_interpolate=is_interpolate,
            enable_camera_viewer=enable_camera_viewer,
            camera_name=camera_name,
        )
        # Set low damping for easily dragging the end.
        self.controller.set_jnt_params(
            b=6.0 * np.ones(7),
            k=100.0 * np.ones(7),
        )
        self.camera_intrinsic_matrix = cv.get_cam_intrinsic()
        self.distCoeffs = np.zeros(5)
        print(self.camera_intrinsic_matrix)

    def step(self, action=None):
        action = self.robot.get_arm_qpos()
        return super().step(action)



if __name__ == "__main__":

    env = CamCalibEnv(
        robot=DianaGraspMultiObjs(),
        render_mode='human',
        control_freq=200,
        controller='JNTIMP',
        is_interpolate=False,
        enable_camera_viewer=True,
        camera_name='cam'
    )
    env.reset()
    # obj_name = "red_block"
    # # print(env.get_body_pos(obj_name))
    # # env.set_object_pose("red_block:joint",np.array([0.5,-0.1,0.46,1,0,0,0.5]))
    # action = env.get_body_pos(obj_name) - np.array([0.0, 0.00, 0.2])
    

    # for t in range(int(100)):  #夹爪打开，HOME移动到过渡点
    #     env.mj_data.actuator('0_gripper_l_finger_joint').ctrl[0] = 0.03
    #     env.mj_data.actuator('0_gripper_r_finger_joint').ctrl[0] = 0.03
    #     env.step(np.concatenate([action, np.array([1, 0, 0, 0.5])]))
    # action = env.get_body_pos(obj_name) - np.array([0.0, 0.00, 0.32])
    for t in range(int(1e6)):
        env.step()
