"""
    ## `Consts` -- constants module

    Pyevolve have defaults in all genetic operators, settings and etc, this is an issue to helps the user in the API use
    and minimize the source code needed to make simple things. In the module `Consts`, you will find those defaults
    settings. You are encouraged to see the constants, but not to change directly on the module, there are methods for this.

    ### General constants

    #### `CDefPythonRequire`

    The mininum version required to run Pyevolve.

    #### `CDefLogFile`

    The default log filename.

    #### `CDefLogLevel`

    Default log level.

    #### `sortType`

    Sort type, raw or scaled.

    Example:
    ```pycon
    >>> sort_type = Consts.sortType["raw"]
    >>> sort_type = Consts.sortType["scaled"]
    ```

    #### `minimaxType`

    The Min/Max type, maximize or minimize the evaluation function.

    Example:
    ```pycon
    >>> minmax = Consts.minimaxType["minimize"]
    >>> minmax = Consts.minimaxType["maximize"]
    ```

    #### `CDefESCKey`

    The ESC key ASCII code. Used to start Interactive Mode.

    #### `CDefRangeMin`

    Minimum range. This constant is used as integer and real max/min.

    #### `CDefRangeMax`

    Maximum range. This constant is used as integer and real max/min.

    #### `CDefBroadcastAddress`

    The broadcast address for UDP, 255.255.255.255

    #### `CDefImportList`

    The import list and messages

    #### `nodeType`

    The genetic programming node types, can be "TERMINAL":0 or "NONTERMINAL":1

    #### `CDefGPGenomes`

    The classes which are used in Genetic Programming, used to detected the
    correct mode when starting the evolution

    ### Selection methods constants (`Selectors`)

    #### `CDefTournamentPoolSize`

    The default pool size for the Tournament Selector (`Selectors.GTournamentSelector`).

    ### Scaling scheme constants (`Scaling`)

    #### `CDefScaleLinearMultiplier`

    The multiplier of the Linear (`Scaling.LinearScaling`) scaling scheme.

    #### `CDefScaleSigmaTruncMultiplier`

    The default Sigma Truncation (`Scaling.SigmaTruncScaling`) scaling scheme.

    #### `CDefScalePowerLawFactor`

    The default Power Law (`Scaling.PowerLawScaling`) scaling scheme factor.

    #### `CDefScaleBoltzMinTemp`

    The default mininum temperature of the (`Scaling.BoltzmannScaling`) scaling scheme factor.

    #### `CDefScaleBoltzFactor`

    The default Boltzmann Factor of (`Scaling.BoltzmannScaling`) scaling scheme factor.
    This is the factor that the temperature will be subtracted.

    #### `CDefScaleBoltzStart`

    The default Boltzmann start temperature (`Scaling.BoltzmannScaling`).
    If you don't set the start temperature parameter, this will be the default initial
    temperature for the Boltzmann scaling scheme.

    ### Population constants (`GPopulation.GPopulation`)

    #### `CDefPopSortType`

    Default sort type parameter.

    #### `CDefPopMinimax`

    Default min/max parameter.

    #### `CDefPopScale`

    Default scaling scheme.

    ### 1D Binary String Defaults (`G1DBinaryString.G1DBinaryString`)

    #### `CDefG1DBinaryStringMutator`

    The default mutator for the 1D Binary String (`G1DBinaryString.G1DBinaryString`) chromosome.

    #### `CDefG1DBinaryStringCrossover`

    The default crossover method for the 1D Binary String (`G1DBinaryString.G1DBinaryString`) chromosome.

    #### `CDefG1DBinaryStringInit`

    The default initializator for the 1D Binary String (`G1DBinaryString.G1DBinaryString`) chromosome.

    #### `CDefG1DBinaryStringUniformProb`

    The default uniform probability used for some uniform genetic operators for the
    1D Binary String (`G1DBinaryString.G1DBinaryString`) chromosome.

    ### 2D Binary String Defaults (`G2DBinaryString.G2DBinaryString`)

    #### `CDefG2DBinaryStringMutator`

    The default mutator for the 2D Binary String (`G2DBinaryString.G2DBinaryString`) chromosome.

    #### `CDefG2DBinaryStringCrossover`

    The default crossover method for the 2D Binary String (`G2DBinaryString.G2DBinaryString`) chromosome.

    #### `CDefG2DBinaryStringInit`

    The default initializator for the 2D Binary String (`G2DBinaryString.G2DBinaryString`) chromosome.

    #### `CDefG2DBinaryStringUniformProb`

    The default uniform probability used for some uniform genetic operators for the
    2D Binary String (`G2DBinaryString.G2DBinaryString`) chromosome.

    ### 1D List chromosome constants (`G1DList.G1DList`)

    #### `CDefG1DListMutIntMU`

    Default *mu* value of the 1D List Gaussian Integer Mutator (`Mutators.G1DListMutatorIntegerGaussian`),
    the *mu* represents the mean of the distribution.

    #### `CDefG1DListMutIntSIGMA`

    Default *sigma* value of the 1D List Gaussian Integer Mutator (`Mutators.G1DListMutatorIntegerGaussian`),
    the *sigma* represents the standard deviation of the distribution.

    #### `CDefG1DListMutRealMU`

    Default *mu* value of the 1D List Gaussian Real Mutator (`Mutators.G1DListMutatorRealGaussian`),
    the *mu* represents the mean of the distribution.

    #### `CDefG1DListMutRealSIGMA`

    Default *sigma* value of the 1D List Gaussian Real Mutator (`Mutators.G1DListMutatorRealGaussian`),
    the *sigma* represents the mean of the distribution.

    ### Tree chromosome constants (`GTree.GTree`)

    #### `CDefGTreeInit`

    Default initializator of the tree chromosome.

    #### `CDefGGTreeMutator`

    Default mutator of the tree chromosome.

    #### `CDefGTreeCrossover`

    Default crossover of the tree chromosome.

    ### 2D List chromosome constants (`G2DList.G2DList`)

    #### `CDefG2DListMutRealMU`

    Default *mu* value of the 2D List Gaussian Real Mutator (`Mutators.G2DListMutatorRealGaussian`),
    the *mu* represents the mean of the distribution.

    #### `CDefG2DListMutRealSIGMA`

    Default *sigma* value of the 2D List Gaussian Real Mutator (`Mutators.G2DListMutatorRealGaussian`),
    the *sigma* represents the mean of the distribution.

    #### `CDefG2DListMutIntMU`

    Default *mu* value of the 2D List Gaussian Integer Mutator (`Mutators.G2DListMutatorIntegerGaussian`),
    the *mu* represents the mean of the distribution.

    #### `CDefG2DListMutIntSIGMA`

    Default *sigma* value of the 2D List Gaussian Integer Mutator (`Mutators.G2DListMutatorIntegerGaussian`),
    the *sigma* represents the mean of the distribution.

    #### `CDefG2DListMutator`

    Default mutator for the 2D List chromosome.

    #### `CDefG2DListCrossover`

    Default crossover method for the 2D List chromosome.

    #### `CDefG2DListInit`

    Default initializator for the 2D List chromosome.

    #### `CDefG2DListCrossUniformProb`

    Default uniform probability for the 2D List Uniform Crossover method (`G2DListCrossoverUniform`).

    ### GA Engine constants (`GSimpleGA.GSimpleGA`)

    #### `CDefGAGenerations`

    Default number of generations.

    #### `CDefGAMutationRate`

    Default mutation rate.

    #### `CDefGACrossoverRate`

    Default crossover rate.

    #### `CDefGAPopulationSize`

    Default population size.

    #### `CDefGASelector`

    Default selector method.

    ### DB Adapters constants (`DBAdapters`)

    Constants for the DB Adapters

    ##### SQLite3 DB Adapter Constants (`DBAdapters.DBSQLite`)

    #### `CDefSQLiteDBName`

    Default database filename.

    #### `CDefSQLiteDBTable`

    Default statistical table name.

    #### `CDefSQLiteDBTablePop`

    Default population statistical table name.

    #### `CDefSQLiteStatsGenFreq`

    Default generational frequency for dump statistics.

    #### `CDefSQLiteStatsCommitFreq`

    Default commit frequency.

    ##### MySQL DB Adapter Constants (`DBAdapters.DBMySQLAdapter`)

    #### `CDefMySQLDBName`

    Default database name.

    #### `CDefMySQLDBTable`

    Default statistical table name.

    #### `CDefMySQLDBTablePop`

    Default population statistical table name.

    #### `CDefMySQLStatsGenFreq`

    Default generational frequency for dump statistics.

    #### `CDefMySQLStatsCommitFreq`

    Default commit frequency.

    #### `CDefMySQLDBHost`

    Default MySQL connection host.

    #### `CDefMySQLDBPort`

    Default MySQL connection TCP port.

    ##### URL Post DB Adapter Constants (`DBAdapters.DBURLPost`)

    #### `CDefURLPostStatsGenFreq`

    Default generational frequency for dump statistics.

    ##### CSV File DB Adapter Constants (`DBAdapters.DBFileCSV`)

    #### `CDefCSVFileName`

    The default CSV filename to dump statistics.

    #### `CDefCSVFileStatsGenFreq`

    Default generational frequency for dump statistics.

    ##### XMP RPC DB Adapter Constants (`DBAdapters.DBXMLRPC`)

    #### `CDefXMLRPCStatsGenFreq`

    Default generational frequency for dump statistics.
"""
import logging

from . import Scaling
from .selections import Selectors
from .initializations import InitializationBinary, InitializationG1DList, InitializationG2DList
from .perturbations import MutatorBinary, MutatorG1DList, MutatorG2DList

from .perturbations.CrossoverG1DList import G1DListCrossoverSinglePoint

from .perturbations.CrossoverG2DList import G2DListCrossoverUniform
from .perturbations.CrossoverBinary import G1DBinaryStringXSinglePoint, G2DBinaryStringXUniform


# Logging system
CDefLogFile = "pyevolve.log"
CDefLogLevel = logging.DEBUG

# Types of sort
# - raw: uses the "score" attribute
# - scaled: uses the "fitness" attribute
sortType = {
    "raw": 0,
    "scaled": 1
}

# Optimization type
# - Minimize or Maximize the Evaluator Function
minimaxType = {"minimize": 0,
               "maximize": 1
               }

CDefESCKey = 27

CDefImportList = {"visual.graph": "you must install VPython !",
                  "csv": "csv module not found !",
                  "urllib": "urllib module not found !",
                  "sqlite3": "sqlite3 module not found, are you using Jython or IronPython ?",
                  "xmlrpclib": "xmlrpclib module not found !",
                  "MySQLdb": "MySQLdb module not found, you must install mysql-python !",
                  "pydot": "Pydot module not found, you must install Pydot to plot graphs !"}

####################
# Defaults section #
####################

# - Tournament selector
CDefTournamentPoolSize = 2

# - Scale methods defaults
CDefScaleLinearMultiplier = 1.2
CDefScaleSigmaTruncMultiplier = 2.0
CDefScalePowerLawFactor = 1.0005
CDefScaleBoltzMinTemp = 1.0
CDefScaleBoltzFactor = 0.05
# 40 temp. = 500 generations
CDefScaleBoltzStart = 40.0

# - Population Defaults
CDefPopSortType = sortType["scaled"]
CDefPopMinimax = minimaxType["maximize"]
CDefPopScale = Scaling.LinearScaling

# - GA Engine defaults
CDefGAGenerations = 100
CDefGAMutationRate = 0.02
CDefGACrossoverRate = 0.9
CDefGAPopulationSize = 80
CDefGASelector = Selectors.GRankSelector
CDefGAElitismReplacement = 1

# - This is general used by integer/real ranges defaults
CDefRangeMin = 0
CDefRangeMax = 100

# - G1DBinaryString defaults
CDefG1DBinaryStringMutator = MutatorBinary.G1DBinaryStringMutatorFlip
CDefG1DBinaryStringCrossover = G1DBinaryStringXSinglePoint
CDefG1DBinaryStringInit = InitializationBinary.G1DBinaryStringInitializator
CDefG1DBinaryStringUniformProb = 0.5

# - G2DBinaryString defaults
CDefG2DBinaryStringMutator = MutatorBinary.G2DBinaryStringMutatorFlip
CDefG2DBinaryStringCrossover = G2DBinaryStringXUniform
CDefG2DBinaryStringInit = InitializationBinary.G2DBinaryStringInitializator
CDefG2DBinaryStringUniformProb = 0.5

# - G1DList defaults
CDefG1DListMutIntMU = 2
CDefG1DListMutIntSIGMA = 10

CDefG1DListMutRealMU = 0
CDefG1DListMutRealSIGMA = 1

CDefG1DListMutator = MutatorG1DList.G1DListMutatorSwap
CDefG1DListCrossover = G1DListCrossoverSinglePoint
CDefG1DListInit = InitializationG1DList.G1DListInitializatorInteger
CDefG1DListCrossUniformProb = 0.5

# SBX Crossover defaults
# Crossover distribution index for SBX
# Larger Etac = similar to parents
# Smaller Etac = far away from parents
CDefG1DListSBXEtac = 10
CDefG1DListSBXEPS = 1.0e-14

# - G2DList defaults
CDefG2DListMutIntMU = 2
CDefG2DListMutIntSIGMA = 10

CDefG2DListMutRealMU = 0
CDefG2DListMutRealSIGMA = 1

CDefG2DListMutator = MutatorG2DList.G2DListMutatorSwap
CDefG2DListCrossover = G2DListCrossoverUniform
CDefG2DListInit = InitializationG2DList.G2DListInitializatorInteger
CDefG2DListCrossUniformProb = 0.5

# Gaussian Gradient
CDefGaussianGradientMU = 1.0
CDefGaussianGradientSIGMA = (1.0 / 3.0)  # approx. +/- 3-sigma is +/- 10%

# - DB Adapters SQLite defaults
CDefSQLiteDBName = "pyevolve.db"
CDefSQLiteDBTable = "statistics"
CDefSQLiteDBTablePop = "population"
CDefSQLiteStatsGenFreq = 1
CDefSQLiteStatsCommitFreq = 300

# - DB Adapters MySQL defaults
CDefMySQLDBName = "pyevolve"
CDefMySQLDBTable = "statistics"
CDefMySQLDBTablePop = "population"
CDefMySQLDBHost = "localhost"
CDefMySQLDBPort = 3306
CDefMySQLStatsGenFreq = 1
CDefMySQLStatsCommitFreq = 300

# - DB Adapters URL Post defaults
CDefURLPostStatsGenFreq = 100

# - DB Adapters CSV File defaults
CDefCSVFileName = "pyevolve.csv"
CDefCSVFileStatsGenFreq = 1

# - DB Adapter XML RPC
CDefXMLRPCStatsGenFreq = 20

# Util Consts
CDefBroadcastAddress = "255.255.255.255"
nodeType = {"TERMINAL": 0, "NONTERMINAL": 1}
