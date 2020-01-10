#!/usr/bin/env python

#
# This file is in the public domain.
#

import re, os, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

v = open(os.path.join(os.path.dirname(__file__), 'jmapd', '__init__.py'))
VERSION = re.compile(r".*__version__ *= *['\"](.*?)['\"]", re.S) \
                                                       .match(v.read()).group(1)

DEPENDENCIES = ('neurons',)

setuptools.setup(
    name="jmapd",
    version=VERSION,
    author="Burak Arslan",
    author_email="inbox@burakarslan.com",
    description="A JMAP server implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arskom/jmapd",
    packages=setuptools.find_packages(),
    install_requires=DEPENDENCIES,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    entry_points={
        'console_scripts': [
            'jmapd=jmapd.main:jmapd_main',
        ]
    },
)
