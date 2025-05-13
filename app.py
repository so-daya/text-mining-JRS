# app.py
import streamlit as st
import os # FONT_PATH_PRIMARY のチェックのため、text_analyzerに移動してもよい

# ページ設定は一番最初に呼び出す
st.set_page_config(layout="wide", page_title="テキストマイニングツール (Streamlit版)")

# --- モジュールのインポート ---
from config import APP_VERSION, SESSION_KEY_MECAB_INIT, TAGGER_OPTIONS
from text_analyzer import initialize_mecab_tagger, setup_japanese_font, perform_morphological_analysis
from ui_components import show_sidebar_options, show_report_tab, show_wordcloud_tab, show_network_tab, show_kwic_tab

# --- MeCab Tagger とフォントの初期化 ---
# Taggerの初期化（キャッシュされる）
tagger = initialize_mecab_tagger()
if tagger:
    st.session_state[SESSION_KEY_MECAB_INIT] = True
else:
    st.session_state[SESSION_KEY_MECAB_INIT] = False

# 日本語フォントの設定（キャッシュされる）
# MeCab初期化後にフォント設定を行う (エラーメッセージがMeCab依存のメッセージより後に出るように)
font_path, font_name = None, None
if st.session_state.get(SESSION_KEY_MECAB_INIT, False):
    font_path, font_name = setup_japanese_font() # font_path_final, font_name_final を受け取る
else:
    # MeCabが初期化できていない場合は、フォント設定を試みない（エラーメッセージが重複しないように）
    if SESSION_KEY_MECAB_INIT not in st.session_state : # 初回実行時などキーが存在しない場合
         st.sidebar.warning("MeCab初期化状態が不明なためフォント設定をスキップします。")
    # else: st.session_state[SESSION_KEY_MECAB_INIT] が False の場合は initialize_mecab_tagger 内でエラー表示済み

# --- Streamlit UI メイン部分 ---
st.title("テキストマイニングツール (Streamlit版)")
st.markdown("日本語テキストを入力して、形態素解析、単語レポート、ワードクラウド、共起ネットワーク、KWIC検索を実行します。")

# サイドバーオプションの表示と取得
analysis_options = show_sidebar_options()

# メインコンテンツエリア
main_text_input = st.text_area(
    "📝 分析したい日本語テキストをここに入力してください:", 
    height=250,
    value="これはStreamlitを使用して作成したテキスト分析ツールです。日本語の形態素解析を行い、単語の出現頻度レポート、ワードクラウド、共起ネットワーク、そしてKWIC（文脈付きキーワード検索）などを試すことができます。様々な文章で分析を実行してみてください。"
)

analyze_button = st.button("分析実行", type="primary", use_container_width=True)

if analyze_button:
    if not main_text_input.strip():
        st.warning("分析するテキストを入力してください。")
    elif not st.session_state.get(SESSION_KEY_MECAB_INIT, False) or tagger is None:
        st.error("MeCab Taggerが利用できません。ページを再読み込みするか、Streamlit Cloudのログを確認してください。")
    else:
        with st.spinner("形態素解析を実行中... しばらくお待ちください。"):
            # Taggerの設定が変わらない限り、perform_morphological_analysisはテキスト入力が同じならキャッシュされた結果を返す
            morphemes = perform_morphological_analysis(main_text_input, TAGGER_OPTIONS) 
        
        if not morphemes:
            st.error("形態素解析に失敗したか、結果が空です。入力テキストを確認してください。")
        else:
            st.success(f"形態素解析が完了しました。総形態素数: {len(morphemes)}")
            st.markdown("---")

            tab_report, tab_wc, tab_network, tab_kwic = st.tabs([
                "📊 単語出現レポート", "☁️ ワードクラウド", "🕸️ 共起ネットワーク", "🔍 KWIC検索"
            ])

            with tab_report:
                show_report_tab(morphemes, 
                                analysis_options["report_pos"], 
                                analysis_options["stop_words"])
            
            with tab_wc:
                show_wordcloud_tab(morphemes, 
                                   font_path, 
                                   analysis_options["wc_pos"], 
                                   analysis_options["stop_words"])
            
            with tab_network:
                show_network_tab(morphemes, main_text_input, TAGGER_OPTIONS, # TAGGER_OPTIONSはキャッシュキー用
                                 font_path, font_name,
                                 analysis_options["net_pos"], 
                                 analysis_options["stop_words"],
                                 analysis_options["node_min_freq"],
                                 analysis_options["edge_min_freq"])

            with tab_kwic:
                show_kwic_tab(morphemes)

# --- フッター情報 ---
st.sidebar.markdown("---")
st.sidebar.info(f"テキストマイニングツール (Streamlit版) v{APP_VERSION}")
