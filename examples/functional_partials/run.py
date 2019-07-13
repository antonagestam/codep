import codep
from . import partials

utc, local_time = codep.run(partials.utc_time, partials.local_time)
print(f"local time: {local_time}, utc time: {utc}")
