<h1 align="center">
Long-horizon Desktop Implicative Placement (LDIP)
</h1>
This is a Long-horizon Desktop Implicative Placement(LDIP) dataset, which is based on the Robopal simulation environment (`robopal`), and includes both observable and partially abservable scenarios, as shown in figure below. The observable environment contains 500 tasks, with more than half involving instruction implication, which reasoning on relative positioning, color, and geometry. It includes four differently colored and shaped blocks and two differently colored cups. In this scenario, the LLM needs to simplify the instructions to correctly match objects in the instructions with those in the environment. In the partially observable environment, there are 97 tasks involving environment implication, with three movable blocks of different weights, one fixed block, and two different colored cups. In this case, standard visual detection models cannot differentiate the blocks, requiring the use of a gravity sensor, which adds to the LLM’s code prediction burden.

![LDIP Introduction](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/LDIP.png)


## Dataset Versions
| Version | File | Scenarios | Tasks | Description |
|---------|------|-----------|-------|-------------|
| v1 | `LDIP1_v1.json` | Observable | 224 | Initial version|
| v2 | `LDIP1_v2.json` | Observable | 500 | Extended version|
| - | `LDIP2.json` | Partially Observable | 97 | Stable version |

## Environment Specifications
- **Observable (LDIP1)**:
  - 4 colored/shaped blocks + 2 colored cups
  - more than 50% tasks require instruction implication
  - Reasoning dimensions: relative positioning, color, geometry

- **Partially Observable (LDIP2)**:
  - 3 weighted blocks (movable) + 1 fixed block + 2 colored cups
  - 97 environment implication tasks
  - Requires gravity sensor (beyond standard vision)

## An Example
![Task Example](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/Example.png)

## Data Structure
### 1.All JSON files follow this schema:
```bash
{
    "instruction": str,     // Natural language instruction
    "code": str,            // Executable policy code
    "goal_pos": str         // Ground truth object/gripper states
}
```

### 2.Explanation of high-level API in code:


| Function | Description | Returns |
|----------|-------------|---------|
| **pri.gripper_ctrl(command: str)** | Control the gripper state.<br>• Valid commands: `'open'` \| `'close'` | `None` |
| **pri.move(position: ndarray, quaternion: ndarray)** | Move end-effector to target pose.<br>• `position`: [x,y,z] coordinates (meters)<br>• `quaternion`: [w,x,y,z] orientation | `None` |
| **pri.get_current_pose()** | Get current gripper pose.<br>• Position relative to world frame<br>| `(pos: ndarray, quat: ndarray)` |
| **pri.get_obj_pose(object_name: str)** | Get object's current pose.<br>• `object_name`: Must match scene object ID<br>• Example: `"red_block"`, `"white_mug"` | `(pos: ndarray, quat: ndarray)` |
| **pri.reset_robot()** | Reset robot to home position.<br>• Should be called at the end of the task unless specified otherwise| `None` |
| **pri.grab(object_name: str)** | Execute grasp action on target object.<br>• Auto-completes approach-grasp sequence| `None` |
| **pri.get_obj_mass(name: str)** | Query object mass (kg).<br>• Critical for LDIP2 weight-implication tasks<br>• Example: `pri.get_obj_mass("block1")` | `mass: float` |
