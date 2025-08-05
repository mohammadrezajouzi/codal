# استفاده از ایمیج رسمی پایتون
FROM python:3.11-slim

# تنظیم پوشه کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های پروژه به کانتینر
COPY . .

# نصب پکیج‌ها
RUN pip install --no-cache-dir fastapi uvicorn pandas requests

# پورت قابل دسترسی
EXPOSE 8000

# اجرای برنامه با uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
