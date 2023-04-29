from setuptools import setup, find_packages

setup(
    name='CarService',
    version='0.0.1',
    author='Igor Chęciński, Patryk Załuska',
    author_email='s24605@pjwstk.edu.pl',
    description='Simple project which helps to manage car service',
    packages=find_packages(),
    install_requires=["requirements.txt"]
)
