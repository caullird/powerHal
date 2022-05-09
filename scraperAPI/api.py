from typing import Optional
from fastapi import FastAPI
from visualization.PowerCloud import PowerCloud
from visualization.PowerGraph import PowerGraph
from specific.openAlex.openAlex import openAlex
from specific.openCitation.openCitation import openCitation
from specific.googleScholar.googleScholar import googleScholar
from specific.hal.hal import hal
from specific.orcid.orcid import orcid
from config.DB import DB

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/openAlex")
def read_root():

    research = {
        "author_name" : "Salamatian",
        "author_forename" : "Kavé",
        "id_connected_user" : 1,
        "id_author_as_user" : 1
    }

    openAlex(research)

    return {"Hello": "World"}
