from setuptools import find_packages, setup


def readRequirements():
    a = []
    with open("requirements.txt") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                a.append(line.strip())
    return a


setup(
    name="easyfeh",
    version="0.1.1",
    description="An easy to use feh wrapper with cool features",
    author="Shibam Roy",
    author_email="shibamroy9826@gmail.com",
    url="https://github.com/ShibamRoy9826/easyfeh",
    packages=find_packages(),  
    install_requires=readRequirements(),
    entry_points={
        "console_scripts": [
            "easyfeh = easyfeh.easyfeh:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
