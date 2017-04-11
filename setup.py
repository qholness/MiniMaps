from setuptools import setup

setup(
    name='MiniMaps',
    packages=['MiniMaps'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pandas']
)