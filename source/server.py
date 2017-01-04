import os
from emis_monitor import create_app


app = create_app(os.getenv("EMIS_MONITOR_CONFIGURATION"))
