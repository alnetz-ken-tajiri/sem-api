from pydantic import BaseModel
from typing import List, Dict

class SEMRequest(BaseModel):
    measurement: str
    structural: str
    data: Dict[str, List[float]]

class SEMResponse(BaseModel):
    rmsea: float
    cfi:   float
    tli:   float
    chi2:  float
    dof:   int

