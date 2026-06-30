import streamlit as st
import pandas as pd
from departments import departments

st.set_page_config(
    page_title="学部学科推薦システム",
    layout="wide"
)

st.title("🎓 学部学科推薦システム")

st.write("以下の質問について最も当てはまるものを選択してください。")

# -----------------------------
# 質問
# -----------------------------

questions = {

"思考力":[

"ニュースや他人の意見を聞いたとき、『本当にそうなのかな？』『別の視点はないか？』とつい深く考えてしまう。",
"複雑な問題に対して、感情的に判断するのではなく、データを集めて筋道を立てて解決策を導き出すのが好きだ。",
"大学では、単に知識を暗記するだけでなく、『物事の根本にある原理や論理』を徹底的に突き詰めたい。"

],

"幅広い教養":[

"自分の専門分野だけでなく、歴史、科学、アート、哲学など、全く異なるジャンルの話にも興味が湧く。",
"変化の激しいこれからの時代、一つの知識に偏るよりも、多様な知識を引き出しとして持っている人がカッコいいと思う。",
"大学の授業では、あえて自分の学部とは関係のない未知の分野の講義を受けてみたい。"

],

"主体性":[

"誰かに指示されて動くよりも、自分で『これがやりたい！』と決めて行動する方がモチベーションが上がる。",
"何か問題が起きたとき、誰かが解決してくれるのを待つのではなく、まず自分が動こうとする。",
"大学ではサークル・留学・インターンなど自分発信で挑戦したい。"

],

"発信力":[

"学んだ知識を他人にわかりやすく伝えることに喜びを感じる。",
"議論では自分の意見を積極的に伝えたい。",
"大学ではプレゼンや文章力を身につけたい。"

],

"協働性":[

"一人よりチームで取り組む方が好きだ。",
"意見が対立したときは相手の考えも尊重できる。",
"チーム全体の成果を高める役割を担いたい。"

],

"倫理性":[

"結果だけでなく過程も大切だと思う。",
"科学技術と倫理について考えることは重要だと思う。",
"大学では何が正しいかを深く学びたい。"

],

"創造性":[

"新しいアイデアを考えることが好きだ。",
"『0から1』を生み出すことに魅力を感じる。",
"自分にしかできないものを作ってみたい。"

]

}

labels = {
1:"そう思わない",
2:"ややそう思わない",
3:"どちらでもない",
4:"ややそう思う",
5:"そう思う"
}

scores = {}

st.divider()

question_number = 1

for category, qs in questions.items():

    st.header(category)

    values=[]

    for q in qs:

        value = st.slider(
    f"Q{question_number}. {q}",
    min_value=1,
    max_value=5,
    value=3,
    key=f"q{question_number}"
)

answered += 1

progress = answered / TOTAL_QUESTIONS

progress_bar.progress(progress)

progress_text.write(
    f"回答状況：{answered} / {TOTAL_QUESTIONS}"
)

            format="%d"

        )

        st.caption(labels[value])

        values.append(value)

        question_number += 1

    scores[category]=round(sum(values)/len(values),2)

st.divider()

st.subheader("あなたの能力")

df = pd.DataFrame({

"能力":list(scores.keys()),
"点数":list(scores.values())

})

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.write("### 能力値")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("思考力",scores["思考力"])
    st.metric("主体性",scores["主体性"])
    st.metric("倫理性",scores["倫理性"])

with col2:
    st.metric("幅広い教養",scores["幅広い教養"])
    st.metric("発信力",scores["発信力"])

with col3:
    st.metric("協働性",scores["協働性"])
    st.metric("創造性",scores["創造性"])
  
  TOTAL_QUESTIONS = 21
answered = 0

progress_bar = st.progress(0)
progress_text = st.empty()


departments = {

"経済学科":[105,105,100,18,18,27,27],
"マネジメント学科":[120,102,41,22,24,38,26],
"法律学科":[6,2,125,16,14,68,68],
"法政策学科":[6,2,125,16,14,68,68],
"現代社会学科":[87,23,42,46,40,20,11],
"健康スポーツ社会学科":[72,11,32,37,36,18,19],
"国際関係学科":[53,30,36,21,26,28,22],
"英語学科":[78,18,16,54,27,19,9],
"ヨーロッパ言語学科":[207,30,47,78,32,26,20],
"アジア言語学科":[163,3,66,30,13,10,29],
"京都文化学科":[89,86,50,33,8,24,16],
"国際文化学科":[46,89,29,32,7,24,8],
"数理科学科":[78,6,8,8,4,4,3],
"物理科学科":[75,19,8,3,5,4,3],
"宇宙物理・気象学科":[64,5,10,6,7,2,8],
"情報理工学科":[2,4,11,6,11,8,5],
"産業生命科学科":[12,21,22,18,17,6,11]

}

def normalize(vector):

    maximum = max(vector)

    return [v / maximum for v in vector]

normalized_departments = {}

for name, vector in departments.items():

    normalized_departments[name] = normalize(vector)

with st.expander("学科ベクトル（正規化）"):

    import pandas as pd

    df = pd.DataFrame(
        normalized_departments,
        index=[
            "思考力",
            "幅広い教養",
            "主体性",
            "発信力",
            "協働性",
            "倫理性",
            "創造性"
        ]
    ).T

    st.dataframe(df.round(2))

