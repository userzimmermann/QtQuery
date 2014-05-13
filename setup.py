try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = open('VERSION').read().strip()

REQUIRES = open('requirements.txt').read()


setup(
  name='modeled',
  version=VERSION,
  description="A jQuery inspired Pythonic Qt experience.",

  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/QtQuery',

  license='LGPLv3',

  install_requires=REQUIRES,

  packages=[
    'QtQuery',
    ],
  )
