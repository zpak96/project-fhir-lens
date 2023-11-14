from pathlib import Path
from rito import rito
import logging
import pytest
import os


LOGGER = logging.getLogger(__name__)

TEST_VALIDATORS = [
    rito.Validator.stu3(),
    rito.Validator.r4(),
    rito.Validator.r4b(),
    rito.Validator.r5()
]

TEST_RESOURCES = ['patient', 'organization', 'observation']
TEST_DATA_BASE_PATH = os.path.join(Path(__file__).resolve().parent, Path('data'))


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

    file_path = TEST_DATA_BASE_PATH + f'/{fhir_version}/{resource}.json'
    result = validator.file_validate(file_path)

    assert result[resource_name] is True


def test_valid_verbose_file_validate(validator, resource):
    fhir_version = validator.fhir_version
    resource_name = f'{resource}.json'

    LOGGER.info(f'Validator Version :: {fhir_version}')
    LOGGER.info(f'Resource File :: {resource}')

    file_path = TEST_DATA_BASE_PATH + f'/{fhir_version}/{resource}.json'
    result = validator.file_validate(file_path, verbose=True)

    assert result[resource_name] is True


def test_valid_fast_dir_validate(validator):
    fhir_version = validator.fhir_version
    LOGGER.info(f'Validator Version :: {fhir_version}')

    directory_path = TEST_DATA_BASE_PATH + f'/{fhir_version}'
    result = validator.dir_validate(directory_path)

    assert result == {'observation.json': True, 'organization.json': True, 'patient.json': True}


def test_valid_verbose_dir_validate(validator):
    fhir_version = validator.fhir_version
    LOGGER.info(f'Validator Version :: {fhir_version}')

    directory_path = TEST_DATA_BASE_PATH + f'/{fhir_version}'
    result = validator.dir_validate(directory_path, verbose=True)

    assert result == {'observation.json': True, 'organization.json': True, 'patient.json': True}
