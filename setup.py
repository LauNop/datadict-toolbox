from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A package to build a data dictionary from xml MS SQL SERVER file'
with open("README.md","r") as f:
    LONG_DESCRIPTION = f.read()
    f.close()

#Setting up
setup(
    name="datadict_toolbox",
    version = VERSION,
    author = "LauNop (Laurent NOPOLY)",
    author_email = "laurentnopoly@gmail.com",
    description = DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    packages = find_packages(),
    install_requires = [],
    keywords = ['python','data','dictionary','governance'],
    license="",
    classifiers = [
        "Development Status :: Developping ERP solution ",
        "Intended Audience :: Deveoppers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)