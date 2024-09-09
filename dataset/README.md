<h1 align="center">
Desktop Cube Placement Dataset
</h1>

This is a dataset for machine-assisted hospital item transport, known as the Hospital Item Transport Dataset (HITD). It takes natural language instructions as input and generates low-level code to facilitate item transport tasks in a hospital setting. We provide both Chinese(`zh`) and English(`en`) versions of the HITD dataset for research purposes. It is important to note that all results discussed in this document are derived from the Chinese(`zh`) dataset. Additionally, within this project, we offer 1-shot English prompt (`prompt/en`) for researchers to validate results.

Each natural language instruction consists of three components: [*originating department*, *intermediate transport department*, *final destination department*]. The *originating department* and *intermediate transport department* are selected from a list of 10 common hospital departments, and the *final destination department* is chosen from "Logistics" or "General Services".
![Introduction of HITD](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/DCPD.png)
## 1.Explanation of high-level API:

**pri.gripper_ctrl(command)**: Ctrl the gripper, param 'command' is a string type, consist of 'open' and 'close'.

**pri.move(position, quaternion)**: Move the end-effector/gripper to the target position and quaternion. The func takes 2 parameters as input, first param 'position' means the target position, second param 'quaternion' means the target quaternion. Both of them are type ndarray.

**pri.get_current_pose()**: Get current pose of the gripper, This func will return 2 parameters, the position and quaternion of the end gripper.

**pri.get_obj_pose(object_name: str)**: Get current pose of the object, This func will return 2 parameters, the position and quaternion of the object. Example: `object_pos, object_quat = pri.get_obj_pose("object_name")`

**pri.reset_robot()**: Reset the robot to initial pose or home pose, you should call it upon task completion, unless the task explicitly specifies moving the gripper to a designated position.

**pri.grab(object_name: str)**: Grab specified object according to the input name.

**pri.say(content:str)**: Say something if you don't understand the command.


### Explanation of each JSON file:

- **dcpd1.json**: Contains the complete HITD dataset with 1000 samples. Each sample is structured as follows:
```
{
    "instruction": str,     # User-inputted instruction
    "code": str,            # Corresponding policy code
    "goal_pos": str,        # The ground truth state of object and gripper
    "task": int             # Type of task, categorized as Short_step_no_inference, Short_step_with_inference, Long_step_no_inference, Long_step_with_inference
}
```

- **dcpd1-1.json**: Subset of HITD dataset containing samples with "task" as "Multi_department" (325 samples). Average code length is 399 characters, with 1-4 *originating departments* and 1-5 *intermediate transport departments*, without priority.

- **dcpd1-2.json**: Subset of HITD dataset containing samples with "task" as "Multi_department_priority" (331 samples). Average code length is 371 characters, with 1-4 *originating departments* and 1-5 *intermediate transport departments*, with priority.

- **dcpd1-3.json**: Subset of HITD dataset containing samples with "task" as "Single_department" (344 samples). Average code length is 202 characters, with 1 *originating department* and 1-9 *intermediate transport departments*, without priority.

- **dcpd1-4.json**: 200 randomly selected samples from HITD dataset, serving as test samples without noise interference.

- **dcpd2.json**: Perturbed version of HITD_no_noise.json with noise, which includes changes in expression while retaining the overall meaning (e.g., synonym substitution, rephrasing of sentence structure).
