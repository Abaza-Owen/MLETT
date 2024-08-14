import os
from setuptools import setup, find_packages


setup(
	name = 'MLETT',
	version = '1.0.0',
	description='Library intended to help read and manipulate chemistry machine learning dataset files and to produce dataset files from gaussian .log files. ',
	author = 'Owen M. Abaza',
	author_email = 'omabaza@syr.edu',
	license='MIT License',
	packages = find_packages(),
    install_requires = [
        'numpy>=2.0',
        'matplotlib>=3.4.3',],
	scripts = ['scripts/gt-ucli']
	)
