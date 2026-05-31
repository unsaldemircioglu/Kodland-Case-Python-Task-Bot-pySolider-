import pytest
from main import TaskDatabase

@pytest.fixture
def db(tmp_path):
    test_db = tmp_path / "test_add_delete.db"
    return TaskDatabase(str(test_db))

def test_add_and_delete(db):
    db.add_task("Yeni görev")
    tasks = db.show_tasks()
    assert len(tasks) == 1
    db.delete_task(1)
    tasks = db.show_tasks()
    assert tasks == []
