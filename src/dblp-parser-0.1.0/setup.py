# -*- encoding: utf-8 -*-
from distutils.core import setup

setup(
    name='dblp-parser',
    version='0.1.0',
    author='Yguaratã Cerqueira Cavalcanti',
    author_email='yguarata@gmail.com',
    packages=['dblpparser', 'dblpparser.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/dblp-parser/',
    license='LICENSE.txt',
    description='A Python lib to parse the DBLP Computer Science Bibliography. It provides a class model which is used to extract publication entries from the XML file provided by the DBLP.',
    long_description=open('README.txt').read(),
    install_requires=[],
)
