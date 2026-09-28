from typing import Optional
from fastapi import FastAPI,status, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(
    title="RandiApp API",
    description="A páros randiapp backend kiszolgálója",
    version="0.1.0"
)

class RandiLetrehozas(BaseModel):
    cim: str
    kategoria: str
    koltseg: str

ALAP_RANDIK = [
    {"id": 1, "cim": "Csillagnézés forró teával a szabadban", "kategoria": "kulteri", "koltseg": "ingyenes"},
    {"id": 2, "cim": "Közös sushi készítés otthon", "kategoria": "belteri", "koltseg": "kozepes"},
    {"id": 3, "cim": "Társasjáték maraton rendelős pizzával", "kategoria": "belteri", "koltseg": "alacsony"},
    {"id": 4, "cim": "Séta és forró csokizás a városban", "kategoria": "kulteri", "koltseg": "alacsony"},
    {"id": 5, "cim": "Szabadulószoba kihívás kettesben", "kategoria": "belteri", "koltseg": "magas"},
]

@app.get("/")
def kezdooldal():
    return {"statusz": "online", "uzenet": "A RandiApp szerver fut!"}

@app.get("/api/randi/veletlen")
def veletlen_randi():
    return random.choice(ALAP_RANDIK)

@app.get("/randik")
def randi_szuro(kategoria: Optional[str]=None,
                koltseg: Optional[str]=None):
    eredmeny=ALAP_RANDIK

    if kategoria is not None:
        eredmeny=[r for r in eredmeny if r["kategoria"].lower()==kategoria.lower()]

    if koltseg is not None:
        eredmeny=[r for r in eredmeny if r["koltseg"].lower()==koltseg.lower()]

    return eredmeny

@app.post("/api/randik", status_code=status.HTTP_201_CREATED)
def uj_randi_letrehozasa(uj_randi: RandiLetrehozas):
    kovetkezo_id = len(ALAP_RANDIK) + 1
    uj_elem = {
        "id": kovetkezo_id,
        "cim": uj_randi.cim,
        "kategoria": uj_randi.kategoria,
        "koltseg": uj_randi.koltseg
    }
    ALAP_RANDIK.append(uj_elem)
    return uj_elem

@app.get("/randi/{randi_id}")
def egy_randi_lekerdezese(randi_id : int):
    for r in ALAP_RANDIK:
        if r["id"]==randi_id:
            return  r

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,detail=f"A(z) {randi_id} azonosítójú randi nem található."
    )

@app.delete("/randi/{randi_id}", status_code=status.HTTP_204_NO_CONTENT)
def randi_torlese(randi_id: int):
    for r in ALAP_RANDIK:
        if r["id"]==randi_id:
            ALAP_RANDIK.remove(r)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"A(z) {randi_id} azonosítójú randi nem található."
    )

@app.put("/randi/{randi_id}")
def randi_modositas(randi_id : int, modositott_randi : RandiLetrehozas):
    for r in ALAP_RANDIK:
        if r["id"]==randi_id:
            r["cim"]=modositott_randi.cim
            r["kategoria"]=modositott_randi.kategoria
            r["koltseg"]=modositott_randi.koltseg
        return r

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"A(z) {randi_id} azonosítójú randi nem található, így nem módosítható"
    )