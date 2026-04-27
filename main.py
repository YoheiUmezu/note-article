import feedparser
import datetime
from urllib.parse import quote_plus

# --- 設定 ---
# 取得したいキーワード
KEYWORDS = ["従業員エンゲージメント", "EX 向上", "社外広報 成功事例", "DX 組織文化"]
# Manusに読み込ませるファイル名
OUTPUT_FILE = "manus_input.md"

def get_latest_trends():
    """Google News RSSからキーワードに関連する最新記事を取得"""
    combined_entries = []
    for kw in KEYWORDS:
        encoded_kw = quote_plus(kw)
        rss_url = f"https://news.google.com/rss/search?q={encoded_kw}&hl=ja&gl=JP&ceid=JP:ja"
        feed = feedparser.parse(rss_url)
        # 各キーワードから上位2件をピックアップ
        combined_entries.extend(feed.entries[:2])
    return combined_entries

def generate_instruction():
    """Manus向けの指示書を作成"""
    entries = get_latest_trends()
    jst = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(jst)
    
    # 曜日ごとの切り口
    themes = ["経営戦略", "現場の運用課題", "システム連携", "RFP/選定基準", "トレンド解説", "キャリア", "海外事例"]
    today_theme = themes[now.weekday()]

    md_content = f"# 本日の執筆テーマ: {today_theme}\n\n"
    md_content += f"- 生成日時 (JST): {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md_content += "## 収集された最新トピック\n"
    for entry in entries:
        md_content += f"- タイトル: {entry.title}\n"
        md_content += f"  URL: {entry.link}\n\n"
    
    md_content += "\n# Manusへの追加指示\n"
    md_content += "上記のトピックから1つ以上を引用し、日本のEX/従業員エンゲージメント業界を盛り上げる記事を書いてください。\n"
    md_content += "SEとしての「現場のリアル」と「ウィット」の注入- 各記事の締めくくりに、**【SEの独り言：現場の解像度】**というセクションを必ず設けてください。ここでは、AIが書いたような教科書的な結論ではなく、以下のトーンで「現場の生々しい本音」を2〜3行で表現してください。-視点: 30代の現役シニアSE。外資の合理性と日本の商習慣の板挟みを楽しんでいる。-トーン:冷静だが少し皮肉（witty）が含まれている。-ポイント:「制度」や「ツール」ではなく、「人の感情や組織の力学」にフォーカスする。"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Success: {OUTPUT_FILE} has been updated.")

if __name__ == "__main__":
    generate_instruction()
