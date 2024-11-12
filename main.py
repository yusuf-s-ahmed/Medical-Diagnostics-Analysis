from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the schema for BPM data
class BPMData(BaseModel):
    bpm: float

# Create an endpoint that accepts POST requests with BPM data
@app.post("/bpm")
async def receive_bpm(data: BPMData):
    # Here you can store or process the BPM data as needed
    print(f"Received BPM: {data.bpm}")
    return {"message": "BPM received successfully"}
