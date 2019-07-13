import codep
from . import partials

local_time, utc = codep.run(partials.LocalTime, partials.UTCTime)
