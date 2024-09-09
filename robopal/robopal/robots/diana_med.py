import os

from robopal.robots.base import *

ASSET_DIR = os.path.join(os.path.dirname(__file__), '../assets')


class DianaMed(BaseRobot):
    """ DianaMed robot base class. """
    def __init__(self,
                 scene='default',
                 manipulator='DianaMed',
                 gripper=None,
                 mount=None
                 ):
        super().__init__(
            name="diana_med",
            scene=scene,
            chassis=mount,
            manipulator=manipulator,
            gripper=gripper,
            attached_body='0_attachment',
        )
        self.arm_joint_names = {self.agents[0]: ['0_j1', '0_j2', '0_j3', '0_j4', '0_j5', '0_j6', '0_j7']}
        self.arm_actuator_names = {self.agents[0]: ['0_a1', '0_a2', '0_a3', '0_a4', '0_a5', '0_a6', '0_a7']}
        self.base_link_name = {self.agents[0]: '0_base_link'}
        self.end_name = {self.agents[0]: '0_link7'}

    @property
    def init_qpos(self):
        """ Robot's init joint position. """
        return {self.agents[0]: np.array([0.0, -np.pi / 4.0, 0.0, np.pi / 2.0, 0.00, np.pi / 4.0, 0.0])}

class DianaGrasp(DianaMed):
    def __init__(self, scene='grasping', gripper='rethink_gripper', mount='top_point'):
        super().__init__(scene=scene, gripper=gripper, mount=mount)

    def add_assets(self):
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/green_cube.xml')

        goal_site = """<site name="goal_site" pos="0.4 0.0 0.5" size="0.02 0.02 0.02" rgba="1 0 0 1" type="sphere" />"""
        self.mjcf_generator.add_node_from_str('worldbody', goal_site)

    @property
    def init_qpos(self):
        """ Robot's init joint position. """
        return {self.agents[0]: np.array([0.02167871, -0.16747492, 0.00730963, 2.5573341, -0.00401727, -0.42203728, -0.01099269])}


class DianaGraspMultiObjs(DianaGrasp):
            
    def add_assets(self):
        # 设置随机种子
        np.random.seed(42)
        
        # 定义生成随机位置和姿态的函数
        def generate_random_pose():
            random_x_pos = np.random.uniform(0.35, 0.85)
            random_y_pos = np.random.uniform(-0.25, 0.25)
            random_quat = np.random.uniform(-0.5, 0.5)
            return random_x_pos, random_y_pos, random_quat
        
        # 生成红色块的随机位置和姿态
        random_x_pos_red, random_y_pos_red, random_quat_red = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/red_cube.xml')
        pos_str_red = f"{random_x_pos_red} {random_y_pos_red} 0.44098543"
        quat_str_red = f"1 0 0 {random_quat_red}"
        self.mjcf_generator.set_node_attrib('body', 'red_block', {'pos': pos_str_red, 'quat': quat_str_red})
        
        # 生成绿色块的随机位置和姿态
        random_x_pos_green, random_y_pos_green, random_quat_green = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_green, random_y_pos_green]):
            random_x_pos_green, random_y_pos_green, random_quat_green = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/green_cube.xml')
        pos_str_green = f"{random_x_pos_green} {random_y_pos_green} 0.44098543"
        quat_str_green = f"1 0 0 {random_quat_green}"
        self.mjcf_generator.set_node_attrib('body', 'green_block', {'pos': pos_str_green, 'quat': quat_str_green})
        
        # 生成蓝色块的随机位置和姿态
        random_x_pos_blue, random_y_pos_blue, random_quat_blue = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_blue, random_y_pos_blue]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_blue, random_y_pos_blue]):
            random_x_pos_blue, random_y_pos_blue, random_quat_blue = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/blue_cube.xml')
        pos_str_blue = f"{random_x_pos_blue} {random_y_pos_blue} 0.44098543"
        quat_str_blue = f"1 0 0 {random_quat_blue}"
        self.mjcf_generator.set_node_attrib('body', 'blue_block', {'pos': pos_str_blue, 'quat': quat_str_blue})
        
        # 生成黄色块的随机位置和姿态
        random_x_pos_yellow, random_y_pos_yellow, random_quat_yellow = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_yellow, random_y_pos_yellow]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_yellow, random_y_pos_yellow]) or \
              self.check_distance([random_x_pos_blue, random_y_pos_blue], [random_x_pos_yellow, random_y_pos_yellow]):
            random_x_pos_yellow, random_y_pos_yellow, random_quat_yellow = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/yellow_cube.xml')
        pos_str_yellow = f"{random_x_pos_yellow} {random_y_pos_yellow} 0.44098543"
        quat_str_yellow = f"1 0 0 {random_quat_yellow}"
        self.mjcf_generator.set_node_attrib('body', 'yellow_block', {'pos': pos_str_yellow, 'quat': quat_str_yellow})
        
        # 生成白色杯子的随机位置
        random_x_pos_white, random_y_pos_white, random_quat_white = generate_random_pose()
        while self.check_distance2([random_x_pos_red, random_y_pos_red], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_green, random_y_pos_green], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_blue, random_y_pos_blue], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_yellow, random_y_pos_yellow], [random_x_pos_white, random_y_pos_white]):
            random_x_pos_white, random_y_pos_white, random_quat_white = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/white_mug.xml')
        pos_str_white = f"{random_x_pos_white} {random_y_pos_white} 0.42"
        quat_str_white = f"1 0 0 {random_quat_white}"
        self.mjcf_generator.set_node_attrib('body', 'white_mug', {'pos': pos_str_white, 'quat': quat_str_white})

        
        # 生成黑色杯子的随机位置
        random_x_pos_black, random_y_pos_black, random_quat_black = generate_random_pose()
        while self.check_distance2([random_x_pos_red, random_y_pos_red], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_green, random_y_pos_green], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_blue, random_y_pos_blue], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_yellow, random_y_pos_yellow], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_white, random_y_pos_white], [random_x_pos_black, random_y_pos_black]):
            random_x_pos_black, random_y_pos_black, random_quat_black = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/black_mug.xml')
        pos_str_black = f"{random_x_pos_black} {random_y_pos_black} 0.42"
        quat_str_black = f"1 0 0 {random_quat_black}"
        self.mjcf_generator.set_node_attrib('body', 'black_mug', {'pos': pos_str_black, 'quat': quat_str_black})

        # set realsense_d435
        self.mjcf_generator.add_mesh(name="cambase", file="objects/realsense_d435/meshes/cambase.STL")
        self.mjcf_generator.add_mesh(name="cam", file="objects/realsense_d435/meshes/cam.STL")

        cam = """<body pos="1.0 0.0 0.8" euler="0 0.785 3.14">
        <include file="objects/realsense_d435/realsense.xml"/>
    </body>"""
        self.mjcf_generator.add_node_from_str('worldbody', cam)
        
        # r_goal_site = """<site name="red_goal" pos="0.4325104758653856 -0.09577637024299157 0.44098542724196255" size="0.02 0.02 0.02" rgba="1 0 0 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', r_goal_site)

        # g_goal_site = """<site name="green_goal" pos="0.4 -0.1 0.5" size="0.01 0.01 0.01" rgba="0 1 0 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', g_goal_site)

        # b_goal_site = """<site name="blue_goal" pos="0.4 0.1 0.5" size="0.01 0.01 0.01" rgba="0 0 1 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', b_goal_site)

        # y_goal_site = """<site name="yellow_goal" pos="0.4 0.1 0.5" size="0.01 0.01 0.01" rgba="0 0 1 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', y_goal_site)
        
    def check_distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2)) < 0.03
    def check_distance2(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2)) < 0.07
    

class DianaGraspMultiObjs_Partobservable(DianaGrasp):

    def add_assets(self):
        # 设置随机种子
        np.random.seed(42)
        
        # 定义生成随机位置和姿态的函数
        def generate_random_pose():
            random_x_pos = np.random.uniform(0.35, 0.85)
            random_y_pos = np.random.uniform(-0.25, 0.25)
            random_quat = np.random.uniform(-0.5, 0.5)
            return random_x_pos, random_y_pos, random_quat
        

        # 生成块1的随机位置和姿态
        random_x_pos_block1, random_y_pos_block1, random_quat_block1 = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/cube1.xml')
        pos_str_block1 = f"{random_x_pos_block1} {random_y_pos_block1} 0.44098543"
        quat_str_block1 = f"1 0 0 {random_quat_block1}"
        self.mjcf_generator.set_node_attrib('body', 'block1', {'pos': pos_str_block1, 'quat': quat_str_block1})
        
        # 生成块2的随机位置和姿态
        random_x_pos_block2, random_y_pos_block2, random_quat_block2 = generate_random_pose()
        while self.check_distance([random_x_pos_block1, random_y_pos_block1], [random_x_pos_block2, random_y_pos_block2]):
            random_x_pos_block2, random_y_pos_block2, random_quat_block2 = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/cube2.xml')
        pos_str_block2 = f"{random_x_pos_block2} {random_y_pos_block2} 0.44098543"
        quat_str_block2 = f"1 0 0 {random_quat_block2}"
        self.mjcf_generator.set_node_attrib('body', 'block2', {'pos': pos_str_block2, 'quat': quat_str_block2})
        
        # 生成块3的随机位置和姿态
        random_x_pos_block3, random_y_pos_block3, random_quat_block3 = generate_random_pose()
        while self.check_distance([random_x_pos_block1, random_y_pos_block1], [random_x_pos_block3, random_y_pos_block3]) or \
              self.check_distance([random_x_pos_block2, random_y_pos_block2], [random_x_pos_block3, random_y_pos_block3]):
            random_x_pos_block3, random_y_pos_block3, random_quat_block3 = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/cube3.xml')
        pos_str_block3 = f"{random_x_pos_block3} {random_y_pos_block3} 0.44098543"
        quat_str_block3 = f"1 0 0 {random_quat_block3}"
        self.mjcf_generator.set_node_attrib('body', 'block3', {'pos': pos_str_block3, 'quat': quat_str_block3})
        
        # 生成块4的随机位置和姿态
        random_x_pos_block4, random_y_pos_block4, random_quat_block4 = generate_random_pose()
        while self.check_distance([random_x_pos_block1, random_y_pos_block1], [random_x_pos_block4, random_y_pos_block4]) or \
              self.check_distance([random_x_pos_block2, random_y_pos_block2], [random_x_pos_block4, random_y_pos_block4]) or \
              self.check_distance([random_x_pos_block3, random_y_pos_block3], [random_x_pos_block4, random_y_pos_block4]):
            random_x_pos_block4, random_y_pos_block4, random_quat_block4 = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/cube4.xml')
        pos_str_block4 = f"{random_x_pos_block4} {random_y_pos_block4} 0.44098543"
        quat_str_block4 = f"1 0 0 {random_quat_block4}"
        self.mjcf_generator.set_node_attrib('body', 'block4', {'pos': pos_str_block4, 'quat': quat_str_block4})
        
        # 生成白色杯子的随机位置
        random_x_pos_white, random_y_pos_white, random_quat_white = generate_random_pose()
        while self.check_distance2([random_x_pos_block1, random_y_pos_block1], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_block2, random_y_pos_block2], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_block3, random_y_pos_block3], [random_x_pos_white, random_y_pos_white]) or \
              self.check_distance2([random_x_pos_block4, random_y_pos_block4], [random_x_pos_white, random_y_pos_white]):
            random_x_pos_white, random_y_pos_white, random_quat_white = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/white_mug.xml')
        pos_str_white = f"{random_x_pos_white} {random_y_pos_white} 0.42"
        quat_str_white = f"1 0 0 {random_quat_white}"
        self.mjcf_generator.set_node_attrib('body', 'white_mug', {'pos': pos_str_white, 'quat': quat_str_white})

        
        # 生成黑色杯子的随机位置
        random_x_pos_black, random_y_pos_black, random_quat_black = generate_random_pose()
        while self.check_distance2([random_x_pos_block1, random_y_pos_block1], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_block2, random_y_pos_block2], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_block3, random_y_pos_block3], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_block4, random_y_pos_block4], [random_x_pos_black, random_y_pos_black]) or \
              self.check_distance2([random_x_pos_white, random_y_pos_white], [random_x_pos_black, random_y_pos_black]):
            random_x_pos_black, random_y_pos_black, random_quat_black = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/black_mug.xml')
        pos_str_black = f"{random_x_pos_black} {random_y_pos_black} 0.42"
        quat_str_black = f"1 0 0 {random_quat_black}"
        self.mjcf_generator.set_node_attrib('body', 'black_mug', {'pos': pos_str_black, 'quat': quat_str_black})

        # set realsense_d435
        self.mjcf_generator.add_mesh(name="cambase", file="objects/realsense_d435/meshes/cambase.STL")
        self.mjcf_generator.add_mesh(name="cam", file="objects/realsense_d435/meshes/cam.STL")

        cam = """<body pos="1.0 0.0 0.8" euler="0 0.785 3.14">
        <include file="objects/realsense_d435/realsense.xml"/>
    </body>"""
        self.mjcf_generator.add_node_from_str('worldbody', cam)
        
        # r_goal_site = """<site name="red_goal" pos="0.4325104758653856 -0.09577637024299157 0.44098542724196255" size="0.02 0.02 0.02" rgba="1 0 0 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', r_goal_site)

        # g_goal_site = """<site name="green_goal" pos="0.4 -0.1 0.5" size="0.01 0.01 0.01" rgba="0 1 0 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', g_goal_site)

        # b_goal_site = """<site name="blue_goal" pos="0.4 0.1 0.5" size="0.01 0.01 0.01" rgba="0 0 1 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', b_goal_site)

        # y_goal_site = """<site name="yellow_goal" pos="0.4 0.1 0.5" size="0.01 0.01 0.01" rgba="0 0 1 1" type="sphere" />"""
        # self.mjcf_generator.add_node_from_str('worldbody', y_goal_site)
        
    def check_distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2)) < 0.03
    def check_distance2(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2)) < 0.07


class DianaGrasp_kh(DianaGrasp):

    def add_assets(self):
        # 设置随机种子
        np.random.seed(42)
        
        # 定义生成随机位置和姿态的函数
        def generate_random_pose():
            random_x_pos = np.random.uniform(0.35, 0.85)
            random_y_pos = np.random.uniform(-0.25, 0.25)
            random_quat = np.random.uniform(-0.5, 0.5)
            return random_x_pos, random_y_pos, random_quat
        
        # 生成红色块的随机位置和姿态
        random_x_pos_red, random_y_pos_red, random_quat_red = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/red_cube.xml')
        pos_str_red = f"{random_x_pos_red} {random_y_pos_red} 0.44098543"
        quat_str_red = f"1 0 0 {random_quat_red}"
        self.mjcf_generator.set_node_attrib('body', 'red_block', {'pos': pos_str_red, 'quat': quat_str_red})
        
        # 生成绿色块的随机位置和姿态
        random_x_pos_green, random_y_pos_green, random_quat_green = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_green, random_y_pos_green]):
            random_x_pos_green, random_y_pos_green, random_quat_green = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/green_cube.xml')
        pos_str_green = f"{random_x_pos_green} {random_y_pos_green} 0.44098543"
        quat_str_green = f"1 0 0 {random_quat_green}"
        self.mjcf_generator.set_node_attrib('body', 'green_block', {'pos': pos_str_green, 'quat': quat_str_green})
        
        # 生成蓝色块的随机位置和姿态
        random_x_pos_blue, random_y_pos_blue, random_quat_blue = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_blue, random_y_pos_blue]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_blue, random_y_pos_blue]):
            random_x_pos_blue, random_y_pos_blue, random_quat_blue = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/blue_cube.xml')
        pos_str_blue = f"{random_x_pos_blue} {random_y_pos_blue} 0.44098543"
        quat_str_blue = f"1 0 0 {random_quat_blue}"
        self.mjcf_generator.set_node_attrib('body', 'blue_block', {'pos': pos_str_blue, 'quat': quat_str_blue})
        
        # 生成黄色块的随机位置和姿态
        random_x_pos_yellow, random_y_pos_yellow, random_quat_yellow = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_yellow, random_y_pos_yellow]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_yellow, random_y_pos_yellow]) or \
              self.check_distance([random_x_pos_blue, random_y_pos_blue], [random_x_pos_yellow, random_y_pos_yellow]):
            random_x_pos_yellow, random_y_pos_yellow, random_quat_yellow = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/yellow_cube.xml')
        pos_str_yellow = f"{random_x_pos_yellow} {random_y_pos_yellow} 0.44098543"
        quat_str_yellow = f"1 0 0 {random_quat_yellow}"
        self.mjcf_generator.set_node_attrib('body', 'yellow_block', {'pos': pos_str_yellow, 'quat': quat_str_yellow})

        # 生成黑色环的随机位置和姿态
        random_x_pos_black_ring, random_y_pos_black_ring, random_quat_black_ring = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_black_ring, random_y_pos_black_ring]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_black_ring, random_y_pos_black_ring]) or \
              self.check_distance([random_x_pos_blue, random_y_pos_blue], [random_x_pos_black_ring, random_y_pos_black_ring]):
            random_x_pos_black_ring, random_y_pos_black_ring, random_quat_black_ring = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/black_ring.xml')
        pos_str_ring = f"{random_x_pos_black_ring} {random_y_pos_black_ring} 0.43098543"
        quat_str_ring = f"1 0 0 {random_quat_black_ring}"
        self.mjcf_generator.set_node_attrib('body', 'black_ring', {'pos': pos_str_ring, 'quat': quat_str_ring})
    
        # 生成白色环的随机位置和姿态
        random_x_pos_white_ring, random_y_pos_white_ring, random_quat_white_ring = generate_random_pose()
        while self.check_distance([random_x_pos_red, random_y_pos_red], [random_x_pos_white_ring, random_y_pos_white_ring]) or \
              self.check_distance([random_x_pos_green, random_y_pos_green], [random_x_pos_white_ring, random_y_pos_white_ring]) or \
              self.check_distance([random_x_pos_blue, random_y_pos_blue], [random_x_pos_white_ring, random_y_pos_white_ring]) or \
              self.check_distance([random_x_pos_black_ring, random_y_pos_black_ring], [random_x_pos_white_ring, random_y_pos_white_ring]) :
            random_x_pos_white_ring, random_y_pos_white_ring, random_quat_white_ring = generate_random_pose()
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/white_ring.xml')
        pos_str_ring = f"{random_x_pos_white_ring} {random_y_pos_white_ring} 0.43098543"
        quat_str_ring = f"1 0 0 {random_quat_white_ring}"
        self.mjcf_generator.set_node_attrib('body', 'white_ring', {'pos': pos_str_ring, 'quat': quat_str_ring})

        # set realsense_d435
        self.mjcf_generator.add_mesh(name="cambase", file="objects/realsense_d435/meshes/cambase.STL")
        self.mjcf_generator.add_mesh(name="cam", file="objects/realsense_d435/meshes/cam.STL")

        cam = """<body pos="1.0 0.0 0.8" euler="0 0.785 3.14">
        <include file="objects/realsense_d435/realsense.xml"/>
    </body>"""
        self.mjcf_generator.add_node_from_str('worldbody', cam)

    def check_distance(self, pos1, pos2):
        return np.linalg.norm(np.array(pos1) - np.array(pos2)) < 0.03
    

class DianaGrasp_am(DianaGrasp):
    def __init__(self):
        super().__init__(scene='grasping_am', gripper='rethink_gripper', mount='top_point')

    def add_assets(self):
        
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/xuewei1.xml')
        pos_str_red = f"0.475 -0.055 0.43"
        quat_str_red = f"1 0 0 0"
        self.mjcf_generator.set_node_attrib('body', '心俞穴', {'pos': pos_str_red, 'quat': quat_str_red})

        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/xuewei2.xml')
        pos_str_red = f"0.352 0.055 0.43"
        quat_str_red = f"1 0 0 0"
        self.mjcf_generator.set_node_attrib('body', '肺俞穴', {'pos': pos_str_red, 'quat': quat_str_red})

        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/xuewei3.xml')
        pos_str_red = f"0.752 0.055 0.43"
        quat_str_red = f"1 0 0 0"
        self.mjcf_generator.set_node_attrib('body', '肝俞穴', {'pos': pos_str_red, 'quat': quat_str_red})

        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/xuewei4.xml')
        pos_str_red = f"0.210 -0.170 0.43"
        quat_str_red = f"1 0 0 0"
        self.mjcf_generator.set_node_attrib('body', '肩俞穴', {'pos': pos_str_red, 'quat': quat_str_red})

        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/xuewei5.xml')
        pos_str_red = f"0.885 -0.055 0.43"
        quat_str_red = f"1 0 0 0"
        self.mjcf_generator.set_node_attrib('body', '脾俞穴', {'pos': pos_str_red, 'quat': quat_str_red})


        # set realsense_d435
        self.mjcf_generator.add_mesh(name="cambase", file="objects/realsense_d435/meshes/cambase.STL")
        self.mjcf_generator.add_mesh(name="cam", file="objects/realsense_d435/meshes/cam.STL")

        cam = """<body pos="1.0 0.0 0.8" euler="0 0.785 3.14">
        <include file="objects/realsense_d435/realsense.xml"/>
    </body>"""
        self.mjcf_generator.add_node_from_str('worldbody', cam)
