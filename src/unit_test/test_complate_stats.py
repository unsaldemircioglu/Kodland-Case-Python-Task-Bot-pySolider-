import pytest
from main import TaskDatabase

@pytest.fixture
def db(tmp_path):
    test_db = tmp_path / "test_complete_stats.db"
    return TaskDatabase(str(test_db))

def test_complete_and_stats(db):
    db.add_task("Görev 1")
    db.add_task("Görev 2")
    db.complete_task(1)
    completed, pending = db.stats()
    assert completed == 1
    assert pending == 1
