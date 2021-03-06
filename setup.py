from setuptools import find_packages, setup

install_requires = [
    "click >= 8.0",
    "numpy >= 1.19",
    "pydub >= 0.25",
    "tensorflow >= 2.7",
    "tensorflow-datasets >= 4.4",
    "tqdm >= 4.62",
]

extras_require = {
    "dev": ["black", "flake8 >= 4.0", "isort >= 5.9", "pre-commit >= 2.16"],
    "mlops": ["cryptography >= 36.0", "jupyter >= 1.0"],
    "notebooks": [
        "jupyter >= 1.0",
        "matplotlib >= 3.5",
        "numpy >= 1.19",
        "seaborn >= 0.11",
    ],
}

setup(
    name="magic-packet",
    version="0.0.1",
    url="https://github.com/jjgp/magic-packet",
    author="Jason Prasad",
    author_email="jasongprasad@gmail.com",
    description="Wake word detection",
    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["magicpkt = magic_packet.cli.magicpkt:magicpkt"],
    },
)
