from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
import requests
from urllib.parse import urlparse, parse_qs, quote

app = FastAPI()

# فعال‌سازی CORS برای استفاده از Google Sheets یا هر کلاینت دیگر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# دریافت داده‌های کدال و ساخت جدول
def get_codal_letters(symbol: str):
    url = "https://search.codal.ir/api/search/v2/q"
    params = {
        "Category": "3",
        "Symbol": symbol
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://codal.ir/",
        "user-agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return pd.DataFrame()  # اگر خطا رخ دهد، جدول خالی برگردان

    data = response.json()
    letters = data.get("Letters", [])

    results = []
    for letter in letters:
        parsed = parse_qs(urlparse(letter.get("Url", "")).query)
        results.append({
            "نماد": letter.get("Symbol", ""),
            "نام شرکت": letter.get("CompanyName", ""),
            "عنوان": letter.get("Title", ""),
            "تاریخ انتشار": letter.get("PublishDateTime", ""),
            "کد گزارش": letter.get("LetterCode", ""),
            "PDF": "https://www.codal.ir/" + letter.get("PdfUrl", ""),
            "Excel": letter.get("ExcelUrl", ""),
            "لینک گزارش": "https://www.codal.ir" + letter.get("Url", ""),
            "LetterSerial": parsed.get("LetterSerial", [""])[0]
        })

    return pd.DataFrame(results)


# خروجی CSV قابل دانلود
@app.get("/csv/{symbol}")
def download_csv(symbol: str):
    df = get_codal_letters(symbol)
    if df.empty:
        return Response(content="هیچ گزارشی پیدا نشد", media_type="text/plain")

    stream = StringIO()
    df.to_csv(stream, index=False, encoding='utf-8-sig')
    csv_data = stream.getvalue()

    # ساخت نام فایل به صورت RFC 5987 برای پشتیبانی از حروف فارسی
    filename = f"{symbol}_codal.csv"
    encoded_filename = quote(filename)
    content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": content_disposition
        }
    )
