from pathlib import Path
from rito import rito
import pytest
import os

TEST_PARAMS = [rito.Validator.r5(), rito.Validator.r4(), rito.Validator.stu3(),]
RESOURCE_PATH = os.path.join(os.path.dirname(__file__), Path('resources'))


@pytest.fixture(name='validator', scope='module', params=TEST_PARAMS)
def fixture_validator(request):
    return request.param


def test_single_patient_valid(validator):
    resource_name = f'{validator.get_fhir_version()}_patient.json'
    result = validator.fhir_validate(RESOURCE_PATH + f'\\{resource_name}')
    assert result[resource_name] is True
