from datetime import datetime

import pytest
from freezegun import freeze_time
from schemas import is_valid_expiration


class TestIsLessThanOneYearAway:
    @freeze_time("2023-03-07")
    def test__given_valid_date__then_date_returned(self):
        date = datetime.strptime("2023-03-09", "%Y-%m-%d").astimezone()
        assert is_valid_expiration(date) == date

    @freeze_time("2023-03-07")
    def test__given_date_too_far__then_raise(self):
        date = datetime.strptime("2025-06-03", "%Y-%m-%d").astimezone()
        with pytest.raises(ValueError):
            is_valid_expiration(date)

    @freeze_time("2023-03-07")
    def test__given_date_in_the_past__then_raise(self):
        date = datetime.strptime("2023-03-06", "%Y-%m-%d").astimezone()
        with pytest.raises(ValueError):
            is_valid_expiration(date)
