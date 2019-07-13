from __future__ import annotations

import datetime

import immutables
import requests

import codep


class GetCurrentTime(codep.Partial):
    @classmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        response = requests.get("http://worldtimeapi.org/api/ip")
        assert response.status_code == 200
        payload = response.json()
        return state.set(
            "current_time", datetime.datetime.fromisoformat(payload["utc_datetime"])
        )


class GetDayOfYear(codep.Partial):
    @classmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        response = requests.get("http://worldtimeapi.org/api/ip")
        assert response.status_code == 200
        payload = response.json()
        return state.set("day_of_year", payload["day_of_year"])


class AddOneHour(codep.Partial):
    depends = (GetCurrentTime,)

    @classmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        return state.set(
            "current_time", state["current_time"] + datetime.timedelta(hours=1)
        )


class LocalTime(codep.Partial):
    depends = (AddOneHour,)

    @classmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        import pytz

        t = state["current_time"]
        print(t.astimezone(pytz.timezone("Europe/Stockholm")))
        return state


class UTCTime(codep.Partial):
    depends = (AddOneHour, GetDayOfYear)

    @classmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        t = state["current_time"]
        print(t.astimezone(datetime.timezone.utc))
        return state
