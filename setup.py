import os

from setuptools import setup

packages = [
    'ssaw',
]

requires = [
    'requests',
    'sgqlc',
]

test_requirements = [
    'flake8',
    'flake8-import-order',
    'pytest',
    'pytest-cov',
    'vcrpy',
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'ssaw', '__about__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: PyPy',
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    classifiers=classifiers,
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
