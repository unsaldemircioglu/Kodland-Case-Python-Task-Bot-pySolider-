import pytest                     # pytest kütüphanesini içe aktarır, testleri çalıştırmak için kullanılır
from main import TaskDatabase      # main.py içindeki TaskDatabase sınıfını test etmek için içe aktarır

@pytest.fixture
def db(tmp_path):                  # pytest fixture: her test için geçici bir veritabanı oluşturur
    test_db = tmp_path / "test_tasks.db"   # tmp_path pytest’in sağladığı geçici klasördür
    return TaskDatabase(str(test_db))      # TaskDatabase sınıfını bu geçici dosya ile başlatır

def test_add_task(db):             # Görev ekleme fonksiyonunu test eder
    db.add_task("Rapor yaz")       # Yeni görev eklenir
    tasks = db.show_tasks()        # Görevler listelenir
    assert len(tasks) == 1         # Görev sayısı 1 olmalı
    assert tasks[0][1] == "Rapor yaz"   # Eklenen görevin açıklaması doğru olmalı

def test_delete_task(db):          # Görev silme fonksiyonunu test eder
    db.add_task("Silinecek görev") # Önce bir görev eklenir
    db.delete_task(1)              # ID’si 1 olan görev silinir
    tasks = db.show_tasks()        # Görevler tekrar listelenir
    assert tasks == []             # Liste boş olmalı

def test_complete_task(db):        # Görev tamamlama fonksiyonunu test eder
    db.add_task("Tamamlanacak görev")   # Görev eklenir
    db.complete_task(1)            # ID’si 1 olan görev tamamlanır
    task = db.get_task(1)          # Görev bilgisi alınır
    assert task[1] == 1            # completed alanı 1 (tamamlandı) olmalı

def test_edit_and_search(db):      # Görev güncelleme ve arama fonksiyonlarını test eder
    db.add_task("Eski açıklama")   # Görev eklenir
    db.edit_task(1, "Yeni açıklama")   # Görev açıklaması güncellenir
    task = db.get_task(1)          # Görev bilgisi alınır
    assert task[0] == "Yeni açıklama"  # Açıklama güncellenmiş olmalı
    results = db.search_tasks("Yeni")  # "Yeni" kelimesi ile arama yapılır
    assert len(results) == 1       # Arama sonucu 1 görev olmalı

def test_stats(db):                # Görev istatistiklerini test eder
    db.add_task("Görev 1")         # İlk görev eklenir
    db.add_task("Görev 2")         # İkinci görev eklenir
    db.complete_task(1)            # İlk görev tamamlanır
    completed, pending = db.stats()   # İstatistikler alınır
    assert completed == 1          # Tamamlanan görev sayısı 1 olmalı
    assert pending == 1            # Bekleyen görev sayısı 1 olmalı
