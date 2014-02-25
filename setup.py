try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from dandelion import __version__

with open('README.rst') as f:
    readme = f.read()

setup(
    name='dandelion-eu',
    packages=[
        'dandelion',
        'dandelion.cache',
    ],
    version=__version__,
    description='Connect to the dandelion.eu API in a very pythonic way!',
    long_description=readme,
    author='SpazioDati s.r.l.',
    author_email='parmesan@spaziodati.eu',
    url='https://github.com/SpazioDati/python-dandelion-eu',
    download_url='https://github.com/SpazioDati/'
                 'python-dandelion-eu/tarball/' + __version__,
    keywords=['api', 'dandelion'],
    install_requires=[
        'requests',
        'six',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ),
)
