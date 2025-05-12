# The Dyrt US Campground Web Scraper

## Proje Amacı

Bu proje, [The Dyrt](https://thedyrt.com/search) web sitesinden ABD genelindeki kamp alanlarını harita tabanlı API üzerinden otomatik olarak toplayıp PostgreSQL veritabanına kaydetmek amacıyla geliştirilmiştir. Scraper, hem manuel hem de zamanlanmış olarak çalışabilmekte, ayrıca bir API arayüzü üzerinden de etkinleştirilebilmektedir.

## Özellikler

* The Dyrt harita API'si ile scraping
* Tüm ABD'yi kapsayan bounding box tarama
* Pydantic ile veri doğrulama
* SQLAlchemy ORM ile PostgreSQL veritabanı
* Kayıt güncelleme (upsert)
* HTTP retry (tenacity ile)
* APScheduler ile 3 saatte bir otomatik scraping
* FastAPI üzerinden API endpoint (`/run-scraper`)

## 📁 Proje Yapısı

```
case_study/
├── src/
│   ├── api.py               # FastAPI servisi
│   ├── scheduler.py         # Zamanlayıcı görev (APScheduler)
│   ├── scraper.py           # Bounding box üretimi ve API'den veri çekme
│   ├── save_to_db.py        # Doğrulanan verileri veritabanına yazma
│   ├── db/
│   │   └── database.py      # SQLAlchemy modeli ve DB bağlantısı
│   └── models/
│       └── campground.py    # Pydantic doğrulama modeli
├── main.py                  # Manuel olarak scraper'ı çalıştırmak için script
├── requirements.txt         # Projenin Python bağımlılıkları
├── docker-compose.yml       # Docker ile PostgreSQL + API çalıştırma
└── Dockerfile               # Scraper API konteyneri için yapılandırma
```

## ⚙️ Kurulum

### 1. Gerekli Bağımlılıkları Kur

```bash
pip install -r requirements.txt
```

### 2. Veritabanını Başlat (Docker ile)

```bash
docker-compose up -d
```

### 3. Veritabanı Tablolarını Oluştur (isteğe bağlı)

```bash
python src/db/database.py
```

### 4. Manuel Scraper Çalıştırma

```bash
python main.py
```

### 5. FastAPI Sunucusunu Docker ile Başlat

```bash
docker-compose up --build
```

## 🌐 API Endpointleri

> FastAPI otomatik Swagger arayüzü de sağlamaktadır: [http://localhost:8000/docs](http://localhost:8000/docs)

## ⏰ Zamanlayıcı (APScheduler)

* `scheduler.py` dosyasında tanımlanmıştır.
* API başlatıldığında otomatik devreye girer.
* Her **3 saatte bir** scraper'ı çalıştırır ve veritabanını günceller.

## 🔁 Manuel Scraping (`main.py`)

* Tüm ABD'yi kapsayan bounding box'ları oluşturur.
* Her bbox için `fetch_bbox_data` fonksiyonu ile veri çeker.
* `save_campgrounds` fonksiyonu ile veritabanına ekler ya da günceller.

---

**Hazırlayan:** İsmail Kılıç

