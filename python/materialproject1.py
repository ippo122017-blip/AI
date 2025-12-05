from mp_api.client import MPRester

# 環境変数 MP_API_KEY を自動で使う
with MPRester() as mpr:
    # 例: Si (mp-149) の summary データを取得
    docs = mpr.materials.summary.search(material_ids=["mp-149"])
    doc = docs[0]

    print("MP-ID:", doc.material_id)
    print("式:", doc.formula_pretty)
    print("バンドギャップ [eV]:", doc.band_gap)
