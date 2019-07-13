from __future__ import annotations

import datetime

import immutables
import pytz
import requests

import codep


class GetCurrentTime(codep.Partial[datetime.datetime]):
    @classmethod
    def run(cls, state: immutables.Map) -> datetime.datetime:
        response = requests.get("http://worldtimeapi.org/api/ip")
        assert response.status_code == 200
        payload = response.json()
        return datetime.datetime.fromisoformat(payload["utc_datetime"])


class GetDayOfYear(codep.Partial[int]):
    @classmethod
    def run(cls, state: immutables.Map) -> int:
        response = requests.get("http://worldtimeapi.org/api/ip")
        assert response.status_code == 200
        payload = response.json()
        return int(payload["day_of_year"])


class AddOneHour(codep.Partial[datetime.datetime]):
    depends = (GetCurrentTime,)

    @classmethod
    def run(cls, state: immutables.Map) -> datetime.datetime:
        return GetCurrentTime.value(state) + datetime.timedelta(hours=1)


class LocalTime(codep.Partial[datetime.datetime]):
    depends = (AddOneHour,)

    @classmethod
    def run(cls, state: immutables.Map) -> datetime.datetime:
        return AddOneHour.value(state).astimezone(pytz.timezone("Europe/Stockholm"))


class UTCTime(codep.Partial[datetime.datetime]):
    depends = (AddOneHour, GetDayOfYear)

    @classmethod
    def run(cls, state: immutables.Map) -> datetime.datetime:
        return AddOneHour.value(state).astimezone(datetime.timezone.utc)
