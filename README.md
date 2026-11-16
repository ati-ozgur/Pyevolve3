# PyEvolve 3

This project started as Python 3 version of pyevolve.
But right now, more focus is given to more genetic algorithm operators, especially those special operators which works for TSP (Traveling Salesperson Problem).


## Installation

	python -m pip install git+https://github.com/ati-ozgur/Pyevolve3.git

Optional extras:

- `graph`: matplotlib, for the `pyevolve_graph` plotting tool and interactive plots
- `examples`: everything the scripts in `examples/` need (tsplib95, Pillow, scipy, scikit-fuzzy, matplotlib)
- `test`: pytest, coverage, ruff, flake8

Extras are given in brackets before the git URL (keep the quotes, shells like zsh treat `[...]` as a glob):

	# one extra, e.g. to run the examples
	python -m pip install "Pyevolve3[examples] @ git+https://github.com/ati-ozgur/Pyevolve3.git"

	# several extras
	python -m pip install "Pyevolve3[graph,test] @ git+https://github.com/ati-ozgur/Pyevolve3.git"

	# a specific branch, tag or commit
	python -m pip install "Pyevolve3[examples] @ git+https://github.com/ati-ozgur/Pyevolve3.git@master"

In a `requirements.txt` file the same form is used without quotes:

	Pyevolve3[examples] @ git+https://github.com/ati-ozgur/Pyevolve3.git

For development, from a clone of the repository:

	python -m pip install -e ".[test,examples]"

## Python support

The minimum supported Python version is 3.9. The CI matrix targets Python 3.9 through 3.13.

## Python 3 Version of PyEvolve

- See this [stackoverflow question for more info](https://stackoverflow.com/questions/38647052/use-pyevolve-in-python-3/41539338)

- [Original Python 2 Version](https://github.com/perone/Pyevolve)

- Python 3 version is cloned from [BubaVV/Pyevolve](https://github.com/BubaVV/Pyevolve)


- The old documentation (html rendered) is still hosted at sourceforge.net at http://pyevolve.sourceforge.net/0_6rc1/
