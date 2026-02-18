import streamlit as st
import pandas as pd
from datetime import datetime
import os

# アプリのタイトル
st.set_page_config(page_title="TAT 入金管理アプリ", layout="centered")
st.title("🎸 THINK ABOUT TODAY 管理")

# データの読み込み設定
FILE_NAME = "data.csv"
if not os.path.exists(FILE_NAME):
    # 初期データがない場合、空の表を作成
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
        item = st.text_input("項目名（例：物販売り上げ、Tシャツ製作費）")
        amount = st.number_input("金額 (¥)", min_value=0, step=100)
        
        submitted = st.form_submit_button("保存する")
        if submitted:
            new_data = pd.DataFrame([[date, entry_type, item, amount]], columns=df.columns)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("記録しました！")
            st.rerun()

# --- 計算ロジック ---
total_in = df[df["タイプ"] == "入金"]["金額"].sum()
total_out = df[df["タイプ"] == "出金"]["金額"].sum()
balance = total_in - total_out

# --- 残高表示 ---
st.metric(label="現在の口座残高（概算）", value=f"¥{balance:,}")

# --- 履歴の表示 ---
st.subheader("📊 入出金履歴")
# スプレッドシートのように、最新が上にくるように表示
st.dataframe(df.iloc[::-1], use_container_width=True)