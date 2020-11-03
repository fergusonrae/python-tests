""" pytest config file for setting up fixtures and spark imports for testing """

import logging
from pathlib import Path
import pytest
import shutil
import tempfile

from pyspark.sql import SparkSession

def quiet_py4j():
    """ Turn down spark logging for the test context """
    logger = logging.getLogger('py4j')
    logger.setLevel(logging.WARN)

# Add the string 'yarn' in params to run spark tests both locally and with yarn
# Currently set to only test local
@pytest.fixture(scope='session', params=['local'])
def get_session(request) -> SparkSession:
    """Returns a spark session object for testing locally
    local[2] meaning two threads - which represents 'minimal' parallelism"""
    if request.param == 'local':
        spark_session = (SparkSession
                         .builder
                         .appName('pytest-pyspark-local-testing')
                         .master('local[2')
                         .enableHiveSupport()
                         .getOrCreate())
    elif request.param == 'yarn':
        spark_session = (SparkSession
                         .builder
                         .appName('pytest-pysaprk-yarn-testing')
                         .master('yarn-client')
                         .config('spark.executor.memory', '1g')
                         .config('spark.executor.instances', 2)
                         .enableHiveSupport()
                         .getOrCreate())
    yield spark_session
    spark_session.stop()

@pytest.fixture(scope='module')
def temp_dir():
    """Creates a directory to store testing files and then once the module is done with it
    deletes all contents"""
    temp_dir_path = Path(tempfile.mkdtemp())
    yield temp_dir_path
    shutil.rmtree(temp_dir_path)