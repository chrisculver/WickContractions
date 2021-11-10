from setuptools import setup

setup(
  name='WickContractions',
  version='0.1.0',
  author='Chris Culver',
  packages=['WickContractions'],
  license='LICENSE.txt',
  description='Package for wick contractions',
  long_description=open('README.md').read(),
  install_requires=open('requirements.py').read()
)
