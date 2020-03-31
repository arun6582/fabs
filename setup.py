from setuptools import setup, find_packages
setup(
    name='fabs',
    packages=find_packages(),
    version='1.0.3',
    author='Arun',
    author_email='arun6582@gmail.com',
    install_requires=[
        'fabric>=2.5.0'
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Web Environment',
    ],
)
