import os
from setuptools import setup, find_packages

def load_requirements(rel_path):
    """
    Load the dependencies from the specified file.
    """
    req_path = os.path.join(os.path.dirname(__file__), rel_path)
    with open(req_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

install_requires = load_requirements("requirements.txt")

extras_require = {}
pawn_dir = os.path.join(os.path.dirname(__file__), "pawn")
for item in os.listdir(pawn_dir):
    submodule_path = os.path.join(pawn_dir, item)
    req_file = os.path.join(submodule_path, "requirements.txt")
    if os.path.isdir(submodule_path) and os.path.exists(req_file):
        extras_require[item] = load_requirements(os.path.join("pawn", item, "requirements.txt"))

setup(
    name="pawn_ai",
    version="0.0.2",
    description="Precompiled Agents Workflow Network (P.A.W.N.) for building AI-driven, multi-agent crypto systems.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Logarithm Labs",
    author_email="dev@logarithm.fi",
    url="https://github.com/Logarithm-Labs/pawn",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
