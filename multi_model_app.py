import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="汎用ML予測アプリ",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 汎用機械学習予測アプリ")
st.markdown("複数のプロジェクトのモデルを使って予測ができます")

# サイドバーでプロジェクト選択
st.sidebar.header("📁 プロジェクト選択")

# 利用可能なプロジェクトを検索
projects_dir = Path("../")
available_projects = []

for project_path in projects_dir.iterdir():
    if project_path.is_dir() and (project_path / "models").exists():
        models_dir = project_path / "models"
        pkl_files = list(models_dir.glob("*.pkl"))
        if pkl_files:
            available_projects.append({
                "name": project_path.name,
                "path": project_path,
                "models": pkl_files
            })

if not available_projects:
    st.error("利用可能なプロジェクト/モデルが見つかりません")
    st.info("MLProjectsフォルダ内にmodels/フォルダと.pklファイルがあるプロジェクトを作成してください")
    st.stop()

# プロジェクト選択
project_names = [p["name"] for p in available_projects]
selected_project_name = st.sidebar.selectbox("プロジェクトを選択", project_names)

# 選択されたプロジェクトの情報を取得
selected_project = next(p for p in available_projects if p["name"] == selected_project_name)

# モデル選択
model_names = [m.name for m in selected_project["models"]]
selected_model_name = st.sidebar.selectbox("モデルを選択", model_names)

selected_model_path = selected_project["path"] / "models" / selected_model_name

# モデルを読み込み
@st.cache_resource
def load_model(model_path):
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"モデルの読み込みに失敗しました: {e}")
        return None

model = load_model(selected_model_path)

if model is None:
    st.stop()

st.success(f"✅ プロジェクト: {selected_project_name}")
st.success(f"✅ モデル: {selected_model_name}")

# プロジェクト別の予測設定
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 特徴量入力")
    
    if selected_project_name.lower() == "iris":
        # Iris専用の入力
        st.markdown("**🌸 Iris花の特徴量**")
        sepal_length = st.slider("がく片の長さ (cm)", 4.0, 8.0, 5.5)
        sepal_width = st.slider("がく片の幅 (cm)", 2.0, 4.5, 3.0)
        petal_length = st.slider("花びらの長さ (cm)", 1.0, 7.0, 4.0)
        petal_width = st.slider("花びらの幅 (cm)", 0.1, 2.5, 1.0)
        
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        feature_names = ["がく片の長さ", "がく片の幅", "花びらの長さ", "花びらの幅"]
        values = [sepal_length, sepal_width, petal_length, petal_width]
        
        class_names = ["Setosa", "Versicolor", "Virginica"]
        
    else:
        # 汎用的な入力（他のプロジェクト用）
        st.markdown(f"**⚙️ {selected_project_name}プロジェクトの特徴量**")
        
        # 特徴量の数を推定（仮で4つ）
        num_features = st.number_input("特徴量の数", min_value=1, max_value=20, value=4)
        
        input_values = []
        feature_names = []
        
        for i in range(num_features):
            feature_name = st.text_input(f"特徴量{i+1}の名前", value=f"特徴量{i+1}")
            feature_value = st.number_input(f"{feature_name}の値", value=0.0)
            
            feature_names.append(feature_name)
            input_values.append(feature_value)
        
        input_data = np.array([input_values])
        values = input_values
        class_names = ["クラス0", "クラス1", "クラス2"]  # デフォルト

    # 予測実行
    if st.button("🎯 予測実行", type="primary"):
        try:
            prediction = model.predict(input_data)[0]
            
            # 確率予測（可能な場合）
            if hasattr(model, 'predict_proba'):
                prediction_proba = model.predict_proba(input_data)[0]
                
                with col2:
                    st.subheader("📈 予測結果")
                    
                    if selected_project_name.lower() == "iris":
                        predicted_class = class_names[prediction]
                        st.success(f"予測クラス: **{predicted_class}**")
                    else:
                        st.success(f"予測値: **{prediction}**")
                    
                    # 確率を表示
                    if len(prediction_proba) <= 10:  # クラス数が少ない場合のみ
                        st.markdown("**各クラスの確率:**")
                        for i, prob in enumerate(prediction_proba):
                            class_name = class_names[i] if i < len(class_names) else f"クラス{i}"
                            st.write(f"{class_name}: {prob:.2%}")
                            st.progress(prob)
                        
                        # 確率の可視化
                        fig = px.bar(
                            x=class_names[:len(prediction_proba)],
                            y=prediction_proba,
                            title="クラス別確率",
                            labels={'x': 'クラス', 'y': '確率'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            else:
                with col2:
                    st.subheader("📈 予測結果")
                    st.success(f"予測値: **{prediction}**")
                    
        except Exception as e:
            st.error(f"予測中にエラーが発生しました: {e}")

# 入力データの表示
with st.expander("📋 入力データ詳細"):
    input_df = pd.DataFrame({
        '特徴量': feature_names,
        '値': values
    })
    st.dataframe(input_df, use_container_width=True)

# プロジェクト情報
with st.expander(f"📚 {selected_project_name}プロジェクト情報"):
    st.write(f"**プロジェクトパス:** `{selected_project['path']}`")
    st.write(f"**利用可能なモデル:**")
    for model_file in selected_project["models"]:
        st.write(f"- {model_file.name}")

# フッター
st.markdown("---")
st.markdown("🚀 **汎用ML予測アプリ** - 複数プロジェクトの機械学習モデルを統合管理")