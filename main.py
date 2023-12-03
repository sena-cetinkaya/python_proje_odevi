import os
import logging
import pymongo
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import Counter
import matplotlib.pyplot as plt

def connect_to_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[DB_NAME]
        log_info("Veritabanına başarı ile bağlanıldı.")
        print("Veritabanına başarı ile bağlanıldı.")
        return db
    except pymongo.errors.ConnectionFailure as e:
        log_error("Bağlantı sağlanamadı.")
        print("Bağlantı sağlanamadı.")
        return None

def create_collection(
        db, collection_name):
    try:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            log_info(f"'{collection_name}' tablosu oluşturuldu.")
            print(f"'{collection_name}' tablosu oluşturuldu.")
        return collection_name
    except Exception as e:
        log_error(f"'{collection_name}' tablosu oluşturulurken hata oluştu.")
        print(f"'{collection_name}' tablosu oluşturulurken hata oluştu.")
        return None

def insert_data(
        db, url, header,
        summary, text, publish_date,
        update_date, img_url_list):
    try:
        db.news.insert_one({
            "url": url, "header": header, "summary": summary,
            "text": text, "publish_date": publish_date,
            "update_date": update_date, "img_url_list": img_url_list}
        )
        log_info("Veriler eklendi.")
        print("veriler eklendi.")
        return url, header, summary, text, publish_date, update_date, img_url_list
    except Exception as e:
        log_error("Veriler eklenemedi.")
        print(f"veriler eklenemedi.")

def data_manipulation(
        db, column_name):
    try:
        result = db.news.aggregate([
            {"$group": {"_id": f"${column_name}", "count": {"$sum": 1}}}
        ])
        for row in result:
            print("veri manipülasyonu yapılarak gruplanan veriler: ", row)
        log_info("Veri manipülasyonu işlemi yapıldı.")
    except Exception as e:
        log_error("Veri gruplanırken hata oluştu")
        print("Veri gruplanırken hata oluştu:", e)

def analyze_and_save_to_words(
        db, table_name, column_name):
    try:
        collection = db[table_name]
        texts = collection.distinct(column_name)
        all_text = ' '.join(texts)
        word_counts = Counter(all_text.split())
        words_collection = db["word_frequency"]
        for word, count in word_counts.items():
            word_data = {"word": word, "count": count}
            words_collection.insert_one(word_data)
        print("Veriler başarıyla kaydedildi.")
        log_info("Veriler başarıyla kaydedildi.")
    except Exception as e:
        print("Veri analiz edilirken hata oluştu:", e)
        log_error("Veri analiz edilirken hata oluştu:")

def plot_top_words_bar_chart(
        db, limit=10):
    try:
        word_frequency_collection = db["word_frequency"]
        top_words = list(word_frequency_collection.find().sort("count", pymongo.DESCENDING).limit(limit))
        words = [word["word"] for word in top_words]
        counts = [word["count"] for word in top_words]
        plt.bar(words, counts)
        plt.xlabel('Kelimeler')
        plt.ylabel('Tekrar Sayısı')
        plt.title(f'En Çok Tekrar Eden {limit} Kelime')
        plt.xticks(rotation=45, ha='right')
        plt.show()
        log_info("Grafik oluşturuldu.")
    except Exception as e:
        print("Grafik oluşturulurken hata oluştu", e)
        log_error("Grafik oluşturulurken hata oluştu")

def get_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    target_div = soup.select('.kategori_yazilist .row .haber-post .haber-content h2')
    for new in target_div:
        sentence = new.text.lower()
        replacements = {
            ' ': '-', '’': '', '‘': '', ':': '',
            ',': '', '.': '-', ';': '-', 'ç': 'c',
            'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        }
        translation_table = str.maketrans(replacements)
        sentence = sentence.translate(translation_table)
        news_details(sentence)

def news_details(sentence):
    news_details_page_url = f'https://turkishnetworktimes.com/{sentence}'
    response = requests.get(news_details_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("url: ", news_details_page_url)
    news_details_page_header = soup.find('h1', class_='single_title')
    print("header: ", news_details_page_header.text)
    news_details_page_summary = soup.find('h2', class_='single_excerpt')
    print("summary: ", news_details_page_summary.get_text())
    news_details_page_text = soup.select('.yazi_icerik p')
    combined_text = ' '.join([paragraph.get_text() for paragraph in news_details_page_text])
    print("text: ", combined_text)
    news_details_page_date = soup.find_all('span', class_='tarih')
    for date in news_details_page_date:
        if 'Yayınlanma' in date.text:
            news_details_page_publish_date = date.text
            print(news_details_page_publish_date)
        else:
            news_details_page_update_date = date.text
            print(news_details_page_update_date)
    news_details_page_img_url_list = soup.select('.row img')
    image_urls = [img.get('data-src') for img in news_details_page_img_url_list]
    print(image_urls)
    insert_data(
        db, news_details_page_url, news_details_page_header.text,
        news_details_page_summary.text, combined_text,
        news_details_page_publish_date, news_details_page_update_date, image_urls
    )

def paginate(
        url, total_pages):
    for page in range(1, total_pages + 1):
        if page == 1:
            page_url = 'https://turkishnetworktimes.com/kategori/gundem/'
            print(f'Fetching data from {page_url}')
            get_news(page_url)
        else:
            page_url = f'{url}page/{page}'
            print(f'Fetching data from {page_url}')
            get_news(page_url)

def setup_logging():
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, "logs.log")
    logging.basicConfig(
        filename = log_file,
        level = logging.DEBUG,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)

WEBSITE_URL = 'https://turkishnetworktimes.com/kategori/gundem/'
DB_NAME = "sena_cetinkaya"
TABLE_NAMES = ['news', 'word_frequency', 'stats']
TOTAL_PAGES = 50
TOTAL_NEWS = 10  

if __name__ == "__main__":
    setup_logging()
    db = connect_to_mongodb()
    if db is not None:
        for table_name in TABLE_NAMES:
            create_collection(db, table_name)
    else:
        log_error("Veritabanı bağlantısı başarısız.")
        print("Veritabanı bağlantısı başarısız!")

    paginate(WEBSITE_URL, TOTAL_PAGES)
    data_manipulation(db, "update_date")
    analyze_and_save_to_words(db, "news", "text")
    plot_top_words_bar_chart(db)