# yfinance 日本株財務情報取得スキル

yfinanceライブラリを使用して日本株（東京証券取引所）の財務情報を取得するClaude.aiスキルです。

## 機能

- 企業の基本情報（企業名、業種、従業員数など）
- 株価情報（現在株価、52週高値・安値、出来高など）
- 企業価値・指標（時価総額、PER、PBR、配当利回りなど）
- 財務健全性（総収益、営業利益率、ROEなど）
- 株価履歴（日次、月次など）
- 財務諸表（損益計算書、貸借対照表、キャッシュフロー計算書）
- 配当情報

## インストール

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. スクリプトの実行権限を付与

```bash
chmod +x japan_stock_info.py
```

## 使用方法

### 基本的な使い方

トヨタ自動車の情報を取得:

```bash
python japan_stock_info.py 7203.T
```

### オプション

```bash
# 基本情報のみ表示
python japan_stock_info.py 7203.T --basic-only

# 株価履歴の期間を指定（1年間）
python japan_stock_info.py 6758.T --history 1y

# すべての財務諸表を表示
python japan_stock_info.py 9984.T --financials all

# 特定の財務諸表のみ表示
python japan_stock_info.py 7974.T --financials balance

# 配当情報を表示しない
python japan_stock_info.py 6861.T --no-dividends
```

### 利用可能なオプション

- `--history`: 株価履歴の期間
  - `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `max`
  - デフォルト: `1mo`

- `--financials`: 取得する財務諸表
  - `income`: 損益計算書
  - `balance`: 貸借対照表
  - `cashflow`: キャッシュフロー計算書
  - `all`: すべて
  - `none`: なし
  - デフォルト: `income`

- `--basic-only`: 基本情報のみ表示

- `--no-dividends`: 配当情報を表示しない

## 主要な日本株ティッカーシンボル

| 企業名 | ティッカー |
|--------|-----------|
| トヨタ自動車 | 7203.T |
| ソニーグループ | 6758.T |
| ソフトバンクグループ | 9984.T |
| 任天堂 | 7974.T |
| キーエンス | 6861.T |
| KDDI | 9433.T |
| 三菱UFJフィナンシャル・グループ | 8306.T |
| 日本電信電話（NTT） | 9432.T |
| ファーストリテイリング | 9983.T |
| リクルートホールディングス | 6098.T |

## 使用例

### 例1: トヨタ自動車の基本情報のみ取得

```bash
python japan_stock_info.py 7203.T --basic-only
```

### 例2: ソニーグループの1年間の株価履歴とすべての財務諸表を取得

```bash
python japan_stock_info.py 6758.T --history 1y --financials all
```

### 例3: 任天堂の貸借対照表のみ取得（配当情報なし）

```bash
python japan_stock_info.py 7974.T --financials balance --no-dividends
```

## 注意事項

1. **ティッカーシンボルの形式**: 日本株の場合、証券コードの後ろに `.T` を付ける必要があります（例: 7203.T）

2. **データの精度**: yfinanceは無料のライブラリであり、データの精度や更新頻度に制限がある場合があります

3. **レート制限**: 大量のリクエストを短時間に送信するとレート制限がかかる可能性があります

4. **通貨**: 日本株の価格は日本円（JPY）で表示されます

5. **財務諸表の言語**: 財務諸表の項目名は英語で表示されます

6. **データの可用性**: すべての銘柄で全ての情報が取得できるとは限りません

## ファイル構成

```
.
├── japan_stock_info.py    # メインスクリプト
├── requirements.txt       # 依存関係
├── README.md             # このファイル
└── .claude/
    └── skills/
        └── claude.md     # スキルドキュメント
```

## ライセンス

このスキルは教育・個人利用目的で作成されています。

## 参考リンク

- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [東京証券取引所](https://www.jpx.co.jp/)
