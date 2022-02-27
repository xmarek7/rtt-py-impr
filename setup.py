from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rtt",
    version="0.0.1",
    url="TODO",
    author="pvavecak",
    author_email="vavercak.pato@gmail.com",
    description="Randomness testing toolkit in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["rtt"],
    package_dir={'': "src"},
    classifiers=[
        "Natural Language :: English"
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ]
    },
)
