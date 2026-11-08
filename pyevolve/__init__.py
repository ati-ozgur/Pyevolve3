"""
    ## `pyevolve` -- the main pyevolve namespace

    This is the main module of the pyevolve, every other module
    is above this namespace, for example, to import `Mutators`:

    ```pycon
    >>> from pyevolve import Mutators
    ```
"""
__all__ = ["Consts", "DBAdapters", "FunctionSlot",
           "GAllele", "GenomeBase", "GPopulation",
           "GSimpleGA", "Scaling"
           "Statistics", "Util"]

__version__ = '0.7'
__author__ = 'Christian S. Perone'

from . import Consts


def logEnable(filename=Consts.CDefLogFile, level=Consts.CDefLogLevel):
    """
        Enable the log system for pyevolve

        ### Parameters

        - `filename`: the log filename
        - `level`: the debugging level

        Example:
        ```pycon
        >>> pyevolve.logEnable()
        ```
    """
    import logging
    logging.basicConfig(level=level,
                        format='%(asctime)s [%(module)s:%(funcName)s:%(lineno)d] %(levelname)s %(message)s',
                        filename=filename,
                        filemode='w')
    logging.info("Pyevolve v.%s, the log was enabled by user.", __version__)
