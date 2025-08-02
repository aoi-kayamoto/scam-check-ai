import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="詐欺案件チェックAI", page_icon="🕵️‍♀️")
st.title("🕵️‍♀️ 詐欺案件チェックAI")
st.write("タイトル・内容・あなたの考えを入力すると、AIが応募OKか判定します。")

title = st.text_input("🔹案件タイトル")
body = st.text_area("🔹案件の内容（コピペ）")
user_opinion = st.text_area("🔹あなたの考え・不安な点（空欄だと判定できません）")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("AIで判定する"):
    if not user_opinion.strip():
        st.warning("⚠️ 自分の考えを入力してください。判断力を育てるために必要です。")
    else:
        with st.spinner("AIがチェック中..."):
            prompt = f"""
あなたは詐欺案件の分析を得意とするAIアシスタントです。
以下の情報を元に、応募しても問題ないかどうかを冷静に判断してください。

【案件タイトル】
{title}

【案件の内容】
{body}

【応募者の考え・不安】
{user_opinion}

▼出力形式：
1. 判定（詐欺の可能性：高・中・低 のいずれか）
2. 理由（怪しい点 or 安心材料を3つまで）
3. アドバイス（迷っている人への一言。優しく・簡潔に）
4. 応募者の考えに対するフィードバック（前向きで寄り添う言葉で、判断力を肯定しつつ必要があれば補足）
"""

            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            st.markdown("### ✅ 判定結果")
            st.write(response.choices[0].message.content)
