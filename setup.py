from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="DiceGameEngine_Dev_JSH",
    verison="0.0.1",
    description="Dice game engine to build various types of dice games",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hollanjs/DiceEngine",
    author="Josh Hollandsworth (hollanjs)",
    author_email="jshollandsworth@gmail.com",
    license="Unlicensed",
    classifiers=[
        "License :: Unlicensed",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independant"
    ],
    python_requires=">=3.12"
)