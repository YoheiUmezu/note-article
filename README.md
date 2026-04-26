# note-article

Google News RSS からトピックを収集し、`manus_input.md` を毎日自動更新するためのリポジトリです。

## 構成

- `main.py`: RSS を取得して執筆用 Markdown を生成
- `requirements.txt`: Python 依存ライブラリ
- `.github/workflows/daily_update.yml`: 毎日 9:00 (JST) に自動実行する GitHub Actions

## ローカル実行

```bash
pip install -r requirements.txt
python main.py
```

実行後、リポジトリ直下に `manus_input.md` が生成されます。

## 自動実行 (GitHub Actions)

- スケジュール: 毎日 UTC 0:00 (日本時間 9:00)
- 手動実行: Actions 画面の `Daily Content Update` から `Run workflow`
- 更新内容: `manus_input.md` をコミットして `main` に push

## Raw URL

生成された `manus_input.md` は次の URL で参照できます。

- https://raw.githubusercontent.com/YoheiUmezu/note-article/main/manus_input.md
