from semopy import Model, stats
import pandas as pd
import numpy as np

def run_sem(measurement: str, structural: str, data: dict[str, list[int | float]]):
    """
    measurement / structural は lavaan 書式の文字列
    data は {"Q1": [..], "Q2": [..]} 形式
    戻り値は JSON 化しても安全な float / None のみ
    """
    # ── 1. モデル定義 ───────────────────────────────────────────
    desc = f"{measurement}\n{structural}"
    #   - mimic_lavaan=True で lavaan と同じ制約を入れる
    #   - baseline_models=False なら CFI/TLI を後で自力計算
    model = Model(desc, mimic_lavaan=True)

    # ── 2. データ読み込み & 前処理 ────────────────────────────
    df = pd.DataFrame(data, dtype=float)

    # a) 欠損を落とす（あるなら）
    df = df.dropna()
    # b) 定数列（std == 0）をはじく
    is_const = df.std(ddof=0) == 0
    if is_const.any():
        raise ValueError(f"constant columns found: {list(df.columns[is_const])}")

    # c) 標準化すると収束が劇的に安定
    df = (df - df.mean()) / df.std(ddof=0)

    # ── 3. フィット ───────────────────────────────────────────
    # ︙“N < パラメータ” のときは MLW + 疑似逆行列が安全
    model.fit(
        df,
        obj="MLW",          # MLW = maximum-likelihood with White correction
        max_iter=1000,
        regularization="l2",
        l2_lambda=0.1       # サンプル不足対策の弱い正則化
    )

    # ── 4. 統計量取得 ───────────────────────────────────────
    sem_stats = stats.gather_statistics(model)

    # ── 5. NaN / inf を None に変換して JSON セーフに ──────
    out = dict(
        rmsea = _clean(sem_stats.rmsea),
        cfi   = _clean(sem_stats.cfi),
        tli   = _clean(sem_stats.tli),
        chi2  = _clean(sem_stats.chi2[0]),
        dof   = int(sem_stats.dof)    # dof は整数
    )

    # ── 6. すべて finite かチェックして返す ─────────────────
    if not all(v is None or np.isfinite(v) for v in out.values()):
        raise ValueError("Non-finite estimates remained after cleaning.")

    return out


def _clean(x: float | np.ndarray) -> float | None:
    """NaN / inf → None（JSON では null）"""
    try:
        x = float(x)  # ndarray → scalar
    except Exception:
        return None
    return None if not np.isfinite(x) else x
