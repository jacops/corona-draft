import os.path
import sys
from glob import glob
from setuptools import setup, find_packages

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def get_requirements(req_file='requirements.txt'):
    try:
        return open(os.path.join(os.path.dirname(__file__), req_file)).readlines()
    except OSError:
        return []

setup(name='super_draft',
      version='0.1',
      description='Watches for Google Spreadsheet changes and tweet it',
      url='https://github.com/jacops/corona-draft/',
      author='Jakub Igla',
      author_email='jakub.igla@gmail.com',
      license='MIT',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=get_requirements(),
      setup_requires=[
          'setuptools >= 21.0.0',
          'wheel',
      ],
      include_package_data=True
      )
