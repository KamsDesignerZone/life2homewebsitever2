from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in life2homewebsitever2/__init__.py
from life2homewebsitever2 import __version__ as version

setup(
	name="life2homewebsitever2",
	version=version,
	description="Life2Home Website Version 2",
	author="Kams Designer Zone",
	author_email="info@life2home.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
