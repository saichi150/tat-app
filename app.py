import streamlit as st
import pandas as pd
from datetime import datetime
import os

# アプリのタイトルと設定
st.set_page_config(page_title="TAT 管理アプリ", layout="centered")

# 背景画像のURL（あなたのGitHubから直接読み込む設定です）
bg_image_url = "https://raw.githubusercontent.com/saichi150/tat-app/main/12278.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("{bg_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* タイトルを白く、影をつけて読みやすくする */
    h1 {{
        color: white !important;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
        padding-top: 20px;
    }}
    /* 入力フォームの背景を白くして入力しやすくする */
    .stForm {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
    }}
    /* 残高表示の文字色 */
    .stMetric {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# タイトル（ギター絵文字を削除）
st.title("THINK ABOUT TODAY 管理")

# データの読み込み設定
FILE_NAME = "data.csv"
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["日付", "タイプ", "項目", "金額"])
    df.to_csv(FILE_NAME, index=False)

def load_data():
    return pd.read_csv(FILE_NAME)

df = load_data()

# --- 入力フォーム ---
with st.expander("➕ 新規入力を追加", expanded=True):
    with st.form("input_form", clear_on_submit=True):
        date = st.date_input("日付", datetime.now())
        entry_type = st.radio("タイプ", ["入金", "出金"], horizontal=True)
        item = st.text_input("項目名")
        amount = st.number_input("金額 (¥)", min_value=0, step=100)
        
        submitted = st.form_submit_button("保存する")
        if submitted:
            new_data = pd.DataFrame([[date, entry_type, item, amount]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("記録しました！")
            st.rerun()

# --- 残高計算 ---
total_in = df[df["タイプ"] == "入金"]["金額"].sum()
total_out = df[df["タイプ"] == "出金"]["金額"].sum()
balance = total_in - total_out

st.metric(label="現在の口座残高（概算）", value=f"¥{balance:,}")

# --- 履歴の表示 ---
st.subheader("📊 入出金履歴")
st.dataframe(df.iloc[::-1], use_container_width=True)
