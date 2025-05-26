from typing import List, Optional
from pydantic import BaseModel, Field

class ClusterRequest(BaseModel):
    embeddings: List[List[float]]
    k_fixed: Optional[int] = Field(None, ge=2, description="固定クラスタ数。None なら自動推定")

class ClusterResponse(BaseModel):
    k: int
    labels: List[int]
    silhouette: float
