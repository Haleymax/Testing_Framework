import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--jobId", action="store", help="The jobid corresponding to the apk package"
    )
    parser.addoption(
        "--serial", action="store", default="", help="Android device serial"
    )
    parser.addoption(
        "--casenum", action="store", default="all", help="Number of test cases"
    )
    parser.addoption(
        "--download", action="store", default=False, help="Download apk from Gitlab"
    )

@pytest.fixture(scope='session')
def get_job_id(pytestconfig):
    return pytestconfig.getoption("--jobId")


@pytest.fixture(scope='session')
def get_serial(pytestconfig):
    return pytestconfig.getoption("--serial")


@pytest.fixture(scope='session')
def get_download(pytestconfig):
    return pytestconfig.getoption("--download")