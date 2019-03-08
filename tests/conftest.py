import os
import pytest
import urllib3

from gen3.auth import Gen3Auth
from gen3.submission import Gen3Submission


DEFAULT_CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
DEFAULT_ENDPOINT = 'https://localhost'

# DEFAULT_CREDENTIALS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen3.compbio.credentials.json')
# DEFAULT_ENDPOINT = 'https://gen3.compbio.ohsu.edu'

DEFAULT_MSG = 'InsecureRequestWarning disabled'
os.environ['CURL_CA_BUNDLE']=''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def pytest_report_header(config):
    return "gen3 config: {} {} {}".format(DEFAULT_CREDENTIALS_PATH, DEFAULT_ENDPOINT, DEFAULT_MSG)


@pytest.fixture(scope="session")
def submission_client(endpoint = DEFAULT_ENDPOINT, refresh_file=DEFAULT_CREDENTIALS_PATH):
    auth = Gen3Auth(endpoint, refresh_file=refresh_file)
    assert auth , 'should return an auth client'
    submission_client = Gen3Submission(endpoint, auth)
    assert submission_client , 'should return a submission client'
    assert 'delete_program' in dir(submission_client), 'should have a delete_program method'
    assert 'create_program' in dir(submission_client), 'should have a create_program method'
    return submission_client
