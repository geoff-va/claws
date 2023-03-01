from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="claws",
    version="0.0.1",
    description="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "claws=claws.main:cli",
        ]
    },
)
