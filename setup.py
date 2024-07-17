import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brealid",
    version="v0.0.5",
    author="brealid",
    author_email="brealid@mail.ustc.edu.cn",
    description="brealid's python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brealid/brealid-python-lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "pycryptodome>=3.15.0",
        "requests>=2.24.0",
        "tqdm>=4.0.0",
    ]
)