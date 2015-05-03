#!/usr/bin/env python

from sys import version_info

from setuptools import setup, find_packages

python_version = "%s.%s" % (version_info[0], version_info[1])

if python_version == "2.7":
    requires = ["orderedmultidict>=0.7", "future"]
else:
    requires = ["orderedmultidict>=0.7"]

setup(
    name="htpasswd",
    version="2.3",
    packages=["htpasswd"],
    install_requires=requires,
    author="Ilya Otyutskiy",
    author_email="ilya.otyutskiy@icloud.com",
    maintainer="Ilya Otyutskiy",
    url="https://github.com/thesharp/htpasswd",
    description="Library to work with htpasswd user (basic authorization) and group files.",
    license="MIT"
)
