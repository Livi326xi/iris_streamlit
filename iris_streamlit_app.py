import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# ページ設定
st.set_page_config(
    page_title="🌸 アイリス予測アプリ",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 アイリス（あやめ）予測アプリ")
st.markdown("あなたが作った機械学習モデルを使って、花の種類を予測します！")

# 1. モデルを読み込む関数
@st.cache_resource
def load_model():
    """
    保存されたpickleファイルからモデルを読み込みます
    """
    # モデルファイルのパス
    model_path = "../iris/models/model_iris.pkl"
    
    # ファイルが存在するかチェック
    if os.path.exists(model_path):
        try:
            # pickleファイルを開いて読み込み
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            st.success("✅ モデルの読み込みが完了しました！")
            return model
            
        except Exception as e:
            st.error(f"❌ モデルの読み込みでエラーが発生: {e}")
            return None
    else:
        st.error("❌ モデルファイルが見つかりません")
        st.info(f"探しているパス: {model_path}")
        st.info("irisプロジェクトでモデルを学習してから実行してください")
        return None

# 2. モデルを読み込み
st.subheader("🤖 モデル読み込み状況")
model = load_model()

# モデルが読み込めない場合は処理を停止
if model is None:
    st.stop()

# 3. アイリスの種類情報
iris_types = {
    0: "🌼 セトサ (Setosa)",
    1: "🌺 バーシクラー (Versicolor)", 
    2: "🌹 バージニカ (Virginica)"
}

# 4. メインアプリ
st.subheader("📏 花の特徴を入力してください")

# 入力エリアを2つのカラムに分割
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🌿 がく片（Sepal）の測定値**")
    sepal_length = st.slider(
        "がく片の長さ (cm)", 
        min_value=4.0, 
        max_value=8.0, 
        value=5.5, 
        step=0.1,
        help="花を支える緑の部分の長さ"
    )
    
    sepal_width = st.slider(
        "がく片の幅 (cm)", 
        min_value=2.0, 
        max_value=4.5, 
        value=3.0, 
        step=0.1,
        help="がく片の最も幅広い部分"
    )

with col2:
    st.markdown("**🌸 花びら（Petal）の測定値**")
    petal_length = st.slider(
        "花びらの長さ (cm)", 
        min_value=1.0, 
        max_value=7.0, 
        value=4.0, 
        step=0.1,
        help="色のついた花びらの長さ"
    )
    
    petal_width = st.slider(
        "花びらの幅 (cm)", 
        min_value=0.1, 
        max_value=2.5, 
        value=1.0, 
        step=0.1,
        help="花びらの最も幅広い部分"
    )

# 5. 入力データの表示
st.subheader("📋 入力データ")
input_df = pd.DataFrame({
    '特徴量': ['がく片の長さ', 'がく片の幅', '花びらの長さ', '花びらの幅'],
    '値 (cm)': [sepal_length, sepal_width, petal_length, petal_width]
})
st.dataframe(input_df, use_container_width=True)

# 6. 予測実行
st.subheader("🎯 予測結果")

# 予測ボタン
if st.button("🔮 アイリスの種類を予測", type="primary", use_container_width=True):
    try:
        # 入力データを配列に変換（モデルが期待する形式）
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        
        # 予測実行
        prediction = model.predict(input_data)[0]  # [0]で最初の要素を取得
        prediction_proba = model.predict_proba(input_data)[0]  # 各クラスの確率
        
        # 結果表示
        predicted_type = iris_types[prediction]
        confidence = prediction_proba[prediction] * 100
        
        # 大きく結果を表示
        st.success(f"🎉 予測結果: **{predicted_type}**")
        st.info(f"📊 予測信頼度: **{confidence:.1f}%**")
        
        # 各種類の確率を表示
        st.markdown("### 📈 各種類の予測確率")
        
        for i, prob in enumerate(prediction_proba):
            type_name = iris_types[i]
            percentage = prob * 100
            
            # プログレスバーで確率を表示
            st.write(f"{type_name}: {percentage:.1f}%")
            st.progress(prob)
        
        # 最も確率の高い結果をハイライト
        max_prob_idx = np.argmax(prediction_proba)
        if max_prob_idx == prediction:
            st.balloons()  # お祝いアニメーション
            
    except Exception as e:
        st.error(f"❌ 予測中にエラーが発生しました: {e}")

# 7. 使い方の説明
with st.expander("📚 使い方とコツ"):
    st.markdown("""
    ### 🌸 アイリスの特徴
    
    **🌼 セトサ (Setosa)**
    - 小さくて丸い花びら
    - がく片が幅広い
    - 花びらが短い
    
    **🌺 バーシクラー (Versicolor)**
    - 中くらいのサイズ
    - バランスの良い形
    - 中間的な特徴
    
    **🌹 バージニカ (Virginica)**
    - 大きくて細長い花びら
    - 花びらが長い
    - 全体的に大きい
    
    ### 📏 測定のコツ
    - **がく片**: 花を支える緑色の部分
    - **花びら**: 色のついた花の部分  
    - **長さ**: 根元から先端まで
    - **幅**: 最も広い部分
    """)

# 8. フッター
st.markdown("---")
st.markdown("🤖 **あなたが作った機械学習モデル**を使用しています")
st.markdown(f"📁 モデルファイル: `../iris/models/model_iris.pkl`")