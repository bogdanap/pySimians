from setuptools import setup
from os import path

def parse_requirements(file_path=None):
    if file_path is None:
        file_path = path.join(path.dirname(__file__), "monkeys/REQUIREMENTS")
    with open(file_path) as fd:
        return [l.strip() for l in fd.xreadlines()]

setup(
    name="pySimians",
    version="0.0.1",
    packages=['monkeys'],
    # package_dir={'': '.'},
    install_requires=parse_requirements(),
    package_data={
        '': ['*.txt'],
    },
    # metadata for upload to PyPI
    author="pySimians Team",
    description="pySimians, a Python powered horde of evil monkeys!",
    url="https://github.com/bogdanap/pySimians/",
)
