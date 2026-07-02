import requests
import time

def check_website(url):
    # रिक्वेस्ट में Professional User-Agent डालना बेहतर होता है ताकि साइट बॉट को ब्लॉक न करे
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"🔄 Checking status for: {url}...\n" + "-"*40)
    
    try:
        # 10 सेकंड का टाइमआउट रखा है ताकि अगर साइट स्लो हो तो स्क्रिप्ट अटकी न रहे
        response = requests.get(url, headers=headers, timeout=10)
        
        # 200 OK का मतलब साइट बिल्कुल सही काम कर रही है
        if response.status_code == 200:
            print(f"✅ SUCCESS: Site is UP and Running! (Status: {response.status_code})")
        else:
            print(f"⚠️ WARNING: Site responded with Status Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Unable to connect. Site is completely DOWN or URL is invalid.")
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request Timed Out. Site is taking too long to respond.")
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Something went wrong: {e}")

if __name__ == "__main__":
    # 🎯 यहाँ अपनी साइट का URL डालो (e.g., "https://example.com" या आपकी Vercel/Koyeb की लाइव लिंक)
    TARGET_URL = "https://multi-bot-hosting-platform.vercel.app/" 
    
    check_website(TARGET_URL)
