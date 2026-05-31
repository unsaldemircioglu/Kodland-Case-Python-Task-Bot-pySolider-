import pytest
from main import TaskDatabase

@pytest.fixture
def db(tmp_path):
    # Geçici veritabanı oluştur
    test_db = tmp_path / "test_tasks.db"
    return TaskDatabase(str(test_db))

def test_add_task(db):
    try:
        db.add_task("Rapor yaz")
        tasks = db.show_tasks()
        assert len(tasks) == 1
        assert tasks[0][1] == "Rapor yaz"
    except Exception as e:
        pytest.fail(f"test_add_task hata verdi: {e}")

def test_delete_task(db):
    try:
        db.add_task("Silinecek görev")
        db.delete_task(1)
        tasks = db.show_tasks()
        assert tasks == []
    except Exception as e:
        pytest.fail(f"test_delete_task hata verdi: {e}")

def test_complete_task(db):
    try:
        db.add_task("Tamamlanacak görev")
        db.complete_task(1)
        task = db.get_task(1)
        assert task[1] == 1
    except Exception as e:
        pytest.fail(f"test_complete_task hata verdi: {e}")

def test_edit_and_search(db):
    try:
        db.add_task("Eski açıklama")
        db.edit_task(1, "Yeni açıklama")
        task = db.get_task(1)
        assert task[0] == "Yeni açıklama"
        results = db.search_tasks("Yeni")
        assert len(results) == 1
    except Exception as e:
        pytest.fail(f"test_edit_and_search hata verdi: {e}")

def test_stats(db):
    try:
        db.add_task("Görev 1")
        db.add_task("Görev 2")
        db.complete_task(1)
        completed, pending = db.stats()
        assert completed == 1
        assert pending == 1
    except Exception as e:
        pytest.fail(f"test_stats hata verdi: {e}")
