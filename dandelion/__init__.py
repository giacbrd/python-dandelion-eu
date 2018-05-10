""" main dandelion package
"""

from dandelion.base import DandelionException, DandelionConfig
from dandelion.datagem import Datagem
from dandelion.datatxt import DataTXT
from dandelion.sentiment import Sentiment

__version__ = '0.2.2'
default_config = DandelionConfig()
