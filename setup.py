from setuptools import setup, find_packages

setup( name ="cmsplugin_availablejob",
        version  ="0.1",
        packages = find_packages(),
        install_requires = ["django-uni-form","south"],
)

