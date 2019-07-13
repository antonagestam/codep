from __future__ import annotations

import datetime

import immutables
import requests

import codep


@codep.make_partial()
def fetch_current_time(state: immutables.Map) -> immutables.Map:
    response = requests.get("http://worldtimeapi.org/api/ip")
    assert response.status_code == 200
    payload = response.json()
    return state.set(
        "current_time", datetime.datetime.fromisoformat(payload["utc_datetime"])
    )


@codep.make_partial()
def fetch_day_of_year(state: immutables.Map) -> immutables.Map:
    response = requests.get("http://worldtimeapi.org/api/ip")
    assert response.status_code == 200
    payload = response.json()
    return state.set("day_of_year", payload["day_of_year"])


@codep.make_partial(depends=(fetch_current_time,))
def add_one_hour(state: immutables.Map) -> immutables.Map:
    return state.set(
        "current_time", state["current_time"] + datetime.timedelta(hours=1)
    )


@codep.make_partial(depends=(add_one_hour,))
def local_time(state: immutables.Map) -> immutables.Map:
    import pytz

    t = state["current_time"]
    print(t.astimezone(pytz.timezone("Europe/Stockholm")))
    return state


@codep.make_partial(depends=(add_one_hour, fetch_day_of_year))
def utc_time(state: immutables.Map) -> immutables.Map:
    t = state["current_time"]
    print(t.astimezone(datetime.timezone.utc))
    print(state["day_of_year"])
    return state
