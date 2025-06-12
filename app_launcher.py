import streamlit as st
import subprocess
import os
from pathlib import Path

st.set_page_config(
    page_title="🚀 MLアプリランチャー",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 機械学習アプリランチャー")
st.markdown("作成したアプリを選択して起動できます")

# 利用可能なアプリを検索
apps = []
app_files = Path(".").glob("*.py")

for app_file in app_files:
    if app_file.name != "app_launcher.py":  # 自分自身は除外
        apps.append({
            "name": app_file.stem,
            "file": app_file.name,
            "description": f"{app_file.stem}アプリ"
        })

# アプリの説明を追加
app_descriptions = {
    "multi_model_app": "🤖 汎用機械学習予測アプリ - 複数プロジェクトに対応",
    "iris_image_classifier": "🌸 あやめ画像分類アプリ - 写真から自動分類",
    "iris_model_training": "📚 Irisモデル学習スクリプト - モデルを作成"
}

st.subheader("📋 利用可能なアプリ一覧")

col1, col2, col3 = st.columns(3)

for i, app in enumerate(apps):
    col = [col1, col2, col3][i % 3]
    
    with col:
        with st.container():
            st.markdown(f"### {app['name']}")
            description = app_descriptions.get(app['name'], app['description'])
            st.markdown(description)
            
            # 起動ボタン
            if st.button(f"🚀 起動", key=f"launch_{app['name']}"):
                st.info(f"'{app['name']}'を起動しています...")
                st.markdown(f"**コマンド**: `streamlit run {app['file']}`")
                st.markdown("ターミナルで上記コマンドを実行してください")

st.markdown("---")

# 新しいアプリの作成ガイド
st.subheader("✨ 新しいアプリを作成")

with st.expander("📝 新しいアプリ作成の手順"):
    st.markdown("""
    ### 1. 新しいPythonファイルを作成
    ```bash
    code new_app_name.py
    ```
    
    ### 2. 基本テンプレート
    ```python
    import streamlit as st
    
    st.title("新しいアプリ")
    st.write("ここにアプリの内容を書く")
    ```
    
    ### 3. アプリを起動
    ```bash
    streamlit run new_app_name.py --server.port 8502
    ```
    
    ### 4. ポート番号の使い分け
    - 8501: メインアプリ
    - 8502, 8503, 8504...: 追加のアプリ
    """)

# 現在実行中のアプリ情報
st.subheader("🔍 実行中のアプリ確認")
st.markdown("""
**現在実行中のアプリを確認する方法:**
- ブラウザのタブをチェック
- `http://localhost:8501`, `http://localhost:8502` などにアクセス

**アプリを停止する方法:**
- ターミナルで `Ctrl + C`
""")

# アプリ管理のコツ
st.subheader("💡 アプリ管理のコツ")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📁 ファイル整理**
    - 機能別にファイル名を付ける
    - コメントでアプリの説明を書く
    - READMEファイルを作成
    """)

with col2:
    st.markdown("""
    **🖥️ 実行管理**
    - ポート番号を記録しておく
    - 複数アプリを同時実行
    - 不要なアプリは停止
    """)

st.markdown("---")
st.markdown("🚀 **MLアプリランチャー** - 作成したアプリを効率的に管理")