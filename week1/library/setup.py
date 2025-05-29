from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "anagramfinder",
        ["anagramfinder.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=['-std=c++11'],
    ),
]

setup(
    name="anagramfinder",
    version="0.1",
    ext_modules=ext_modules,
    include_package_data=True,
    package_data={
        "": ["words.txt"],
    },
)