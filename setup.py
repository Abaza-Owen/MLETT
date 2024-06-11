import os
from setuptools import setup, find_packages




setup(
	name = 'gausstrajlib',
	version='0.0.1',
	description='Library intended to help read gaussian BOMD trajectory output files',
	author='Owen M. Abaza',
	author_email='omabaza@syr.edu',
	license='MIT License',
	packages= find_packages(),
	scripts = ['scripts/gt-ucli.py']
	
	)
