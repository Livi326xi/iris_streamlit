import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="🧪 Streamlit軽量テストアプリ",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Streamlit軽量テストアプリ")
st.markdown("基本的なStreamlit機能を試すためのアプリです")

# サイドバー
st.sidebar.header("📋 機能選択")
feature = st.sidebar.selectbox(
    "試したい機能を選択",
    ["📊 表とグラフ", "🖼️ 画像操作", "🎛️ 入力要素", "📱 レイアウト", "🎨 スタイル"]
)

# ====================
# 📊 表とグラフ
# ====================
if feature == "📊 表とグラフ":
    st.header("📊 表とグラフのテスト")
    
    # サンプルデータ作成
    data = pd.DataFrame({
        '商品': ['商品A', '商品B', '商品C', '商品D', '商品E'],
        '売上': [1200, 800, 1500, 600, 2000],
        '利益': [300, 200, 450, 150, 600],
        '評価': [4.2, 3.8, 4.5, 3.5, 4.8]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 データテーブル")
        st.dataframe(data, use_container_width=True)
        
        st.subheader("📈 メトリクス")
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("総売上", f"¥{data['売上'].sum():,}", "↗️ 前月比+15%")
        with col1_2:
            st.metric("平均評価", f"{data['評価'].mean():.1f}⭐", "↗️ +0.2")
    
    with col2:
        st.subheader("📊 グラフ")
        
        graph_type = st.selectbox("グラフの種類", ["棒グラフ", "折れ線グラフ", "散布図", "円グラフ"])
        
        if graph_type == "棒グラフ":
            fig = px.bar(data, x='商品', y='売上', title="商品別売上")
            st.plotly_chart(fig, use_container_width=True)
        
        elif graph_type == "折れ線グラフ":
            fig = px.line(data, x='商品', y='売上', title="売上推移")
            st.plotly_chart(fig, use_container_width=True)
        
        elif graph_type == "散布図":
            fig = px.scatter(data, x='売上', y='利益', title="売上 vs 利益")
            st.plotly_chart(fig, use_container_width=True)
        
        elif graph_type == "円グラフ":
            fig = px.pie(data, values='売上', names='商品', title="売上構成")
            st.plotly_chart(fig, use_container_width=True)

# ====================
# 🖼️ 画像操作
# ====================
elif feature == "🖼️ 画像操作":
    st.header("🖼️ 画像操作のテスト")
    
    # 画像生成関数
    def create_sample_image():
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # 図形を描画
        draw.rectangle([50, 50, 350, 250], fill='white', outline='black', width=3)
        draw.ellipse([100, 100, 300, 200], fill='yellow', outline='orange', width=2)
        draw.text((180, 140), "Streamlit", fill='black')
        
        return img
    
    # ランダム画像生成
    def create_random_image():
        import random
        
        # ランダムな背景色
        bg_colors = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'lavender']
        bg_color = random.choice(bg_colors)
        
        img = Image.new('RGB', (400, 300), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # ランダムな図形の色
        shape_colors = ['red', 'blue', 'green', 'purple', 'orange', 'pink']
        
        # ランダムな図形を複数描画
        for i in range(random.randint(2, 5)):
            x1 = random.randint(0, 300)
            y1 = random.randint(0, 200)
            x2 = x1 + random.randint(50, 100)
            y2 = y1 + random.randint(50, 100)
            color = random.choice(shape_colors)
            
            shape_type = random.choice(['rectangle', 'ellipse'])
            if shape_type == 'rectangle':
                draw.rectangle([x1, y1, x2, y2], fill=color, outline='black', width=2)
            else:
                draw.ellipse([x1, y1, x2, y2], fill=color, outline='black', width=2)
        
        # ランダムなテキスト
        texts = ['Streamlit', 'Python', 'Random', 'Test', 'Fun!']
        text = random.choice(texts)
        text_x = random.randint(50, 300)
        text_y = random.randint(50, 250)
        draw.text((text_x, text_y), text, fill='black')
        
        return img
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 固定画像生成")
        sample_img = create_sample_image()
        st.image(sample_img, caption="プログラムで生成した画像（固定）")
        
        st.subheader("🎲 ランダム画像生成")
        if st.button("🔄 新しいランダム画像を生成", key="random_img"):
            st.session_state.random_image = create_random_image()
        
        # セッションステートで画像を保持
        if 'random_image' not in st.session_state:
            st.session_state.random_image = create_random_image()
        
        st.image(st.session_state.random_image, caption="ランダム生成画像")
        
        if st.button("🎨 アート風ランダム画像", key="art_img"):
            # より芸術的なランダム画像
            import random
            img = Image.new('RGB', (400, 300), color='black')
            draw = ImageDraw.Draw(img)
            
            # ランダムな線を描画
            for _ in range(20):
                x1, y1 = random.randint(0, 400), random.randint(0, 300)
                x2, y2 = random.randint(0, 400), random.randint(0, 300)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                draw.line([x1, y1, x2, y2], fill=color, width=random.randint(1, 5))
            
            st.session_state.art_image = img
        
        if 'art_image' in st.session_state:
            st.image(st.session_state.art_image, caption="アート風ランダム画像")
    
    with col2:
        st.subheader("📸 画像アップロード")
        uploaded_file = st.file_uploader("画像をアップロード", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="アップロードされた画像")
            
            # 画像情報
            st.write(f"**サイズ**: {image.size}")
            st.write(f"**モード**: {image.mode}")
            
            # 画像の統計情報
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                st.write(f"**平均色 (RGB)**: {img_array.mean(axis=(0,1)).astype(int)}")
        
        st.subheader("🎨 画像生成のコツ")
        with st.expander("画像生成について"):
            st.markdown("""
            **固定画像**: 毎回同じ画像を生成
            - デザインが決まっている場合に使用
            - ロゴやアイコンなど
            
            **ランダム画像**: ボタンを押すたびに変化
            - テスト用データの生成
            - 動的なコンテンツ作成
            
            **アート風**: より複雑なランダム生成
            - 芸術的な表現
            - データビジュアライゼーション
            """)

# ====================
# 🎛️ 入力要素
# ====================
elif feature == "🎛️ 入力要素":
    st.header("🎛️ 入力要素のテスト")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 基本入力")
        
        name = st.text_input("お名前", "山田太郎")
        age = st.number_input("年齢", min_value=0, max_value=120, value=25)
        score = st.slider("スコア", 0, 100, 75)
        birthday = st.date_input("誕生日", datetime(1990, 1, 1).date())
        
        st.subheader("☑️ 選択入力")
        agree = st.checkbox("利用規約に同意する")
        gender = st.radio("性別", ["男性", "女性", "その他"])
        hobby = st.selectbox("趣味", ["読書", "映画", "スポーツ", "音楽", "旅行"])
        skills = st.multiselect("スキル", ["Python", "JavaScript", "SQL", "Excel", "PowerPoint"])
    
    with col2:
        st.subheader("📊 入力結果")
        
        if st.button("結果を表示"):
            st.write("### 入力内容")
            st.write(f"**名前**: {name}")
            st.write(f"**年齢**: {age}歳")
            st.write(f"**スコア**: {score}点")
            st.write(f"**誕生日**: {birthday}")
            st.write(f"**同意**: {'はい' if agree else 'いいえ'}")
            st.write(f"**性別**: {gender}")
            st.write(f"**趣味**: {hobby}")
            st.write(f"**スキル**: {', '.join(skills) if skills else 'なし'}")
            
            # 結果をJSON形式で表示
            result_data = {
                "name": name,
                "age": age,
                "score": score,
                "birthday": str(birthday),
                "agree": agree,
                "gender": gender,
                "hobby": hobby,
                "skills": skills
            }
            st.json(result_data)

# ====================
# 📱 レイアウト
# ====================
elif feature == "📱 レイアウト":
    st.header("📱 レイアウトのテスト")
    
    st.subheader("📄 タブレイアウト")
    tab1, tab2, tab3 = st.tabs(["データ", "グラフ", "設定"])
    
    with tab1:
        st.write("**データタブの内容**")
        sample_data = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
        st.dataframe(sample_data)
    
    with tab2:
        st.write("**グラフタブの内容**")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
        st.line_chart(chart_data)
    
    with tab3:
        st.write("**設定タブの内容**")
        st.selectbox("テーマ", ["ライト", "ダーク"])
        st.slider("表示件数", 5, 50, 10)
    
    st.subheader("📦 カラムレイアウト")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.info("幅2のカラム")
        st.bar_chart(np.random.randn(10, 1))
    
    with col2:
        st.success("幅1のカラム")
        st.metric("値1", "123", "5%")
    
    with col3:
        st.warning("幅1のカラム")
        st.metric("値2", "456", "-2%")
    
    st.subheader("📋 展開セクション")
    with st.expander("詳細情報を表示"):
        st.write("これは展開可能なセクションです。")
        st.code("print('Hello, World!')")

# ====================
# 🎨 スタイル
# ====================
elif feature == "🎨 スタイル":
    st.header("🎨 スタイルのテスト")
    
    st.subheader("💬 メッセージボックス")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ 成功メッセージ")
        st.info("ℹ️ 情報メッセージ")
    
    with col2:
        st.warning("⚠️ 警告メッセージ")
        st.error("❌ エラーメッセージ")
    
    st.subheader("💻 コード表示")
    code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price']
    return total
    '''
    st.code(code, language='python')
    
    st.subheader("🎮 インタラクティブ要素")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎈 お祝い"):
            st.balloons()
        
        if st.button("❄️ 雪を降らせる"):
            st.snow()
    
    with col2:
        progress_value = st.slider("プログレス", 0, 100, 50)
        st.progress(progress_value / 100)
    
    st.subheader("📊 ステータス")
    status = st.selectbox("ステータス選択", ["準備中", "進行中", "完了", "エラー"])
    
    if status == "準備中":
        st.info(f"現在のステータス: {status}")
    elif status == "進行中":
        st.warning(f"現在のステータス: {status}")
    elif status == "完了":
        st.success(f"現在のステータス: {status}")
    else:
        st.error(f"現在のステータス: {status}")

# フッター
st.markdown("---")
st.markdown("🧪 **Streamlit軽量テストアプリ** - 基本機能のテスト用")