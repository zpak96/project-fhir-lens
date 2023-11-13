from pathlib import Path
from rito import rito
import logging
import pytest
import os


LOGGER = logging.getLogger(__name__)
TEST_VALIDATORS = [rito.Validator.r5(), rito.Validator.r4(), rito.Validator.stu3()]
TEST_RESOURCES = ['patient', 'organization', 'observation']
DIRECTORY_PATH = os.path.join(Path(__file__).resolve().parent, Path('data'))


@pytest.fixture(name='resource', scope='module', params=TEST_RESOURCES)
def fixture_resource(request):
    return request.param


@pytest.fixture(name='validator', scope='module', params=TEST_VALIDATORS)
def fixture_validator(request):
    return request.param


def test_valid_fast_file_validate(validator, resource):
    fhir_version = validator.fhir_version
    resource_name = f'{resource}.json'
    LOGGER.info(f'Validator Version :: {fhir_version}')
    LOGGER.info(f'Resource File :: {resource}')

    result = validator.file_validate(DIRECTORY_PATH + f'/{fhir_version}/{resource}.json')
    assert result[resource_name] is True


def test_valid_fast_dir_validate(validator):
    fhir_version = validator.fhir_version
    LOGGER.info(f'Validator Version :: {fhir_version}')

    result = validator.dir_validate(DIRECTORY_PATH + f'/{fhir_version}')
    assert result == {'observation.json': True, 'organization.json': True, 'patient.json': True}
