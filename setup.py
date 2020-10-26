import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iotpy", # Replace with your own username
    version="0.0.1",
    author="Alessandro Manfredini",
    author_email="a.manfredini.work@gmail.com",
    description="Simple webserver to expose IOT devices tough HTTP and prometheus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panManfredini/IOTpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)