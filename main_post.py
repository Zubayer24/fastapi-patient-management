from fastapi import FastAPI, Path, HTTPException, Query, Field
import json
from pydantic import BaseModel, computed_field
from typing import Optional, Dict,List,Literal,Annotated

app = FastAPI()

class patient(BaseModel):
    id: Annotated[str,Field(...,description="ID of the patient in DB", examples="P002"  )] 
    name: Annotated[str,Field(...,description="Name of the patient", examples="Zubayer Hasan")] 
    city: Annotated[str,Field(...,description="City of residence of the patient")]
    age: Annotated[int, Field(...,description="Age of the patient", gt=0, lt=120)] 
    gender: Annotated[Literal["Male","Female","Others"],Field(...,description="Gender of the patient")] 
    height: Annotated[float, Field(...,gt=0, description="Height of the patient in meters")]  
    weight: Annotated[float, Field(...,gt=0, description="Weight of the patient in Kgs")]  

    @computed_field
    @property
    def bmi(self) -> float:
        bmi =  round(self.weight/(self.height**2), 2) 
        return bmi  
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Healthy weight"
        elif self.bmi <30:
            return "Overweight"
        else:
            return "obesity" 

def load_data():
    with open("patients.json","r") as f:
        data= json.load(f)
    return data 

@app.get("/")
def hello():
    return {"message": "patient management system API"}

@app.get("/about")
def about():
    return {"message": "A fully functional api to manage your patient records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="ID of the patient in DB", example="P001")):
    data= load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    

@app.get("/sort")
def sort_


