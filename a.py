import requests
import pandas as pd

def get_codal_letters(symbol: str):
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
        letters = data.get("Letters", [])

        results = []
        for letter in letters:
            results.append({
                "نماد": letter.get("Symbol", ""),
                "نام شرکت": letter.get("CompanyName", ""),
                "عنوان": letter.get("Title", ""),
                "تاریخ انتشار": letter.get("PublishDateTime", ""),
                "کد گزارش": letter.get("LetterCode", ""),
                "PDF": "https://www.codal.ir/" + letter.get("PdfUrl", ""),
                "Excel": letter.get("ExcelUrl", ""),
                "لینک گزارش": "https://www.codal.ir" + letter.get("Url", ""),
                "LetterSerial": extract_letter_serial(letter.get("Url", ""))
            })

        return results
    else:
        print("❌ خطا در دریافت اطلاعات:", response.status_code)
        return []

# 🔍 استخراج مقدار LetterSerial از فیلد Url
from urllib.parse import urlparse, parse_qs

def extract_letter_serial(url):
    parsed = parse_qs(urlparse(url).query)
    return parsed.get("LetterSerial", [""])[0]

# 📥 دریافت ورودی نماد
symbol = input("نماد مورد نظر را وارد کنید (مثلاً شستا): ")
all_data = get_codal_letters(symbol)

# 📤 نمایش خروجی به صورت DataFrame
df = pd.DataFrame(all_data)

# نمایش در کنسول (چند سطر اول)
print("\n🔹 اولین گزارش‌ها:")
print(df.head())

# ✅ ذخیره CSV (اختیاری)
df.to_csv(f"{symbol}_codal_reports.csv", index=False, encoding='utf-8-sig')
print(f"\n✅ فایل {symbol}_codal_reports.csv ذخیره شد.")
