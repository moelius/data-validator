from os.path import join, dirname

from setuptools import setup, find_packages

PACKAGE = "data_validator"
NAME = "data-validator"
DESCRIPTION = "'Package for validate'"
AUTHOR = "Klimov Konstantin"
AUTHOR_EMAIL = "moelius1983@gmail.com"
URL = "https://github.com/moelius/data-validator"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        'numpy',
    ],
    zip_safe=False,
)
