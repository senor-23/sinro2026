import streamlit as st
import pandas as pd

# ===============================
# ページ設定
# ===============================
st.set_page_config(
    page_title="学部学科 推薦AI",
    layout="wide"
)

st.title("学部学科 推薦AI")
st.write("高校生の特徴から、似ている大学生を探し、満足度の高い学部学科を推薦します。")

# ===============================
# データ読み込み
# ===============================
df = pd.read_excel("excel3 (1).xlsx")

# ===============================
# 学部学科列
# ===============================
departments = [
    "経済学部_経済学科",
    "経営学部_マネジメント学科",
    "法学部_法律学科",
    "法学部_法政策学科",
    "現代社会学部_現代社会学科",
    "現代社会学部_健康スポーツ社会学科",
    "国際関係学部_国際関係学科",
    "外国語学部_英語学科",
    "外国語学部_ヨーロッパ言語学科",
    "外国語学部_アジア言語学科",
    "文化学部_文化構想学科",
    "文化学部_京都文化学科",
    "文化学部_文化観光学科",
    "理学部_数理科学科",
    "理学部_物理科学科",
    "理学部_宇宙物理・気象学科",
    "情報理工学部_情報理工学科",
    "生命科学部_先端生命科学科",
    "生命科学部_産業生命科学科",
    "アントレプレナーシップ学環"
]

# ===============================
# 特徴列
# ===============================
character_columns = [
    'ISTJ(管理者)','ISFJ(擁護者)','INFJ(提唱者)','INTJ(建築家)',
    'ISTP(巨匠)','ISFP(冒険家)','INFP(仲介者)','INTP(論理学者)',
    'ESTP(起業家)','ESFP(エンターテイナー)','ENFP(広報活動家)','ENTP(討論者)',
    'ESTJ(幹部)','ESFJ(領事)','ENFJ(主人公)','ENTJ(指揮官)'
]

gender_columns = ["男性", "女性"]

bunri_columns = ["文系", "理系"]

decision_columns = ["8月以前", "8月以降"]

bukatu_columns = ["運動部", "文化部", "未所属"]

# ===============================
# 重み設定
# ===============================
def weight_of(name):

    if name in ["文系", "理系"]:
        return 3.0

    if name in [
        "語学","数学","歴史","資格",
        "ビジネス","投資","旅行","SNS","芸術"
    ]:
        return 2.5

    if name in ["男性", "女性"]:
        return 0.5

    return 1.5

# ===============================
# 入力UI
# ===============================
mbti = st.selectbox("MBTI", character_columns)

gender = st.selectbox("性別", gender_columns)

bunri = st.selectbox("文理", bunri_columns)

decision = st.selectbox("進路決定時期", decision_columns)

bukatu = st.selectbox("部活動・サークル", bukatu_columns)

main_hobbies = st.multiselect(
    "趣味（3つまで選択可能）",
    [
        "音楽","アニメ・漫画・映画","読書","ゲーム","アウトドア","勉強",
        "グルメ","旅行","SNS","推し活","スポーツ",
        "動植物","ファッション・メイク","芸術","投資","その他"
    ],
    max_selections=3
)

selected_sub_hobbies = []

# ===============================
# サブ項目
# ===============================

# 音楽
if "音楽" in main_hobbies:

    music = st.multiselect(
        "好きな音楽ジャンル",
        [
            "j-pop",
            "k-pop",
            "洋楽"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(music)

# アニメ・漫画・映画
if "アニメ・漫画・映画" in main_hobbies:

    anime = st.multiselect(
        "好きなジャンル（アニメ・漫画・映画）",
        [
            "バトル・アクション",
            "SF・ファンタジー",
            "恋愛・ラブコメ",
            "ミステリー・サスペンス",
            "スポーツ(漫画)",
            "コメディ"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(anime)

# 読書
if "読書" in main_hobbies:

    books = st.multiselect(
        "好きな読書ジャンル",
        [
            "小説",
            "ビジネス",
            "ライトノベル",
            "エッセイ",
            "学術書"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(books)

# ゲーム
if "ゲーム" in main_hobbies:

    games = st.multiselect(
        "好きなゲームジャンル",
        [
            "アクション",
            "RPG",
            "シュミレーション",
            "パズル",
            "ソシャゲ"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(games)

# アウトドア
if "アウトドア" in main_hobbies:

    outdoor = st.multiselect(
        "アウトドアの趣味",
        [
            "キャンプ",
            "釣り",
            "登山",
            "フェス"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(outdoor)

# 勉強
if "勉強" in main_hobbies:

    study = st.multiselect(
        "興味のある勉強分野",
        [
            "語学",
            "数学",
            "歴史",
            "資格"
        ],max_selections=1
    )

    selected_sub_hobbies.extend(study)

# ===============================
# 推薦計算
# ===============================
if st.button("推薦を計算する"):

    # -------------------------------
    # 入力特徴をまとめる
    # -------------------------------
    selected_features = []

    selected_features.extend([
        mbti,
        gender,
        bunri,
        decision,
        bukatu
    ])

    selected_features.extend(main_hobbies)

    selected_features.extend(selected_sub_hobbies)

    # 重複削除
    selected_features = list(set(selected_features))

    # ===============================
    # 類似学生を探す
    # ===============================
    similarity_scores = []

    for idx, student in df.iterrows():

        score = 0
        matched = []

        for feature in selected_features:

            # 列が存在する場合のみ
            if feature in df.columns:

                # 一致しているか
                if student[feature] == 1:

                    score += weight_of(feature)
                    matched.append(feature)

        similarity_scores.append({
            "index": idx,
            "score": score,
            "matched": matched
        })

    # ===============================
    # 類似度順
    # ===============================
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x["score"],
        reverse=True
    )

    # 上位10人を取得
    top_students = similarity_scores[:10]

    # ===============================
    # 学部別 満足度集計
    # ===============================
    department_scores = []

    for dept in departments:

        total_satisfaction = 0
        matched_count = 0

        matched_features = []

        for sim in top_students:

            student = df.iloc[sim["index"]]

            # その学部所属か
            if student[dept] == 1:

                # 満足度列取得
                satisfaction = 0

                for i in range(1, 11):

                    col = f"満足度_{i}"

                    if col in df.columns and student[col] == 1:
                        satisfaction = i
                        break

                # 類似度 × 満足度
                total_satisfaction += sim["score"] * satisfaction

                matched_count += 1

                matched_features.extend(sim["matched"])

        # 平均
        avg_score = 0

        if matched_count > 0:

            avg_score = total_satisfaction / matched_count

        department_scores.append({

            "学部学科": dept,

            "推薦スコア": round(avg_score, 2),

            "一致人数": matched_count,

            "一致特徴": list(set(matched_features))

        })

    # ===============================
    # ソート
    # ===============================
    department_scores = sorted(
        department_scores,
        key=lambda x: x["推薦スコア"],
        reverse=True
    )

    # ===============================
    # 結果表示
    # ===============================
    st.subheader("推薦結果")

    for i, result in enumerate(department_scores[:8]):

        st.markdown(f"## {i+1}位：{result['学部学科']}")

        st.metric(
            label="推薦スコア",
            value=result["推薦スコア"]
        )

        st.write(f"一致した類似学生数：{result['一致人数']}人")

        if len(result["一致特徴"]) > 0:

            st.write("一致した特徴")

            cols = st.columns(4)

            for idx, feature in enumerate(result["一致特徴"][:8]):

                cols[idx % 4].success(feature)

        st.divider()

# ===============================
# ロジック説明
# ===============================
with st.expander("推薦ロジック"):

    st.write("""
    1. 高校生が特徴を入力
    2. 各大学生との特徴一致数を計算
    3. 一致特徴に重みを加算して類似度算出
    4. 類似度の高い学生を抽出
    5. 類似学生の満足度を参照
    6. 満足度の高い学部学科を推薦
    """)
