from setuptools import setup, find_packages

setup(
    name='WinAdmin',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pywin32',
        'psutil',
        'schedule'
    ],
    entry_points={
        'console_scripts': [
            'winadmin=src.main:main',
        ],
    },
)
