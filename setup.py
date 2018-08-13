from setuptools import setup

from utils.install_webdrivers import InstallWebDrivers

setup(
    name="Testing Framework",
    version="1.0.0",
    author="",
    author_email="",
    install_requires = ["pytest", "selenium", "requests"],
    cmdclass = {
        'install_webdrivers': InstallWebDrivers
    }
)