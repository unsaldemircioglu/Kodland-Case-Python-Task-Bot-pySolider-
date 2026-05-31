<img width="716" height="527" alt="image" src="https://github.com/user-attachments/assets/086e2404-0c07-4154-8802-a599f482b3cc" />





Envoriment içerği Discord Devloper Portal Üzeirnden Token alınarak eklenemelidir .gitignordan dolayı api manuel olarak eklenmelidir

Kodun içeirği
Testler
Hata Ayıklama
VeriTabanı
Kodland Ascii Art
Ve Main Dosyası olarak birkaç parçaya ayrılır

Kodu ekledkten sonra Sql3 ortam dğeişkeninde kurulu olamlıdır okunabilmesi için tabikide basit bir vscode uzantısı veya pyCharm Aynı İşi görecektir


Kod içinde kullanılacak kütüphaneler requmantion dosyasının içinde bulunamktadır.

# Merhaba, DÜnya
#Python Bot
Gereksinimler

Python 3.10+ sürümü (senin ortamında 3.14 var, uyumlu).

discord.py kütüphanesi → Discord API ile iletişim kurmak için.

sqlite3 → Görevleri saklamak için veritabanı.

dotenv → .env dosyasından gizli bilgileri (token) okumak için.

logging → Hataları ve olayları kaydetmek için.

Ayrıca:

Discord Developer Portal’da bir bot uygulaması oluşturulmalı.

Bot token .env dosyasında saklanmalı.

“Privileged Intents” (Message Content ve Server Members) Developer Portal’da açılmalı.

Kodun Yapısı
1. TaskDatabase sınıfı
Bu sınıf veritabanı işlemlerini yönetiyor. Görev ekleme, silme, listeleme, tamamlama, güncelleme ve arama gibi tüm işlemler burada tanımlı.
Örneğin:

add_task(description) → yeni görev ekler.

delete_task(task_id) → görevi siler.

show_tasks() → tüm görevleri listeler.

complete_task(task_id) → görevi tamamlanmış olarak işaretler.

search_tasks(keyword) → açıklamaya göre görev arar.

stats() → tamamlanan ve bekleyen görev sayısını döner.

2. TaskManagerBot sınıfı
Discord botunun kendisi. Burada komutlar tanımlanıyor.
Örneğin:

!add_task <açıklama> → görev ekler.

!delete_task <id> → görevi siler.

!show_tasks → görevleri listeler.

!complete_task <id> → görevi tamamlar.

!celebrate <id> → kutlama mesajı gönderir.

!edit_task <id> <yeni açıklama> → görevi günceller.

!search_task <kelime> → görev arar.

!stats → istatistikleri gösterir.

!help_tasks → tüm komutları listeler.

Ayrıca on_command_error fonksiyonu ile hatalar yakalanıyor ve kullanıcıya anlaşılır mesaj veriliyor.

3. Main bölümü
.env dosyasından token yükleniyor.

Discord intents ayarları yapılıyor.

Veritabanı başlatılıyor.

Bot çalıştırılıyor.

Kullanım Senaryosu
Kullanıcı !add_task Raporu yaz der → görev eklenir.

Kullanıcı !show_tasks der → görev listesi gösterilir.

Kullanıcı !complete_task 1 der → görev tamamlanır.

Kullanıcı !celebrate 1 der → kutlama mesajı gönderilir.

Kullanıcı !stats der → kaç görev tamamlandı, kaç görev bekliyor gösterilir.
