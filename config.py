# config.py
import os

# --- MeCab関連定数 ---
MECABRC_PATH = "/etc/mecabrc"
DICTIONARY_PATH = "/var/lib/mecab/dic/ipadic-utf8"
TAGGER_OPTIONS = f"-r {MECABRC_PATH} -d {DICTIONARY_PATH}"

# --- フォント関連定数 ---
# Streamlit Cloud環境に合わせてIPAフォントのパスを指定
FONT_PATH_PRIMARY = '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'
# FONT_PATH_PRIMARY = 'ipaexg.ttf' # ローカルで試す場合やフォント名で指定したい場合

# --- デフォルト設定 ---
DEFAULT_TARGET_POS = ['名詞', '動詞', '形容詞']
DEFAULT_STOP_WORDS_SET = set() # デフォルトは空のセット

# --- 共起ネットワークPyvisオプション ---
PYVIS_OPTIONS_STR = """
var options = {
  "interaction": {
    "navigationButtons": false,
    "keyboard": {
      "enabled": false
    }
  },
  "manipulation": {
    "enabled": false
  },
  "configure": {
    "enabled": false
  },
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -30000,
      "centralGravity": 0.1,
      "springLength": 150,
      "springConstant": 0.03,
      "damping": 0.09,
      "avoidOverlap": 0.5
    },
    "solver": "barnesHut",
    "stabilization": {
      "iterations": 500
    }
  }
};
"""

# --- Streamlit Session State Keys ---
# (オプション) 必要に応じてセッションステートのキーも定数化
SESSION_KEY_MECAB_INIT = 'mecab_tagger_initialized'
SESSION_KEY_KWIC_KEYWORD = 'kwic_keyword'
SESSION_KEY_KWIC_MODE_IDX = 'kwic_mode_idx'
SESSION_KEY_KWIC_WINDOW_VAL = 'kwic_window_val'
SESSION_KEY_ANALYZED_MORPHS = 'analyzed_morphemes' # 解析結果をセッションに保持する場合

# --- アプリケーション情報 ---
APP_VERSION = "0.3.1" # バージョン更新
