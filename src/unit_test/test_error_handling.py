import pytest
from main import TaskDatabase

@pytest.fixture
def db(tmp_path):
    test_db = tmp_path / "test_error_handling.db"
    return TaskDatabase(str(test_db))

def test_delete_nonexistent_task(db):
    try:
        db.delete_task(999)  # olmayan görev
        tasks = db.show_tasks()
        assert tasks == []
    except Exception as e:
        pytest.fail(f"Hata yakalandı: {e}")

def test_get_nonexistent_task(db):
    task = db.get_task(999)
    assert task is None or task == ()
