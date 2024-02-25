from functools import lru_cache

from db.logout.redis_logout_storage import RedisLogoutStorage
from db.postgres import PostgresInterface
from db.storages_creator import StoragesCreator

'''
Сможем подменять креатор в тестах

например:

 @pytest.fixture
 def test_creator():
     # Создаем моки для RedisProvider и ElasticProvider
     redis_provider_mock = MagicMock()
     elastic_provider_mock = MagicMock()
     # Возвращаем экземпляр Creator с подменными мок провайдерами
     return Creator(redis_provider_mock, elastic_provider_mock)

 тогда в тестах можно будет делать так:

     def test_get_person_by_id(test_creator):
         # Создаем экземпляр PersonService с подмененным Creator
         person_service = PersonService(test_creator)
         # Проверяем, что в метод get_by_id был вызван метод get_storage
         # у подмененного RedisProvider
         person_service.get_by_id('1')
         test_creator.get_cache_provider().get_storage.assert_called_once()

 или через манкипатч

 def test_some_feature(monkeypatch, test_creator):
     # Подменяем get_creator функцию на версию, возвращающую тестовую фикстуру
     from utils.creator import get_creator
     monkeypatch.setattr('utils.creator.get_creator', lambda: test_creator)

     # Теперь при вызове get_creator в тесте будет возвращаться тестовый
 экземпляр
     creator = get_creator()

'''


@lru_cache()
def get_creator():
    creator = StoragesCreator(
        RedisLogoutStorage(),
        PostgresInterface()
    )
    return creator
