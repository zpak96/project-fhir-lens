from rito import rito


def test_validator_no_version():
    try:
        validator = rito.Validator()
        assert False
    except TypeError as e:
        assert True


def test_validator_unsupported_version():
    try:
        validator = rito.Validator('fake-version')
        assert False
    except LookupError as e:
        assert True


def test_r5_create():
    r5 = rito.Validator('r5')
    r5_cls_method = rito.Validator.r5()
    assert r5.get_fhir_version() == 'r5'
    assert r5_cls_method.get_fhir_version() == 'r5'


def test_r4_create():
    r4 = rito.Validator('r4')
    r4_cls_method = rito.Validator.r4()
    assert r4.get_fhir_version() == 'r4'
    assert r4_cls_method.get_fhir_version() == 'r4'


def test_stu3_create():
    stu3 = rito.Validator('stu3')
    stu3_cls_method = rito.Validator.stu3()
    assert stu3.get_fhir_version() == 'stu3'
    assert stu3_cls_method.get_fhir_version() == 'stu3'


