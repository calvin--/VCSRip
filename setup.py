try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='vcsrip',
      version='0.1',
      description='VCSRip',
      url='https://github.com/calvin--/VCSRip',
      author='Simon Toft',
      author_email='simon@toft.io',
      license='MIT',
      packages=['dvcsrip'],
      zip_safe=False)
