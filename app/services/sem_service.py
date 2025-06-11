from semopy import Model, stats
import pandas as pd
import numpy as np

def run_sem(measurement: str, structural: str, data: dict[str, list]):
    # 1) モデル定義
    desc  = f"{measurement}\n{structural}"
    model = Model(desc, mimic_lavaan=True)      # lavaan 互換

    # 2) データ前処理
    df = pd.DataFrame(data, dtype=float).dropna()
    df = (df - df.mean()) / df.std(ddof=0)      # 標準化で収束を安定化

    # 3) フィット
    model.fit(
        df,
        obj="MLW",               # White 補正付き ML
        solver="SLSQP",
        options={"maxiter": 1000}   # ← SciPy へ渡す
    )

    # 4) 指標取得
    st = stats.gather_statistics(model)
    out = {
        "rmsea": _safe(st.rmsea),
        "cfi":   _safe(st.cfi),
        "tli":   _safe(st.tli),
        "chi2":  _safe(st.chi2[0]),
        "dof":   int(st.dof)
    }
    if not all(v is None or np.isfinite(v) for v in out.values()):
        raise ValueError("Non-finite estimates (NaN/inf) detected.")
    return out


def _safe(x):
    """NaN / inf → None（JSON では null）"""
    x = float(x)
    return None if not np.isfinite(x) else x
