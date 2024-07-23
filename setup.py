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
        'numpy>=2.0',# Any version of numpy above 2
        'matplotlib>=3.4.3', # Ensure matplotlib version 3.4.3 or newer'],
	scripts = ['scripts/gt-ucli']
	)
