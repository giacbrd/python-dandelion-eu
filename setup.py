import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from dandelion import __version__


def readfile(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path).read()

setup(
    name='dandelion-eu',
    packages=[
        'dandelion',
        'dandelion.cache',
    ],
    version=__version__,
    description='Connect to the dandelion.eu API in a very pythonic way!',
    long_description=readfile('README.rst'),
    author='SpazioDati s.r.l.',
    author_email='berardi@spaziodati.eu',
    url='https://github.com/giacbrd/python-dandelion-eu',
    download_url='https://github.com/giacbrd/'
                 'python-dandelion-eu/tarball/' + __version__,
    keywords=['api', 'dandelion'],
    install_requires=[
        'requests',
        'six',
    ],
    classifiers=(
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: English',
        'Natural Language :: Italian',
        'Natural Language :: Spanish',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Russian',
        'Natural Language :: Portuguese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ),
)
