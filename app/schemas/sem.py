from pydantic import BaseModel
from typing import List, Dict, Optional


class SEMRequest(BaseModel):
    measurement: str
    structural: str
    data: Dict[str, List[float]]


class SEMResponse(BaseModel):
    """Fit indices returned by the SEM engine.

    NaN や inf になる指標は `None` (JSON では `null`) として返します。\n    フロント側では `null` チェックで表示制御してください。"""
    rmsea: Optional[float] = None
    cfi: Optional[float] = None
    tli: Optional[float] = None
    chi2: Optional[float] = None
    dof: int
