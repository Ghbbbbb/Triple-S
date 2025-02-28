<h1 align="center">
Long-horizon Desktop Abstract Placement
</h1>
This is a Long-horizon Desktop Implicative Placement(LDIP) dataset, which is based on the Robopal simulation environment (`robopal`), and includes both observable and partially abservable scenarios, as shown in figure below. The observable environment contains 500 tasks, with more than half involving instruction implication, which reasoning on relative positioning, color, and geometry. It includes four differently colored and shaped blocks and two differently colored cups. In this scenario, the LLM needs to simplify the instructions to correctly match objects in the instructions with those in the environment. In the partially observable environment, there are 97 tasks involving environment implication, with three movable blocks of different weights, one fixed block, and two different colored cups. In this case, standard visual detection models cannot differentiate the blocks, requiring the use of a gravity sensor, which adds to the LLM’s code prediction burden.


![Introduction of LDIP](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/LDIP.png)

### An Example
![Example of LDIP](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/Example.png)

### 1.Explanation of each JSON file:

- **LDIP1.json**: Includes a total of 500 data points in the observable environment. Each sample is structured as follows:
```
{
    "instruction": str,     # User-inputted instruction
    "code": str,            # Corresponding policy code
    "goal_pos": str,        # The ground truth state of object and gripper
    "task": str             # Type of task, categorized as "Short_step_no_inference", "Short_step_with_inference", "Long_step_no_inference", "Long_step_with_inference"
}
```

- **LDIP2.json**: Includes a total of 97 data points in the partially abservable environment. Each sample is structured as follows:
```
{
    "instruction": str,     # User-inputted instruction
    "code": str,            # Corresponding policy code
    "goal_pos": str,        # The ground truth state of object and gripper
}
```

### 2.Explanation of high-level API:

**pri.gripper_ctrl(command)**: Ctrl the gripper, param 'command' is a string type, consist of 'open' and 'close'.

**pri.move(position, quaternion)**: Move the end-effector/gripper to the target position and quaternion. The func takes 2 parameters as input, first param 'position' means the target position, second param 'quaternion' means the target quaternion. Both of them are type ndarray.

**pri.get_current_pose()**: Get current pose of the gripper, This func will return 2 parameters, the position and quaternion of the end gripper.

**pri.get_obj_pose(object_name: str)**: Get current pose of the object, This func will return 2 parameters, the position and quaternion of the object. Example: `object_pos, object_quat = pri.get_obj_pose("object_name")`

**pri.reset_robot()**: Reset the robot to initial pose or home pose, you should call it upon task completion, unless the task explicitly specifies moving the gripper to a designated position.

**pri.grab(object_name: str)**: Grab specified object according to the input name.

**pri.get_obj_mass(self, name: str)**: Get the mass of the object.

**pri.say(content:str)**: Say something if you don't understand the command.