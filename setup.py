from setuptools import setup, find_packages

setup(
    name='filestructuregenerator',
    version='0.1',
    author='Thomas Rasser',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['Click'],
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'fsg=FileStructureGenerator.cli.cli_commands:cli', 
        ]
    }
)
