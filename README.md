# Python Proje Ödevi

## Bu repo belirli bir haber sitesinden eş zamanlı olarak veri çekerek, belirli sütunlara odaklanarak veri analizi yapabilen, çekilen verileri MongoDB veritabanına kaydedebilen  ve temiz kod prensiplerine uygun bir Python programıdır. 

### Gerekli Kütüphaneler
```
import os
import logging
import pymongo
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import Counter
import matplotlib.pyplot as plt
``` 
### Program İçerisinde Yer Alan Fonksiyonların Gerçekleştirdiği İşlemler
 * `connect_to_mongodb` fonksiyonu, veritabanına bağlanma işlemlerini gerçekleştirir.
 * `create_collection` fonksiyonu, veritabanında gerekli koleksiyonlar yoksa bu koleksiyonları oluşturmayı sağlar.
 * `insert_data` fonksiyonu, "news" koleksiyonu içerisine haber içeriklerini ekler.
 * `data_manipulation` fonksiyonu, "news" koleksiyonunun "update_date" kolonuna göre gruplama yapar.
 * `analyze_and_save_to_words` fonksiyonu, "word_frequency" koleksiyonuna, "news" koleksiyonunun "text" verisinin içindeki kelimeleri sayarak, kelimeleri sayıları ile birlikte ekler.
 * `plot_top_words_bar_chart` fonksiyonu, "word_frequency" koleksiyonunda en çok tekrar eden 10 kelimenin sütun grafiğini çizer.
 * `get_news` fonksiyonu, her bir haberin detay sayfasına gidebilmek için haberlerin başlıklarını düzenler.
 * `news_details` fonksiyonu, haberlerin sayfasına giderek detaylarını alır ve bu verileri veritabanına kayıt edilebilmesi için "insert_data" fonksiyonuna yollar.
 * `paginate` fonksiyonu, 50 sayfanın her birinde bulunan 10 adet haberi alabilmek için, 50 sayfayı sıra ile gezmeyi sağlar.
 * `setup_logging` fonksiyonu, programda gerçekleşen işlemlerin log bilgisini tutar. Bu verileri "logs" klasörü altında "logs.log" dosyasında saklar.
 * `log_error` fonksiyonu, hata mesajı vermek için kullanılır.
 * `log_info` fonksiyonu, bilgi mesajı vermek için kullanılır.

### Aşağıda en çok tekrar eden 10 kelimenin frekans grafiğinden bir örnek yer almaktadır.
![Örnek Kelime Frekansı Grafiği](https://github.com/sena-cetinkaya/python_proje_odevi/blob/main/Figure_1.png)

