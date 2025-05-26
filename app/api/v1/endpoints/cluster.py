from fastapi import APIRouter, HTTPException
from app.schemas.cluster import ClusterRequest, ClusterResponse
from app.services.cluster_service import auto_kmeans

router = APIRouter()

@router.post("/", response_model=ClusterResponse)
def cluster(req: ClusterRequest):
    try:
        if req.k_fixed is not None:
            k, labels, sc = auto_kmeans(req.embeddings, req.k_fixed, req.k_fixed)
        else:
            k, labels, sc = auto_kmeans(req.embeddings)
        return {"k": k, "labels": labels, "silhouette": sc}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
