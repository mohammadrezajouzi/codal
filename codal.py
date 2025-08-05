import requests
from urllib.parse import urlparse, parse_qs

def get_letter_serials(symbol: str):
    url = "https://search.codal.ir/api/search/v2/q"
    params = {
        "Category": "3",
        "Symbol": symbol
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://codal.ir/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        serials = []

        for item in data.get("Letters", []):
            full_url = item.get("Url", "")
            parsed = parse_qs(urlparse(full_url).query)
            letter_serial = parsed.get("LetterSerial", [""])[0]
            serials.append(letter_serial)

        return serials
    else:
        print("خطا در دریافت اطلاعات:", response.status_code)
        return []

# 📥 گرفتن ورودی از کاربر
symbol_input = input("نماد مورد نظر را وارد کنید (مثلاً شستا): ")
letter_serials = get_letter_serials(symbol_input)

# 📤 نمایش خروجی
print("لیست LetterSerial ها:")
for s in letter_serials:
    print(s)
