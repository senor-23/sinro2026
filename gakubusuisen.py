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
st.write("高校生の特徴から、似ている大学生が多い学部学科を推薦します。")

# ===============================
# データ読み込み
# ===============================
df = pd.read_excel("excel3.xlsx")

print(df.columns.tolist())

# ===============================
# 列定義
# ===============================

# 学部学科列
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

# 特徴列
character_columns = [
    'ISTJ(管理者)','ISFJ(擁護者)','INFJ(提唱者)','INTJ(建築家)',
    'ISTP(巨匠)','ISFP(冒険家)','INFP(仲介者)','INTP(論理学者)',
    'ESTP(起業家)','ESFP(エンターテイナー)','ENFP(広報活動家)','ENTP(討論者)',
    'ESTJ(幹部)','ESFJ(領事)','ENFJ(主人公)','ENTJ(指揮官)'
]
features_calumns = ["男性","女性"]

bunri_columns = ["文系","理系"]

decision_columns =["8月以前","8月以降"]

bukatu_columns = ["運動部","文化部","未所属"]

interest_columns = [ 
    "音楽","アニメ・漫画・映画","読書","ゲーム","アウトドア","勉強",
    "グルメ","旅行","SNS","推し活","スポーツ","動植物","ファッション・メイク","芸術","投資","その他"
]

# ===============================
# 重み設定
# ===============================
def weight_of(name):

    if name in ["文系", "理系"]:
        return 3.0

    if name in [
        "音楽","アニメ・漫画・映画","読書","ゲーム","アウトドア","勉強",
        "グルメ","旅行","SNS","推し活","スポーツ","動植物","ファッション・メイク",
        "芸術","投資","その他"
    ]:
        return 2.5

    if "満足度_" in name:
        return 2.0

    if name in [
        "運動部",
        "文化部",
        "未所属",
        "8月以前",
        "8月以降"
    ]:
        return 1.0

    if name in ["男性", "女性"]:
        return 0.5

    return 1.5

# ===============================
# サイドバー
# ===============================
selected_features = []

mbti = st.selectbox("MBTI", character_columns)
gender = st.selectbox("性別",features_calumns)
bunri = st.selectbox("文理",bunri_columns)
decision = st.selectbox("進路決定時期",decision_columns)
bukatu = st.selectbox("部活動・サークル",bukatu_columns)
shumi = st.checkbox(
    "音楽","アニメ・漫画・映画","読書","ゲーム","アウトドア","勉強",
    "グルメ","旅行","SNS","推し活","スポーツ","動植物","ファッション・メイク","芸術","投資","その他"
    ,interest_columns)


# ===============================
# 推薦計算
# ===============================
if st.button("推薦を計算する"):

    if len(selected_features) == 0:
        st.warning("特徴を選択してください")

    else:

        department_scores = []

        # ===============================
        # 各学部ごとのスコア計算
        # ===============================
        for dept in departments:

            dept_students = df[df[dept] == 1]

            scores = []

            matched_features = []

            for _, student in dept_students.iterrows():

                score = 0

                for feature in selected_features:

                    if student[feature] == 1:

                        score += weight_of(feature)
                        matched_features.append(feature)

                scores.append(score)

            # 平均類似度
            avg_score = 0

            if len(scores) > 0:
                avg_score = sum(scores) / len(scores)

            department_scores.append({
                "学部学科": dept,
                "スコア": round(avg_score, 2),
                "人数": len(dept_students),
                "一致特徴": list(set(matched_features))
            })

        # ===============================
        # スコア順に並べ替え
        # ===============================
        department_scores = sorted(
            department_scores,
            key=lambda x: x["スコア"],
            reverse=True
        )

        # ===============================
        # 結果表示
        # ===============================
        st.subheader("推薦結果")

        for i, result in enumerate(department_scores[:8]):

            st.markdown(f"## {i+1}位 {result['学部学科']}")

            st.metric(
                label="推薦スコア",
                value=result["スコア"]
            )

            st.write(f"参照学生数：{result['人数']}人")

            if len(result["一致特徴"]) > 0:
                st.write("一致した特徴")

                cols = st.columns(4)

                for idx, feature in enumerate(result["一致特徴"][:8]):
                    cols[idx % 4].success(feature)

            st.divider()

# ===============================
# 説明
# ===============================
with st.expander("計算ロジック"):

    st.write("""
    1. 高校生が特徴を選択
    2. 各大学生との特徴一致数を計算
    3. 一致特徴に重みを加算
    4. 学部学科ごとに平均類似度を算出
    5. スコア順に推薦
    """)
