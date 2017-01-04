import os
os.environ["EMIS_MONITOR_CONFIGURATION"] = "production"
from server import app


app.run(host="0.0.0.0")
