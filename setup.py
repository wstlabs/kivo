import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "kivo",
    version = "0.0.5",
    author = "wstlabs",
    author_email = "wst@pobox.com",
    description = ("Modular ELT for elephants"),
    license = "Apache 2.0",
    keywords = "ELT postgresql data-warehouse"
    url = "http://packages.python.org/kivo",
    packages= ['kivo', 'tests'],
    long_description=read('README.md'),
    classifiers= [
        "Topic :: Utilities",
        "Development Status :: 2 - Pre-Alpha",
    ],
)

