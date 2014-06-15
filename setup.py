#!/usr/bin/python
import os
from setuptools import setup

#README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-db-mixins',
    version='1.0.0-alpha',
    packages=['django_mixins', 'django_mixins.tests'],
    include_package_data=True,
    license='Apache Software License',
    description='A small Django app that provides mixins and extended mixin capabilities to the model layer.',
    #long_description=README,
    url='http://silkentrance.github.io/django-db-mixins',
    author='Carsten Klein',
    author_email='trancesilken@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

