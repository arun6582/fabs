from setuptools import setup, find_namespace_packages
setup(
  name='fabs',
  packages=find_namespace_packages(include=["src.*"]),
  version='1.0',
  author='Arun',
  author_email='arun6582@gmail.com',
  classifiers=[
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Environment :: Web Environment',
  ],
)
