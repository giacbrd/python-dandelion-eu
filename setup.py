try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'dandelion-eu',
    packages = ['dandelion'],
    version = '0.1.2',
    description = 'Connect to the dandelion.eu API in a very pythonic way!',
    author = 'Stefano Parmesan',
    author_email = 'parmesan@spaziodati.eu',
    url = 'https://github.com/armisael/python-dandelion',
    download_url = 'https://github.com/armisael/python-dandelion/tarball/0.1.2',
    keywords = ['api', 'dandelion'],
    install_requires=[
        'requests',
    ],
    classifiers = [],
)
