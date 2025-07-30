import pytest


def test_equal_or_not_equal():
    assert 1 == 1
    assert 2 != 3

def test_is_instance():
    assert isinstance("Hello", str)
    assert not isinstance(123, str)

def test_boolean_checks():
    validated = True
    assert validated is True
    assert ('Hello' == 'Hello World') is False

def test_type():
    assert type(5) is int
    assert type("Test") is not int

def test_greater_than():
    assert 10 > 5
    assert not (3 > 4)

def test_list():
    sample_list = [1, 2, 3]
    assert len(sample_list) == 3
    assert 2 in sample_list

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_student():
    return Student("Jane", "Doe", "Engineering", 3)

def test_person_initialization(default_student):
    assert default_student.first_name == "Jane"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Engineering"
    assert default_student.years == 3