try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='ontrack',
      version='1.0',
      py_modules=['cosine_matcher', 'text_cleaners', 'string_searcher'],
      install_requires=['numpy', 'pandas', 'nltk', 'scipy==0.16.1', 'scikit-learn'])

import nltk
nltk.download('stopwords')
nltk.download('punkt')

