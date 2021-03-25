from url_shortener.storage import InMemoryStorage
from url_shortener.logic import Logic


def test_logic_fails_to_save_when_key_already_exists():
    storage = InMemoryStorage()
    logic = Logic(storage=storage)
    logic.save_example_if_not_exists("test", "value 1")
    assert logic.save_example_if_not_exists("test", "value 2") is False
    assert logic.get_example("test") == "value 1"
