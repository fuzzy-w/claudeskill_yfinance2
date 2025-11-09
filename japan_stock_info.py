#!/usr/bin/env python3
"""
yfinance日本株財務情報取得スキル

日本株（東京証券取引所）の財務情報を取得するスクリプト
"""

import sys
import argparse
from datetime import datetime
import yfinance as yf
import pandas as pd


def format_large_number(num):
    """大きな数値を読みやすくフォーマット"""
    if num is None or pd.isna(num):
        return "N/A"

    if abs(num) >= 1_000_000_000_000:  # 兆
        return f"{num / 1_000_000_000_000:.2f}兆"
    elif abs(num) >= 100_000_000:  # 億
        return f"{num / 100_000_000:.2f}億"
    elif abs(num) >= 10_000:  # 万
        return f"{num / 10_000:.2f}万"
    else:
        return f"{num:,.0f}"


def get_company_info(ticker_symbol):
    """企業の基本情報を取得"""
    print(f"\n{'='*80}")
    print(f"日本株情報取得: {ticker_symbol}")
    print(f"{'='*80}\n")

    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        # 基本情報
        print("【企業基本情報】")
        print(f"企業名: {info.get('longName', 'N/A')}")
        print(f"業種: {info.get('sector', 'N/A')}")
        print(f"産業: {info.get('industry', 'N/A')}")
        print(f"ウェブサイト: {info.get('website', 'N/A')}")
        print(f"従業員数: {info.get('fullTimeEmployees', 'N/A'):,}" if info.get('fullTimeEmployees') else "従業員数: N/A")

        # 株価情報
        print(f"\n【株価情報】")
        print(f"現在株価: {info.get('currentPrice', 'N/A')}円")
        print(f"前日終値: {info.get('previousClose', 'N/A')}円")
        print(f"始値: {info.get('open', 'N/A')}円")
        print(f"日中高値: {info.get('dayHigh', 'N/A')}円")
        print(f"日中安値: {info.get('dayLow', 'N/A')}円")
        print(f"52週高値: {info.get('fiftyTwoWeekHigh', 'N/A')}円")
        print(f"52週安値: {info.get('fiftyTwoWeekLow', 'N/A')}円")
        print(f"出来高: {format_large_number(info.get('volume'))}")
        print(f"平均出来高: {format_large_number(info.get('averageVolume'))}")

        # 時価総額と指標
        print(f"\n【企業価値・指標】")
        print(f"時価総額: {format_large_number(info.get('marketCap'))}円")
        print(f"PER (株価収益率): {info.get('trailingPE', 'N/A')}")
        print(f"PBR (株価純資産倍率): {info.get('priceToBook', 'N/A')}")
        print(f"配当利回り: {info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "配当利回り: N/A")
        print(f"ベータ値: {info.get('beta', 'N/A')}")

        # 財務健全性
        print(f"\n【財務健全性】")
        print(f"総収益: {format_large_number(info.get('totalRevenue'))}円")
        print(f"営業利益率: {info.get('operatingMargins', 0) * 100:.2f}%" if info.get('operatingMargins') else "営業利益率: N/A")
        print(f"利益率: {info.get('profitMargins', 0) * 100:.2f}%" if info.get('profitMargins') else "利益率: N/A")
        print(f"ROE (自己資本利益率): {info.get('returnOnEquity', 0) * 100:.2f}%" if info.get('returnOnEquity') else "ROE: N/A")
        print(f"総負債: {format_large_number(info.get('totalDebt'))}円")
        print(f"総資産: {format_large_number(info.get('totalAssets'))}円")

        return stock

    except Exception as e:
        print(f"エラー: 企業情報の取得に失敗しました - {str(e)}")
        return None


def get_stock_history(stock, period="1mo"):
    """株価履歴を取得"""
    print(f"\n【株価履歴（{period}）】")

    try:
        hist = stock.history(period=period)

        if hist.empty:
            print("株価データが取得できませんでした")
            return

        print(f"\n直近5日間:")
        print(hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail().to_string())

        print(f"\n統計情報:")
        print(f"期間最高値: {hist['High'].max():.2f}円")
        print(f"期間最安値: {hist['Low'].min():.2f}円")
        print(f"平均終値: {hist['Close'].mean():.2f}円")
        print(f"平均出来高: {format_large_number(hist['Volume'].mean())}")

    except Exception as e:
        print(f"エラー: 株価履歴の取得に失敗しました - {str(e)}")


def get_financials(stock, statement_type="income"):
    """財務諸表を取得"""
    try:
        if statement_type == "income":
            print(f"\n【損益計算書（年次）】")
            financials = stock.financials
        elif statement_type == "balance":
            print(f"\n【貸借対照表（年次）】")
            financials = stock.balance_sheet
        elif statement_type == "cashflow":
            print(f"\n【キャッシュフロー計算書（年次）】")
            financials = stock.cashflow
        else:
            print(f"不明な財務諸表タイプ: {statement_type}")
            return

        if financials.empty:
            print("財務データが取得できませんでした")
            return

        # 最新の列（最新の財務データ）を取得
        print(f"\n直近の財務データ:")
        print(financials.iloc[:, 0].head(15).to_string())

    except Exception as e:
        print(f"エラー: 財務諸表の取得に失敗しました - {str(e)}")


def get_dividends(stock):
    """配当情報を取得"""
    print(f"\n【配当情報】")

    try:
        dividends = stock.dividends

        if dividends.empty:
            print("配当データが取得できませんでした")
            return

        print(f"\n直近10回の配当:")
        recent_dividends = dividends.tail(10)
        for date, amount in recent_dividends.items():
            print(f"{date.strftime('%Y-%m-%d')}: {amount:.2f}円")

        print(f"\n配当統計:")
        print(f"最新配当: {dividends.iloc[-1]:.2f}円")
        print(f"平均配当: {dividends.mean():.2f}円")
        print(f"配当回数: {len(dividends)}回")

    except Exception as e:
        print(f"エラー: 配当情報の取得に失敗しました - {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='yfinanceを使って日本株の財務情報を取得',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # トヨタ自動車の情報を取得
  python japan_stock_info.py 7203.T

  # ソニーグループの詳細情報を取得
  python japan_stock_info.py 6758.T --history 1y --financials all

  # 任天堂の基本情報のみ取得
  python japan_stock_info.py 7974.T --basic-only

主要な日本株ティッカーシンボル:
  7203.T - トヨタ自動車
  6758.T - ソニーグループ
  9984.T - ソフトバンクグループ
  7974.T - 任天堂
  6861.T - キーエンス
  9433.T - KDDI
  8306.T - 三菱UFJフィナンシャル・グループ
        """
    )

    parser.add_argument(
        'ticker',
        help='日本株のティッカーシンボル（例: 7203.T）'
    )

    parser.add_argument(
        '--history',
        default='1mo',
        choices=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'],
        help='株価履歴の期間（デフォルト: 1mo）'
    )

    parser.add_argument(
        '--financials',
        default='income',
        choices=['income', 'balance', 'cashflow', 'all', 'none'],
        help='取得する財務諸表（デフォルト: income）'
    )

    parser.add_argument(
        '--basic-only',
        action='store_true',
        help='基本情報のみ表示'
    )

    parser.add_argument(
        '--no-dividends',
        action='store_true',
        help='配当情報を表示しない'
    )

    args = parser.parse_args()

    # 企業基本情報を取得
    stock = get_company_info(args.ticker)

    if stock is None:
        sys.exit(1)

    # 基本情報のみの場合はここで終了
    if args.basic_only:
        print(f"\n{'='*80}\n")
        return

    # 株価履歴を取得
    get_stock_history(stock, args.history)

    # 財務諸表を取得
    if args.financials != 'none':
        if args.financials == 'all':
            get_financials(stock, 'income')
            get_financials(stock, 'balance')
            get_financials(stock, 'cashflow')
        else:
            get_financials(stock, args.financials)

    # 配当情報を取得
    if not args.no_dividends:
        get_dividends(stock)

    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
