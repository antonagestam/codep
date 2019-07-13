import logging
import sys

import codep
from . import partials

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

utc, local_time = codep.run(partials.utc_time, partials.local_time)
logging.info(f"local time: {local_time}, utc time: {utc}")
