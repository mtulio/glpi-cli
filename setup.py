from setuptools import setup, find_packages
from codecs import open
from os import path


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

exec (open('glpi-cli/version.py').read())

setup(
    name='glpi-cli',
    packages=["glpi-cli"],
    version=__version__,
    description='GLPI Command Line Interface',
    #long_description=readme(),
    url='https://github.com/mtulio/glpi-cli',
    download_url='https://github.com/mtulio/glpi-cli/archive/0.1.1.tar.gz',
    author='Marco Tulio R Braga',
    author_email='braga@mtulio.eng.br',
    license='Apache-2.0',
    classifiers=[],
    keywords=['GLPI', 'CLI'],
    install_requires=[
        'glpi',
        'dotenv',
        'argparse',
    ]
)
