# Triple-S
This is code repository for the paper **"Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Abstract Tasks in Robotics"**.

In recent years, extensive research has focused on enabling Large Language Models (LLMs) to write strategy code that drives robots. However, for long-horizon abstract tasks, this approach often results in API parameter and sequencing errors, leading to failures in the robot’s final movements. To address this issue, we propose a multi-LLM collaborative framework, named Triple-S, which leverages In-Context Learning to assign specific roles to different LLMs. Through a closed loop process of Simplify-Solution-Summary, the framework significantly improves the success rate of executing long-horizon abstract tasks. We validated Triple-S on the Long-sequence Desktop Abstract Placement[(LDAP)](dataset/README.md) dataset, where it successfully completed 89% of tasks in both observable and partially observable scenarios, outperforming state-of-the-art methods by 16%. Additionally, Triple-S demonstrated remarkable robustness. 

![The framework of IRAIS](https://github.com/Ghbbbbb/Triple-S/blob/main/assets/Triple-S.png)


## Install
Install requirements for repository 
```
    # Install Robopal simulation environment
    cd robopal
    pip install -r requirements.txt
    # Install the main program dependencies
    cd ..
    pip install -r requirements.txt
```


## Run

- gpt
```
export OPENAI_API_KEY=[YOUR_KEY]
python server.py [--write *** --doc --env2]
python client_retrieval_gpt.py [--debug --doc --prompt *** --task ***]
```

- llama3
```
python server.py [--write *** --doc --env2]
python client_retrieval_llama3.py [--debug --doc --prompt *** --task ***]
```

The prediction file will be dumped in the output/ folder if `--write ***` has been set.

## Evaluation

```
cd output
python compare.py --file "GPT3.5-LDAP1-ours.txt" --env "env1"
python compare.py --file "GPT3.5-LDAP2-ours.txt" --env "env2"
....
```

## Results
GPT3.5-turbo-0613
- Output: output/GPT3.5-LDAP1-ours.txt
- Accuracy: 93.30%
- Mean error: 0.028  
- Output: outputs/GPT3.5-LDAP2-ours.txt
- Accuracy: 94.85%
- Mean error: 0.042
