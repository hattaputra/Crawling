from fastapi import FastAPI

app = FastAPI()

from src.conf import *
from src.routes import route