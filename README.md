# Triple-S
This is code repository for the paper **"Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Abstract Tasks in Robotics"**.

In recent years, extensive research has focused on enabling Large Language Models (LLMs) to write strategy code that drives robots. However, for long-horizon abstract tasks, this approach often results in API parameter and sequencing errors, leading to failures in the robot’s final movements. To address this issue, we propose a multi-LLM collaborative framework, named Triple-S, which leverages In-Context Learning to assign specific roles to different LLMs. Through a closed loop process of Simplify-Solution-Summary, the framework significantly improves the success rate of executing long-horizon abstract tasks. We validated Triple-S on the Long-sequence Desktop Abstract Placement[(LDAP)](dataset/README.md) dataset, where it successfully completed 89% of tasks in both observable and partially observable scenarios, outperforming state-of-the-art methods by 16%. Additionally, Triple-S demonstrated remarkable robustness. 

![The framework of Triple-S](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/Triple-S.png)


## 🛠 Install
Install requirements for repository 
```
    # Install Robopal simulation environment
    cd robopal
    pip install -r requirements.txt
    # Install the main program dependencies
    cd ..
    pip install -r requirements.txt
```


## 🏋️ Running


- gpt
```
export OPENAI_API_KEY=[YOUR_KEY]
python server.py --doc --write "GPT3.5_LDAP1_ours"
python client_retrieval_gpt.py --doc --prompt "ours" --task "LDAP1"
```

- llama3
```
python server.py --doc --env2 --write "LLAMA3_LDAP2_ours"
python client_retrieval_llama3.py --doc --prompt "ours" --task "LDAP2"
```

The prediction file will be dumped in the `output` folder.

## 🧪 Evaluation

```
cd output
python compare.py --file "GPT3.5_LDAP1_ours.txt" --env "env1"
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

Our project is open-sourced under the MIT license. Feel free to explore, modify, and share your innovations with the world.