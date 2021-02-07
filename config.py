
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# ENVs
MONGO_URL = os.getenv("MONGO_URL")
MONGO_URL_LOCAL = os.getenv("MONGO_URL_LOCAL")
