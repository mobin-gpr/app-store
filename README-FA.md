# 🚀 فروشگاه اپلیکیشن جنگو

<div align="center" dir="rtl">

![App Store Cover](screenshots/cover.png)

[![Django](https://img.shields.io/badge/Django-4.2%20LTS-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**یک فروشگاه اپلیکیشن اندروید حرفه‌ای و کامل ساخته شده با جنگو**

[ویژگی‌ها](#-ویژگی‌ها) • [شروع سریع](#-شروع-سریع) • [مستندات](#-مستندات) • [مشارکت](#-مشارکت)

</div>

---

<div dir="rtl">

## 📋 فهرست مطالب

- [معرفی](#-معرفی)
- [ویژگی‌ها](#-ویژگی‌ها)
- [فناوری‌های استفاده شده](#-فناوری‌های-استفاده-شده)
- [معماری](#-معماری)
- [شروع سریع](#-شروع-سریع)
- [پیکربندی](#-پیکربندی)
- [استقرار](#-استقرار)
- [مشارکت](#-مشارکت)
- [تیم سازنده](#-تیم-سازنده)
- [مجوز](#-مجوز)

---

## 🌟 معرفی

فروشگاه اپلیکیشن جنگو یک پلتفرم جامع و آماده برای استقرار جهت توزیع اپلیکیشن‌ها و بازی‌های اندروید است. این پروژه با استفاده از جدیدترین تکنولوژی‌های وب و بهترین روش‌های برنامه‌نویسی ساخته شده و راه‌حلی کامل برای مدیریت، توزیع و کشف اپلیکیشن‌های موبایل ارائه می‌دهد.

این پروژه به‌طور کامل بازنویسی شده و با استانداردهای سطح سازمانی در زمینه کیفیت کد، امنیت و مقیاس‌پذیری بهبود یافته است که آن را برای پروژه‌های کوچک و استقرارهای بزرگ مناسب می‌کند.

### چرا این پروژه؟

✅ **آماده برای استقرار**: کاملاً پیکربندی شده برای محیط توسعه و تولید  
✅ **امن**: پیاده‌سازی استانداردهای امنیتی صنعتی  
✅ **مقیاس‌پذیر**: طراحی شده برای مدیریت ترافیک بالا با کش و بهینه‌سازی  
✅ **مستندسازی کامل**: مستندات جامع و کد تمیز  
✅ **پشتیبانی از Docker**: استقرار آسان با Docker  
✅ **پشتیبانی کامل از فارسی**: پشتیبانی کامل از زبان فارسی و چیدمان RTL  

---

## ✨ ویژگی‌ها

### 🎯 ویژگی‌های اصلی

- **📱 مدیریت اپلیکیشن**
  - پشتیبانی از چندین نسخه (مود، اورجینال و...)
  - وارد کردن خودکار اطلاعات از گوگل پلی
  - لینک‌های دانلود سفارشی با رنگ‌بندی
  - گالری اسکرین‌شات اپلیکیشن‌ها
  - سیستم دسته‌بندی و برچسب‌گذاری

- **👥 مدیریت کاربران**
  - سیستم احراز هویت سفارشی
  - تایید ایمیل و فعال‌سازی حساب
  - بازیابی رمز عبور
  - ورود با شبکه‌های اجتماعی (گوگل، گیت‌هاب)
  - سیستم آواتار با گزینه‌های از پیش آماده
  - پروفایل کاربری (عمومی و خصوصی)

- **💬 سیستم پیشرفته نظرات**
  - نظرات تو در تو با پاسخ
  - قابلیت لایک/دیسلایک
  - تمایز بین ادمین و کاربر عادی
  - مدیریت نظرات
  - تعامل همزمان

- **📰 اخبار و وبلاگ**
  - مقالات خبری با برچسب
  - محتوای متنی غنی
  - بهینه‌سازی سئو
  - اشتراک‌گذاری اجتماعی

- **🎨 رابط کاربری**
  - حالت تاریک و روشن
  - طراحی واکنش‌گرا
  - رابط مدرن و جذاب
  - پشتیبانی از تاریخ شمسی
  - بارگذاری تنبل تصاویر
  - انیمیشن‌های روان

### 🔧 ویژگی‌های فنی

- **امنیت**
  - محافظت CSRF
  - جلوگیری از XSS
  - محافظت از SQL Injection
  - هش امن رمز عبور
  - اجبار HTTPS (تولید)
  - URL ادمین سفارشی
  - پشتیبانی از محدودیت نرخ

- **عملکرد**
  - کش Redis
  - بهینه‌سازی کوئری دیتابیس
  - فشرده‌سازی فایل‌های استاتیک
  - پشتیبانی CDN (AWS S3)
  - ایندکس‌گذاری دیتابیس
  - بارگذاری تنبل

- **DevOps**
  - Docker و Docker Compose
  - تنظیمات جداگانه dev/prod
  - مایگریشن‌های خودکار
  - سیستم لاگ
  - اندپوینت بررسی سلامت
  - آماده CI/CD

---

## 🛠 فناوری‌های استفاده شده

### Backend
- **فریمورک**: Django 4.2.16 LTS (پشتیبانی بلند مدت)
- **زبان**: Python 3.8+
- **دیتابیس**: PostgreSQL 16 (تولید) / SQLite (توسعه)
- **کش**: Redis 7
- **صف کار**: (آماده برای Celery)

### Frontend
- **موتور قالب**: Django Templates
- **CSS**: CSS سفارشی با پشتیبانی RTL
- **JavaScript**: jQuery, Custom JS
- **آیکون‌ها**: مجموعه آیکون سفارشی

### DevOps
- **کانتینرسازی**: Docker, Docker Compose
- **وب سرور**: Nginx (تولید)
- **WSGI سرور**: Gunicorn
- **فایل‌های استاتیک**: WhiteNoise / AWS S3
- **مانیتورینگ**: Sentry (اختیاری)

---

## 🚀 شروع سریع

### پیش‌نیازها

- Python 3.11 یا بالاتر
- PostgreSQL 16 (برای تولید)
- Redis 7 (برای کش)
- Git

### توسعه محلی

1. **کلون کردن مخزن**
   ```bash
   git clone https://github.com/mobin-gpr/app-store.git
   cd app-store
   ```

2. **ایجاد محیط مجازی**
   ```bash
   python -m venv venv
   source venv/bin/activate  # در ویندوز: venv\Scripts\activate
   ```

3. **نصب وابستگی‌ها**
   ```bash
   pip install -r requirements/development.txt
   ```

4. **تنظیم متغیرهای محیطی**
   ```bash
   cp .env.example .env
   # ویرایش .env با تنظیمات خود
   ```

5. **اجرای مایگریشن‌ها**
   ```bash
   python manage.py migrate
   ```

6. **جمع‌آوری آواتارها**
   ```bash
   python manage.py collectavatars
   ```

7. **ایجاد سوپریوزر**
   ```bash
   python manage.py createsuperuser
   ```

8. **اجرای سرور توسعه**
   ```bash
   python manage.py runserver
   ```

9. **دسترسی به اپلیکیشن**
   - سایت اصلی: http://localhost:8000
   - پنل ادمین: http://localhost:8000/admin

### راه‌اندازی با Docker

#### توسعه با Docker

```bash
# ساخت و اجرای کانتینرها
docker-compose up -d

# اجرای مایگریشن‌ها
docker-compose exec web python manage.py migrate

# ایجاد سوپریوزر
docker-compose exec web python manage.py createsuperuser

# جمع‌آوری آواتارها
docker-compose exec web python manage.py collectavatars

# مشاهده لاگ‌ها
docker-compose logs -f
```

#### تولید با Docker

```bash
# ساخت ایمیج‌های تولید
docker-compose -f docker-compose.prod.yml build

# اجرای کانتینرهای تولید
docker-compose -f docker-compose.prod.yml up -d

# اجرای مایگریشن‌ها
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# جمع‌آوری فایل‌های استاتیک
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
```

### استفاده از Makefile (توصیه می‌شود)

```bash
# مشاهده دستورات موجود
make help

# نصب وابستگی‌ها
make install-dev

# اجرای مایگریشن‌ها
make migrate

# اجرای سرور توسعه
make run

# اجرای با Docker
make docker-up
```

---

## ⚙️ پیکربندی

### متغیرهای محیطی

یک فایل `.env` بر اساس `.env.example` ایجاد کنید:

```env
# تنظیمات اصلی
SECRET_KEY=کلید-امنیتی-شما
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# دیتابیس (PostgreSQL برای تولید)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=appstore_db
DB_USER=appstore_user
DB_PASSWORD=رمز_امن
DB_HOST=localhost
DB_PORT=5432

# کش (Redis)
REDIS_URL=redis://127.0.0.1:6379/1

# ایمیل
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=ایمیل-شما@gmail.com
EMAIL_HOST_PASSWORD=رمز-اپ-شما
DEFAULT_FROM_EMAIL=noreply@دامنه-شما.com
```

---

## 🌐 استقرار

### چک‌لیست تولید

- [ ] تنظیم `DEBUG=False`
- [ ] تولید `SECRET_KEY` قوی
- [ ] پیکربندی `ALLOWED_HOSTS`
- [ ] راه‌اندازی دیتابیس PostgreSQL
- [ ] پیکربندی Redis برای کش
- [ ] راه‌اندازی گواهی HTTPS/SSL
- [ ] پیکربندی تنظیمات ایمیل
- [ ] تنظیم `ADMIN_URL` سفارشی
- [ ] فعال‌سازی هدرهای امنیتی
- [ ] پیکربندی سرو فایل‌های استاتیک
- [ ] راه‌اندازی استراتژی پشتیبان
- [ ] پیکربندی مانیتورینگ (Sentry)

### استقرار با Docker (توصیه می‌شود)

```bash
# 1. به‌روزرسانی متغیرهای محیطی
cp .env.example .env
# ویرایش .env با مقادیر تولید

# 2. ساخت و اجرا
docker-compose -f docker-compose.prod.yml up -d --build

# 3. اجرای مایگریشن‌ها
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# 4. جمع‌آوری فایل‌های استاتیک
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 5. ایجاد سوپریوزر
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

---

## 🤝 مشارکت

ما از مشارکت شما استقبال می‌کنیم! لطفاً این مراحل را دنبال کنید:

1. فورک کردن مخزن
2. ایجاد برنچ ویژگی (`git checkout -b feature/AmazingFeature`)
3. کامیت تغییرات (`git commit -m 'Add some AmazingFeature'`)
4. پوش به برنچ (`git push origin feature/AmazingFeature`)
5. باز کردن Pull Request

---

## 👥 تیم سازنده

### توسعه‌دهندگان

- **[مبین قنبرپور](https://github.com/mobin-gpr)** - توسعه‌دهنده Backend
- **[مهیار نصیری](https://github.com/Mhyar-nsi)** - توسعه‌دهنده Frontend

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است - فایل [LICENSE](LICENSE) را برای جزئیات مشاهده کنید.

---

## 🙏 قدردانی

- جامعه Django برای فریمورک عالی
- تمام کتابخانه‌های متن‌باز استفاده شده در این پروژه
- مشارکت‌کنندگان و تستر‌ها

---

## 📞 پشتیبانی

- **مسائل**: [GitHub Issues](https://github.com/mobin-gpr/app-store/issues)
- **بحث‌ها**: [GitHub Discussions](https://github.com/mobin-gpr/app-store/discussions)

---

## 🔮 نقشه راه

- [ ] پیاده‌سازی REST API
- [ ] بهبود داشبورد ادمین
- [ ] آنالیتیکس پیشرفته
- [ ] اپلیکیشن موبایل (React Native)
- [ ] یکپارچه‌سازی درگاه پرداخت
- [ ] پشتیبانی از چند زبان
- [ ] جستجوی پیشرفته با Elasticsearch
- [ ] سیستم پیشنهاددهنده

---

<div align="center">

**[بازگشت به بالا ⬆](#-فروشگاه-اپلیکیشن-جنگو)**

ساخته شده با ❤️ توسط تیم فروشگاه اپلیکیشن

[English Version](README.md)

</div>

</div>
