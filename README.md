# Triple-S
Welcome to Triple-S! 🚀This is code repository for the paper **"Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Implicative Tasks in Robotics"**.

We propose the Triple-S(Simplify-Solution-Summary) framework, which leverages the In-Context Learning capabilities of multiple LLMs to generate more robust policy code. This is a lightweight, training-free approach. The effectiveness and robustness of the Triple-S framework were validated through tests on the Long-horizon Desktop Implicative Placement[(LDIP)](dataset/README.md) dataset, which features long horizon tasks with implicative instructions in both observable and partially observable scenarios.

![The framework of Triple-S](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/Triple-S.png)


## 🛠 Installation
```bash
# Install Robopal simulation environment
cd robopal
pip install -r requirements.txt

# Install main program dependencies
cd ..
pip install -r requirements.txt
```

## 🏋️ Running
### 1. Set Environment Variables
```bash
export OPENAI_API_KEY = [YOUR_KEY]
export HF_ENDPOINT = https://hf-mirror.com  # Set this mirror if you cannot access HuggingFace directly
```

### 2. Execution Modes
### 2.1 Debug Mode (Tests LLM policy generation without robot control)
```bash
# Tests GPT using LDIP1_v1 task prompts (manual instruction input)
python client_retrieval_gpt.py --debug --prompt "ours" --task "LDIP1_v1" 
```
### 2.2 Simulation Mode (Tests policy execution with robot simulation)
```bash
# Start simulation environment (saves results to test.txt)
python server.py --write "test" --env 1  

# Generate policy code with GPT and execute in simulation
python client_retrieval_gpt.py --prompt "ours" --task "LDIP1_v1"  
```
### 2.3 Dataset Mode (Run dataset instructions and save results)
```bash
# Start simulation environment (will reset environment state after each run)
python server.py --doc --write "GPT3.5_ours" --env 1

# Generate policy code with GPT (document instruction input)
python client_retrieval_gpt.py --doc --prompt "ours" --task "LDIP1_v1"
```
> **Note**: To test with LLAMA3, replace `client_retrieval_gpt.py` with `client_retrieval_llama3.py` in above commands.And before using LLAMA3, you must [request access](https://llama.meta.com/llama-downloads/) from Meta and accept their license agreement.<br>
Prompts for baseline methods are re-implementations based on original paper methodologies, not direct copies.

The prediction file will be dumped in the `output` folder.

## 🧪 Evaluation

```bash
cd output/LDIP1_v1
python compare.py --file "GPT3.5_ours.txt"
....
```

## 📈 Results
![Results of Triple-S](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/result.jpg)

## 🙏 Acknowledgment

Special thanks to:

1. [Robopal](https://github.com/NoneJou072/robopal) for their simulation environment.
2. [Llama3](https://github.com/meta-llama/llama3) by Meta AI Research for their powerful baseline model.

Each of these contributions has been pivotal in shaping our work. We're incredibly grateful for the community's shared knowledge and innovation.

## 📄 License 

Our project is open-sourced under the MIT license. Feel free to explore, modify, and share your innovations with the world.# Triple-S
