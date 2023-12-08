from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in dscapl/__init__.py
from dscapl import __version__ as version

setup(
	name="dscapl",
	version=version,
	description="This app is created for the purpose of customisation in D.S. Controls and Automation Pvt Ltd",
	author="Ajay Patole",
	author_email="ajaypatole@dhuparbrothers.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
