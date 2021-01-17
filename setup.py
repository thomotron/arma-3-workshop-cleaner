import os
from setuptools import find_packages
from cx_Freeze import setup, Executable

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
	name='a3-workshop-cleaner',
	packages=find_packages('.'),
	version='1.0.0',
	license='Unlicense',
	author='Thomotron',
	executables=[Executable('main.py')]
)
