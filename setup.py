#!/usr/bin/env python

from setuptools import setup

setup(
    name='talli.fi',
    version='1.0',
    description='Multitenant django-stables provider',
    author='Juho Rutila',
    author_email='juho.rutila@iki.fi',
    url='',
    install_requires=[ 'Django==1.5', 'django-tenant-schemas', 'South==0.8.1', 'django-reusableapps==0.1.1', 'djangorestframework', 'django-grappelli', 'django-stables==dev', 'django-compressor' ],
    zip_ok=False,
    dependency_links = [
        "https://api.github.com/repos/jrutila/django-stables/tarball/multitenant?access_token=30e539ba9491700b201ccbeda82b8cb722c4064c#egg=django-stables-dev"
    ]
)
