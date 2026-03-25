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
    # 🟢 從 GitHub Secrets 讀取變數，這樣最安全！
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not BOT_TOKEN or not CHAT_ID:
        print("找不到 Token 或 Chat ID，請確認環境變數設定。")
        sys.exit()

    stock = yf.Ticker("0050.TW")
    hist = stock.history(period="2d")
    
    if len(hist) < 2:
        print("無法取得足夠的歷史資料。")
        sys.exit()
        
    yesterday_close = hist['Close'].iloc[0]
    today_open = hist['Open'].iloc[1]
    drop_pct = (today_open - yesterday_close) / yesterday_close
    
    print(f"📊 昨日收盤: {yesterday_close:.2f}")
    print(f"📊 今日開盤: {today_open:.2f}")
    print(f"📈 漲跌幅: {drop_pct*100:.2f}%")
    
    # 測試期間可以改成 <= 1，確認通知會通後，再改成 <= -0.05
    if drop_pct <= -0.05: 
        msg = f"⚠️【0050 暴跌通知】⚠️\n今日開盤價: {today_open:.2f}\n昨日收盤價: {yesterday_close:.2f}\n目前跌幅達: {drop_pct*100:.2f}%！\n請注意市場風險。"
        send_telegram_message(msg, BOT_TOKEN, CHAT_ID)
    else:
        print("目前跌幅未達標準，不發送通知。")

if __name__ == "__main__":
    check_0050_open()
