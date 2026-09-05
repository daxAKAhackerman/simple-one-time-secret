from datetime import datetime

import pytest
from freezegun import freeze_time
from schemas import is_less_than_one_year_away


class TestIsLessThanOneYearAway:
    @freeze_time("2023-03-07")
    def test__given_valid_date__then_date_returned(self):
        date = datetime.strptime("2023-03-09", "%Y-%m-%d").astimezone()
        assert is_less_than_one_year_away(date) == date

    @freeze_time("2023-03-07")
    def test__given_invalid_date__then_raise(self):
        date = datetime.strptime("2025-06-03", "%Y-%m-%d").astimezone()
        with pytest.raises(ValueError):
            is_less_than_one_year_away(date)
