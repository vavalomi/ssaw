import os

from setuptools import setup

packages = [
    'ssaw.headquarters',
]

requires = [
    'requests',
]

test_requirements = [
    'pytest',
    'vcr',
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'ssaw', '__about__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=packages,
    install_requires=requires,
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    license="",
    keywords="Survey Solutions",
    url=about['__url__'],
    tests_require=test_requirements,
)
