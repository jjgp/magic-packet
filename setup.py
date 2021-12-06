from setuptools import setup

install_requires = []

extras_require = {
    "dev": ["black >= 21", "flake8 >= 4.0", "isort >= 5.9", "pre-commit >= 2.16"],
    "mlops": [
        "cryptography >= 36.0",
        "jupyter >= 1.0",
        # pandas is used by jupyter variables view in vscode interactive python window
        "pandas >= 1.3",
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
)
