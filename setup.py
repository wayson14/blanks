from setuptools import setup, find_packages

setup(
    name = 'blanks',
    version = '0.1.0',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'blanks=blanks_game.__main__:main'
        ]},
    )