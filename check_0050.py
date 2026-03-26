import yfinance as yf
import requests
import sys
import os

def send_telegram_message(message, bot_token, chat_id):
    """發送 Telegram 通知"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ 通知發送成功！")
    else:
        print("❌ 通知發送失敗！", response.text)

def check_0050_open():
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not BOT_TOKEN or not CHAT_ID:
        print("找不到 Token 或 Chat ID，請確認環境變數設定。")
        sys.exit()

    stock = yf.Ticker("0050.TW")
    # 🟢 修正點 1：改成抓取最近 5 天的資料，避免時差問題
    hist = stock.history(period="5d")
    
    if len(hist) < 2:
        print("無法取得足夠的歷史資料。")
        sys.exit()
        
    # 🟢 修正點 2：直接抓取清單中的「倒數第二筆(昨日)」與「最後一筆(今日)」
    yesterday_close = hist['Close'].iloc[-2]
    today_open = hist['Open'].iloc[-1]
    
    drop_pct = (today_open - yesterday_close) / yesterday_close
    
    print(f"📊 昨日收盤: {yesterday_close:.2f}")
    print(f"📊 最新開盤: {today_open:.2f}")
    print(f"📈 漲跌幅: {drop_pct*100:.2f}%")
    
    # 🟢 修正點 3：暫時改成 <= 1 (保證觸發)，用來測試 Telegram 會不會響
    if drop_pct <= 1: 
        msg = f"🔔【0050 監控測試成功】🔔\n最新開盤價: {today_open:.2f}\n昨日收盤價: {yesterday_close:.2f}\n目前漲跌幅: {drop_pct*100:.2f}%"
        send_telegram_message(msg, BOT_TOKEN, CHAT_ID)
    else:
        print("目前跌幅未達標準，不發送通知。")

if __name__ == "__main__":
    check_0050_open()
