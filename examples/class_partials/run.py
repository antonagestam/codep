import codep
from . import partials

local_time, utc = codep.run(partials.LocalTime, partials.UTCTime)
print(f"local time: {local_time}, utc time: {utc}")
