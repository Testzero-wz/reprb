# setup.py
from setuptools import setup, Extension, find_packages
import os


def read(fname):
    return open(
        os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8"
    ).read()


NAME = "reprb"

DESCRIPTION = "Represent bytes with printable characters"

LONG_DESCRIPTION = read("README.MD")

KEYWORDS = "repr bytes eval dump load"

AUTHOR = "T3stzer0"

AUTHOR_EMAIL = "testzero.wz@gmail.com"

URL = "https://github.com/testzero-wz/reprb"

VERSION = "1.0.1"

LICENSE = "MIT"

module = Extension(
    "_reprb",
    sources=["src/_reprb.c"],
    extra_compile_args=["-Wno-unused-const-variable"],
)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    ext_modules=[module],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
)
