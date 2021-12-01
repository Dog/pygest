from setuptools import setup
from pathlib import Path

setup(
    name="pygest",
    description="A python framework for digesting APIs",
    packages=["pygest"],
    author="Dog",
    url="https://github.com/dog/pygest",
    version="0.0.1",
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    zip_safe=False,
    install_requires=[
        "httpx"
    ]
)