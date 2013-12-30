#!/usr/bin/env python

from setuptools import setup

setup(
    name='talli.fi',
    version='1.0',
    description='Multitenant django-stables provider',
    author='Juho Rutila',
    author_email='juho.rutila@iki.fi',
    url='',
    install_requires=[ 
        'Django==1.5',
        'django-tenant-schemas',
        'django-reusableapps==0.1.1',
        'django-grappelli',
        'django-stables==dev',
        'django-compressor',
        'South==0.8.2',
        'django-mptt==0.6.0',
        'python-memcached',
        'python-dateutil==1.5',
        'django-fluent-comments==0.9.2',
        'django-import-export==0.1.5',
    ],
    zip_ok=False,
    zip_safe=False,
    dependency_links = [
        "https://api.github.com/repos/jrutila/django-stables/tarball/multitenant?access_token=30e539ba9491700b201ccbeda82b8cb722c4064c#egg=django-stables-dev",
        "https://api.github.com/repos/jrutila/django-tenant-schemas/tarball/master?access_token=30e539ba9491700b201ccbeda82b8cb722c4064c#egg=django-tenant-schemas-1.4.2-1",
    ]
)
