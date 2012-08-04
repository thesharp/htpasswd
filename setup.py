#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="htpasswd",
    version="1.0",
    packages=["htpasswd"],
    install_requires=["orderedmultidict>=0.7"],
    author="Ilya A. Otyutskiy",
    author_email="sharp@thesharp.ru",
    maintainer="Ilya A. Otyutskiy",
    url="https://github.com/thesharp/htpasswd",
    description="Library to work with htpasswd user (basic authorization) "
                "and group files.",
    license="MIT"
)
