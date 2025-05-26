from fastapi import APIRouter, HTTPException

from app.schemas.cluster import ClusterRequest, ClusterResponse
from app.services.cluster_service import auto_kmeans

router = APIRouter()


@router.post("/", response_model=ClusterResponse)
def cluster(req: ClusterRequest):
    """
    ベクトルと ID を受け取り:
      1. k-means（自動または固定）でクラスタリング
      2. Silhouette を計算
      3. {cluster_id: [questionIds]} 形式で返す
    """
    try:
        # --- 入力を ID とベクトルに分離 --------------------
        ids = [item.id for item in req.items]
        vectors = [item.vector for item in req.items]

        if len(vectors) < 3:
            raise HTTPException(status_code=400, detail="Need at least 3 items")

        # --- クラスタリング --------------------------------
        if req.k_fixed is not None:
            k, labels, sil = auto_kmeans(vectors, req.k_fixed, req.k_fixed)
        else:
            k, labels, sil = auto_kmeans(vectors)

        # --- labels → {clusterId: [questionIds]} へ変換 ----
        clusters_map = {}
        for qid, lbl in zip(ids, labels):
            clusters_map.setdefault(lbl, []).append(qid)

        clusters = [
            {"id": cid, "questionIds": qids}
            for cid, qids in clusters_map.items()
        ]

        return {"k": k, "clusters": clusters, "silhouette": sil}

    except HTTPException:
        # すでに整形済みのものはそのまま投げる
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
