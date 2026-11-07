#from distutils.core import setup #changed to distutils.core for pypy comptibility
from setuptools import find_namespace_packages, setup
import sys

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
   name = "Pyevolve3",
   version = '0.7',
   packages = find_namespace_packages(include=["pyevolve", "pyevolve.*"]),
   scripts = ['pyevolve_graph.py'],
   install_requires=required,
   package_data = {
      'pyevolve': ['*.txt']
   },
   test_suite = 'tests',
   author = 'Atilla Özgür, Burak Dalkılıç, Christian S. Perone,   Gürkan Er',
   author_email = "ati.ozgur@gmail.com",
   description = "A complete, free and open-source genetic algorithms framework written in Python 3. Traveling salesperson problem related optimizations.",
   license = "PSF",
   keywords = "genetic algorithms, travelling salesperson problem, framework library python ai evolutionary framework",
   url = "http://pyevolve.sourceforge.net/",
   python_requires=">=3.9",
)
