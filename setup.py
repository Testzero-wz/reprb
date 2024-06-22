# setup.py
from setuptools import setup, Extension

module = Extension(
    "_reprb",
    sources=["src/_reprb.c"],
    extra_compile_args=["-Wno-unused-const-variable"],
)

setup(
    name="reprb",
    version="1.0",
    author="T3stzer0",
    description="represent bytes as printable chars, vice versa",
    ext_modules=[module],
)
