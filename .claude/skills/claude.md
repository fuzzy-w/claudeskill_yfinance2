# yfinance 日本株財務情報取得スキル

このスキルは、yfinanceライブラリを使用して日本株の財務情報を取得し、分析するためのものです。

## 概要

- **目的**: 日本株の株価、財務諸表、企業情報などを取得する
- **使用ライブラリ**: yfinance
- **対象市場**: 東京証券取引所（Tokyo Stock Exchange）

## 日本株のティッカーシンボル形式

日本株のティッカーシンボルは、証券コードの後ろに `.T` を付けます。

例:
- トヨタ自動車: `7203.T`
- ソニーグループ: `6758.T`
- ソフトバンクグループ: `9984.T`
- 任天堂: `7974.T`
- キーエンス: `6861.T`

## 取得可能な情報

### 1. 基本情報
- 企業名
- 業種
- 従業員数
- ウェブサイト
- 企業概要

### 2. 株価情報
- 現在株価
- 過去の株価データ（日次、週次、月次）
- 出来高
- 時価総額

### 3. 財務情報
- 損益計算書（Income Statement）
- 貸借対照表（Balance Sheet）
- キャッシュフロー計算書（Cash Flow Statement）
- 財務指標（PER、PBR、配当利回りなど）

### 4. 配当情報
- 配当履歴
- 配当利回り

## 実装例

### 必要なライブラリのインストール

```bash
pip install yfinance pandas
```

### 基本的な使用例

```python
import yfinance as yf
import pandas as pd

# 日本株のティッカーシンボルを指定
ticker_symbol = "7203.T"  # トヨタ自動車

# Tickerオブジェクトを作成
stock = yf.Ticker(ticker_symbol)

# 1. 基本情報を取得
info = stock.info
print(f"企業名: {info.get('longName', 'N/A')}")
print(f"業種: {info.get('sector', 'N/A')}")
print(f"現在株価: {info.get('currentPrice', 'N/A')}円")
print(f"時価総額: {info.get('marketCap', 'N/A')}円")

# 2. 過去の株価データを取得（過去1年間）
hist = stock.history(period="1y")
print("\n過去1年間の株価データ:")
print(hist.head())

# 3. 財務諸表を取得
# 損益計算書
income_stmt = stock.financials
print("\n損益計算書:")
print(income_stmt)

# 貸借対照表
balance_sheet = stock.balance_sheet
print("\n貸借対照表:")
print(balance_sheet)

# キャッシュフロー計算書
cash_flow = stock.cashflow
print("\nキャッシュフロー計算書:")
print(cash_flow)

# 4. 配当情報を取得
dividends = stock.dividends
print("\n配当履歴:")
print(dividends.tail(10))
```

## 主要な関数とメソッド

### yf.Ticker(ticker_symbol)
指定したティッカーシンボルの株式オブジェクトを作成

### stock.info
企業の基本情報を辞書形式で取得

### stock.history(period, interval)
過去の株価データを取得
- period: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
- interval: "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"

### stock.financials
損益計算書を取得（年次）

### stock.quarterly_financials
損益計算書を取得（四半期）

### stock.balance_sheet
貸借対照表を取得（年次）

### stock.quarterly_balance_sheet
貸借対照表を取得（四半期）

### stock.cashflow
キャッシュフロー計算書を取得（年次）

### stock.quarterly_cashflow
キャッシュフロー計算書を取得（四半期）

### stock.dividends
配当履歴を取得

### stock.actions
配当と株式分割の履歴を取得

## 注意事項

1. **データの精度**: yfinanceは無料のライブラリであり、データの精度や更新頻度に制限がある場合があります
2. **レート制限**: 大量のリクエストを短時間に送信するとレート制限がかかる可能性があります
3. **通貨**: 日本株の場合、価格は日本円（JPY）で表示されます
4. **財務諸表の言語**: 財務諸表の項目名は英語で表示されます
5. **データの可用性**: すべての銘柄で全ての情報が取得できるとは限りません

## 活用シーン

- 個別株の財務分析
- 複数銘柄の比較分析
- 株価トレンドの可視化
- ポートフォリオ管理
- 投資判断のための情報収集

## 参考リンク

- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [東京証券取引所](https://www.jpx.co.jp/)
