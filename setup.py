from setuptools import setup, find_packages
setup(
	name="ssaw",
	version="0.0.1",
	packages=find_packages(exclude=['tests*']),

	install_requires=['pytest', 'requests'],

	author="Zurab Sajaia",
	author_email="zsajaia@hotmail.com",
	description="Wrapper for Survey Solutions API",
	license="",
	keywords="Survey Solutions",
	url="http://worldbank.org/capi",
)
