from typing import List, Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    """フロントから送られてくる 1 質問ぶんのデータ"""
    id: str                 # 質問 ID
    vector: List[float]     # 埋め込みベクトル


class ClusterRequest(BaseModel):
    """POST /cluster のリクエストスキーマ"""
    items: List[Item]
    k_fixed: Optional[int] = Field(
        None,
        ge=2,
        description="固定クラスタ数。None なら自動推定"
    )


class Cluster(BaseModel):
    """レスポンス内のクラスタ情報"""
    id: int
    questionIds: List[str]


class ClusterResponse(BaseModel):
    """POST /cluster のレスポンススキーマ"""
    k: int
    clusters: List[Cluster]
    silhouette: float
