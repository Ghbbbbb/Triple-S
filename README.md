# Triple-S
Welcome to Triple-S! 🚀This is code repository for the paper **"Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Abstract Tasks in Robotics"**.

We propose the Triple-S(Simplify-Solution-Summary) framework, which leverages the In-Context Learning capabilities of multiple LLMs to generate more robust policy code. This is a lightweight, training-free approach. The effectiveness and robustness of the Triple-S framework were validated through tests on the Long-horizon Desktop Implicative Placement[(LDIP)](dataset/README.md) dataset, which features long horizon tasks with implicative instructions in both observable and partially observable scenarios.

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