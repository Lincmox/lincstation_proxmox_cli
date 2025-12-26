from setuptools import setup, find_packages

setup(
    name="lincmox",
    version="1.0.0",
    description="LincMox CLI to control LincStation LEDS",
    author="Florent GAUDIN",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'lincmox=lincmox_cli.cli.main:main'
        ],
    }
)