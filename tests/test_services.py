import pytest
from datetime import datetime, timedelta

from ponto_eletronico.models import UserConfig
from ponto_eletronico.services import TimeClockCalculator

@pytest.fixture
def cfg_single():
    return UserConfig(6.0, two_shifts=False)

@pytest.fixture
def cfg_double():
    return UserConfig(8.0, two_shifts=True, break_duration=60,
                      overtime_allowed=True, max_overtime_hours=2.0)

def test_expected_exit_single(cfg_single):
    calc = TimeClockCalculator(cfg_single)
    entry = datetime(2025, 5, 10, 9, 0)
    assert calc.expected_exit(entry) == entry + timedelta(hours=6)

def test_expected_exit_double(cfg_double):
    calc = TimeClockCalculator(cfg_double)
    entry = datetime(2025, 5, 10, 8, 0)
    assert calc.expected_exit(entry) == datetime(2025, 5, 10, 17, 0)

def test_worked_and_overtime_no_extra(cfg_double):
    calc = TimeClockCalculator(cfg_double)
    entries = [datetime(2025, 5, 10, 8, 0), datetime(2025, 5, 10, 12, 0)]
    exit_time = datetime(2025, 5, 10, 17, 0)
    worked, extra = calc.worked_and_overtime(entries, exit_time)
    assert worked == timedelta(hours=8)
    assert extra == timedelta()

def test_worked_and_overtime_with_extra(cfg_double):
    calc = TimeClockCalculator(cfg_double)
    entries = [datetime(2025, 5, 10, 8, 0), datetime(2025, 5, 10, 12, 0)]
    exit_time = datetime(2025, 5, 10, 19, 0)
    worked, extra = calc.worked_and_overtime(entries, exit_time)
    assert worked == timedelta(hours=8)
    assert extra == timedelta(hours=2)
