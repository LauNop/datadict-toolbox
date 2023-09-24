from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'A package to build a data dictionary from .xmla MS SQL SERVER file and select SQL query.'
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()
    f.close()

# Setting up
setup(
    name="datadict-toolbox",
    version=VERSION,
    packages=["datadict_toolbox"],
    author="Laurent NOPOLY",
    author_email="laurentnopoly@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/LauNop/datadict-toolbox",
    install_requires=["openai", "pandas", "openpyxl", "python-dotenv"],
    keywords=['python', 'data', 'dictionary', 'governance', 'SQL'],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha ",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)