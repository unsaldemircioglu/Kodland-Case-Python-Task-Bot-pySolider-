import pytest
from main import TaskDatabase

@pytest.fixture
def db(tmp_path):
    test_db = tmp_path / "test_edit_search.db"
    return TaskDatabase(str(test_db))

def test_edit_and_search(db):
    db.add_task("Eski açıklama")
    db.edit_task(1, "Yeni açıklama")
    task = db.get_task(1)
    assert task[0] == "Yeni açıklama"
    results = db.search_tasks("Yeni")
    assert len(results) == 1
