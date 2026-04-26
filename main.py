import feedparser
import datetime

# --- 設定 ---
# 取得したいキーワード
KEYWORDS = ["従業員エンゲージメント", "EX 向上", "社外広報 成功事例", "DX 組織文化"]
# Manusに読み込ませるファイル名
OUTPUT_FILE = "manus_input.md"

def get_latest_trends():
    """Google News RSSからキーワードに関連する最新記事を取得"""
    combined_entries = []
    for kw in KEYWORDS:
        rss_url = f"https://news.google.com/rss/search?q={kw}&hl=ja&gl=JP&ceid=JP:ja"
        feed = feedparser.parse(rss_url)
        # 各キーワードから上位2件をピックアップ
        combined_entries.extend(feed.entries[:2])
    return combined_entries

def generate_instruction():
    """Manus向けの指示書を作成"""
    entries = get_latest_trends()
    now = datetime.datetime.now()
    
    # 曜日ごとの切り口
    themes = ["経営戦略", "現場の運用課題", "システム連携", "RFP/選定基準", "トレンド解説", "キャリア", "海外事例"]
    today_theme = themes[now.weekday()]

    md_content = f"# 本日の執筆テーマ: {today_theme}\n\n"
    md_content += "## 収集された最新トピック\n"
    for entry in entries:
        md_content += f"- タイトル: {entry.title}\n"
        md_content += f"  URL: {entry.link}\n\n"
    
    md_content += "\n# Manusへの追加指示\n"
    md_content += "上記のトピックから1つ以上を引用し、日本のEX/従業員エンゲージメント業界を盛り上げる記事を書いてください。\n"
    md_content += "セールスエンジニアの視点で、現場の泥臭い課題（稟議の通りにくさ、ITリテラシーの壁など）を具体的に含めてください。"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Success: {OUTPUT_FILE} has been updated.")

if __name__ == "__main__":
    generate_instruction()
