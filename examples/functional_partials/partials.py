from __future__ import annotations

import datetime

import immutables
import pytz
import requests

import codep


@codep.make_partial()
def fetch_current_time(_state: immutables.Map) -> datetime.datetime:
    response = requests.get("http://worldtimeapi.org/api/ip")
    assert response.status_code == 200
    payload = response.json()
    return datetime.datetime.fromisoformat(payload["utc_datetime"])


@codep.make_partial()
def fetch_day_of_year(_state: immutables.Map) -> int:
    response = requests.get("http://worldtimeapi.org/api/ip")
    assert response.status_code == 200
    payload = response.json()
    return int(payload["day_of_year"])


@codep.decorators.make_partial(depends=(fetch_current_time,))
def add_one_hour(state: immutables.Map) -> datetime.datetime:
    return fetch_current_time.value(state) + datetime.timedelta(hours=1)


@codep.decorators.make_partial(depends=(add_one_hour,))
def local_time(state: immutables.Map) -> datetime.datetime:
    return add_one_hour.value(state).astimezone(pytz.timezone("Europe/Stockholm"))


@codep.decorators.make_partial(depends=(add_one_hour, fetch_day_of_year))
def utc_time(state: immutables.Map) -> datetime.datetime:
    return add_one_hour.value(state).astimezone(datetime.timezone.utc)
