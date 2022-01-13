from setuptools import setup

install_requires = [
    "tensorflow >= 2.6.0",
]

extras_require = {
    "dev": ["black", "flake8 >= 4.0", "isort >= 5.9", "pre-commit >= 2.16"],
}

setup(
    name="magicpacket",
    version="0.0.1",
    url="https://github.com/jjgp/magic-packet",
    author="Jason Prasad",
    author_email="jasongprasad@gmail.com",
    description="Wake word detection",
    install_requires=install_requires,
    extras_require=extras_require,
)
