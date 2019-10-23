from setuptools import setup, find_packages
from os import path

from compositor import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='compositor',
    version=__version__,
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rafaelaraujobsb/pi3-compositor.git',
    author='Rafael Araujo',
    author_email='',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.6.*',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==1.1.1',
        'loguru==0.3.2',
        'flasgger==0.9.3',
        'gunicorn==19.9.0',
        'dnspython==1.16.0',
        'flask-cors==3.0.8',
        'jsonschema==2.6.0',
        'flask_restful==0.3.7',
    ],
)
