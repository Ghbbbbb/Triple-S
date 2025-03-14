from setuptools import setup, find_packages

setup(
    name='robopal',
    packages=[package for package in find_packages() if package.startswith("robopal")],
    version='0.4.0',
    author="Haoran Zhou, Yichao Huang, Yuhan Zhao, Yang Lu",
    author_email="jou072@126.com",
    description="robopal: A Simulation Framework based Mujoco",
    url="https://github.com/NoneJou072/robopal",
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        'numpy>=1.23.5',
        'mujoco==3.1.4',
        'gymnasium',
        'opencv-python',
        'opencv-contrib-python'
    ],
    extras_require={
        'planning': ['ruckig~=0.9.2'],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
)
