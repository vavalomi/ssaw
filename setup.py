from setuptools import setup, find_packages
setup(
	name="ssaw",
	version="0.0.2",
	packages=find_packages(exclude=['tests*']),

	install_requires=['requests'],

	author="Zurab Sajaia",
	author_email="vavalomi@hotmail.com",
	description="Wrapper for Survey Solutions API",
	license="",
	keywords="Survey Solutions",
	url="https://github.com/vavalomi/ssaw",
	download_url = 'https://github.com/vavalomi/ssaw/archive/0.0.2.tar.gz',
)
