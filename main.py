import feedparser
import datetime
import json
import os
from urllib.parse import quote_plus

# --- 設定 ---
# 取得したいキーワード
KEYWORDS = ["従業員エンゲージメント", "EX 向上", "社外広報 成功事例", "DX 組織文化"]
# Manusに読み込ませるファイル名
OUTPUT_FILE = "manus_input.md"
STATE_FILE = "used_links.json"
PICKS_PER_KEYWORD = 2
MAX_USED_LINKS = 200


def load_used_links():
    """過去に使用した記事URLを読み込む"""
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return set(data)
    except (json.JSONDecodeError, OSError):
        pass
    return set()


def save_used_links(links):
    """使用済みURLを保存する（無制限増加を避ける）"""
    trimmed = list(links)[-MAX_USED_LINKS:]
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(trimmed, f, ensure_ascii=False, indent=2)

def get_latest_trends():
    """Google News RSSからキーワードに関連する最新記事を取得（重複回避）"""
    used_links = load_used_links()
    combined_entries = []
    seen_in_run = set()

    for kw in KEYWORDS:
        encoded_kw = quote_plus(kw)
        rss_url = f"https://news.google.com/rss/search?q={encoded_kw}&hl=ja&gl=JP&ceid=JP:ja"
        feed = feedparser.parse(rss_url)

        fresh_entries = []
        fallback_entries = []
        for entry in feed.entries:
            link = entry.link
            if link in seen_in_run:
                continue
            if link in used_links:
                fallback_entries.append(entry)
            else:
                fresh_entries.append(entry)

        selected = fresh_entries[:PICKS_PER_KEYWORD]
        if len(selected) < PICKS_PER_KEYWORD:
            selected.extend(fallback_entries[: PICKS_PER_KEYWORD - len(selected)])

        for entry in selected:
            combined_entries.append(entry)
            seen_in_run.add(entry.link)

    save_used_links(used_links.union(seen_in_run))
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

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Success: {OUTPUT_FILE} has been updated.")

if __name__ == "__main__":
    generate_instruction()
