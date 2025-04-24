from semopy import Model, stats
import pandas as pd

def run_sem(measurement: str, structural: str, data: dict):
    # ① モデル定義
    desc = f"{measurement}\n{structural}"
    model = Model(desc)

    # ② データ読み込み
    df = pd.DataFrame(data)
    model.fit(df)

    # ③ 統計量を取得
    #   DataFrame ではなく NamedTuple が欲しいので gather_statistics() を使う
    sem_stats = stats.gather_statistics(model)

    return {
        "rmsea": sem_stats.rmsea,
        "cfi":   sem_stats.cfi,
        "tli":   sem_stats.tli,
        "chi2":  sem_stats.chi2[0],
        "dof":   sem_stats.dof
    }
