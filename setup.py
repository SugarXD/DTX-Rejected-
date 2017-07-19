from distutils.core import setup

setup(
    name='Rejected',
    version='0.1.1',
    author='Team Rejected',
    packages=['rejected'],
    long_description=open('README.txt').read(),
    install_requires=[
        "Flask",
        "requests",
        "setuptools",
        "apscheduler",
    ],
)
