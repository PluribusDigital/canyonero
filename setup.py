from setuptools import setup

setup(name='canyonero',
      version='0.1',
      description='Creates a canon from a list of values',
      author='STSI',
      packages=['canyonero'],
      install_requires=[
          'nltk',
          'flask',
          'flask-restful',
          'distance',
      ],
      test_suite='tests',
      zip_safe=False)
