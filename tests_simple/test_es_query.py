import unittest

import requests

URL: str = 'http://localhost:8000/api/v1/'
URL_films: str = URL + 'films/'
URL_genres: str = URL + 'genres/'
URL_persons: str = URL + 'persons/'


def get_response(URL: str = URL_films, params: dict = {}):
    """
    Отправляет запрос на localhost:8000/api/v1/.
    Возвращает ответ.
    """
    response = requests.get(URL, params=params)
    return response


def check_films_data(test, data):
    """
    Функция проверяет, удовлетворяет ли ответ на запрос .../films/... требованиям:
    1) ответ является списком словарей;
    2) каждый словарь содержит поля uuid типа uuid, title типа str, imdb_rating типа float.
    :param test: объект Теста, метод которого вызвал эту функцию
    :param data: ответ на запрос
    """
    test.assertIsInstance(data['results'], list)

    doc = data['results'][0]

    test.assertIsInstance(doc, dict)

    test.assertIn('uuid', doc)
    test.assertIn('title', doc)
    test.assertIn('imdb_rating', doc)

    test.assertIsInstance(doc['uuid'], str)
    test.assertIsInstance(doc['title'], str)
    test.assertIsInstance(doc['imdb_rating'], (float, int))


def check_person_films_data(test, data):
    """
    Функция проверяет, удовлетворяет ли ответ на запрос .../films/... требованиям:
    1) ответ является списком словарей;
    2) каждый словарь содержит поля uuid типа uuid, title типа str, imdb_rating типа float.
    :param test: объект Теста, метод которого вызвал эту функцию
    :param data: ответ на запрос
    """

    test.assertIsInstance(data, list)

    doc = data[0]

    test.assertIsInstance(doc, dict)

    test.assertIn('uuid', doc)
    test.assertIn('title', doc)
    test.assertIn('imdb_rating', doc)

    test.assertIsInstance(doc['uuid'], str)
    test.assertIsInstance(doc['title'], str)
    test.assertIsInstance(doc['imdb_rating'], (float, int))


def get_genre_uuid():
    """
    Функция отправляет запрос .../genres/,
    преобразует ответ в формат JSON,
    берет uuid первого жанра.
    :return: uuid жанра
    """
    response = requests.get(URL_genres, params={'page_size': 1, 'page_number': 1})
    genres = response.json()['results']
    genre_uuid = genres[0]['uuid']
    return genre_uuid


def get_film_uuid():
    """
    Функция отправляет запрос .../films/,
    преобразует ответ в формат JSON,
    берет uuid первого фильма.
    :return: uuid фильма
    """
    response = requests.get(URL_films, params={'page_size': 1, 'page_number': 1})
    films = response.json()['results']
    film_uuid = films[0]['uuid']
    return film_uuid


def get_person_uuid():
    """
    Функция отправляет запрос .../persons/,
    преобразует ответ в формат JSON,
    берет uuid первого person.
    :return: uuid персоны
    """
    response = requests.get(URL_persons, params={'page_size': 1, 'page_number': 1})
    persons = response.json()['results']
    person_uuid = persons[0]['uuid']
    return person_uuid


class TestESQuery(unittest.TestCase):
    def test_films_rating(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/films?sort=-imdb_rating&page_size=50&page_number=1
        возвращается ответ вида
        [
            {
                "uuid": "uuid",
                "title": "str",
                "imdb_rating": "float"
            },
            ...
        ]
        """

        response = get_response(URL_films,
                                {'sort': '-imdb_rating', 'page_size': 50, 'page_number': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        check_films_data(self, data)

    def test_search_films(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/films/search?query=star&page_number=1&page_size=50
        возвращается ответ вида
        [
            {
              "uuid": "uuid",
              "title": "str",
              "imdb_rating": "float"
            },
            ...
        ]
        """

        response = get_response(URL_films, {'query': 'star', 'page_size': 50, 'page_number': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        check_films_data(self, data)

    def test_search_persons(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/persons/search?query=captain&page_number=1&page_size=50
        возвращается ответ вида
        [
            {
              "uuid": "uuid",
              "full_name": "str",
              "films": [
                      {
                        "uuid": "uuid",
                        "roles": ["str"]
                      },
                      ...
              ]
            },
            ...
        ]
        """

        response = get_response(URL_persons + 'search/',
                                {'query': 'george', 'page_size': 50, 'page_number': 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data['results'], list)

        doc = data['results'][0]

        self.assertIsInstance(doc, dict)

        self.assertIn('uuid', doc)
        self.assertIn('full_name', doc)
        self.assertIn('films', doc)

        self.assertIsInstance(doc['uuid'], str)
        self.assertIsInstance(doc['full_name'], str)
        self.assertIsInstance(doc['films'], list)

        film = doc['films'][0]
        self.assertIsInstance(film, dict)

        self.assertIn('uuid', film)
        self.assertIn('roles', film)

        self.assertIsInstance(film['uuid'], str)
        self.assertIsInstance(film['roles'], list)

    def test_film_uuid(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/films/<uuid:UUID>/
        возвращается ответ вида
        {
            "uuid": "uuid",
            "title": "str",
            "imdb_rating": "float",
            "description": "str",
            "genre": [
              { "uuid": "uuid", "name": "str" },
              ...
            ],
            "actors": [
              {
                "uuid": "uuid",
                "full_name": "str"
              },
              ...
            ],
            "writers": [
              {
                "uuid": "uuid",
                "full_name": "str"
              },
              ...
            ],
            "directors": [
              {
                "uuid": "uuid",
                "full_name": "str"
              },
              ...
            ],
        }
        """

        film_uuid = get_film_uuid()
        response = requests.get(URL_films + film_uuid)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertIn('uuid', data)
        self.assertIn('title', data)
        self.assertIn('imdb_rating', data)
        self.assertIn('description', data)
        self.assertIn('genre', data)
        self.assertIn('actors', data)
        self.assertIn('writers', data)
        self.assertIn('directors', data)

        self.assertIsInstance(data['uuid'], str)
        self.assertIsInstance(data['title'], str)
        self.assertIsInstance(data['imdb_rating'], float)
        self.assertIsInstance(data['description'], str)
        self.assertIsInstance(data['genre'], list)
        self.assertIsInstance(data['actors'], list)
        self.assertIsInstance(data['writers'], list)
        self.assertIsInstance(data['directors'], list)

        if data['actors']:
            self.assertIsInstance(data['actors'][0], dict)
            self.assertIn('uuid', data['actors'][0])
            self.assertIn('full_name', data['actors'][0])

        if data['writers']:
            self.assertIsInstance(data['writers'][0], dict)
            self.assertIn('uuid', data['writers'][0])
            self.assertIn('full_name', data['writers'][0])

        if data['directors']:
            self.assertIsInstance(data['directors'][0], dict)
            self.assertIn('uuid', data['directors'][0])
            self.assertIn('full_name', data['directors'][0])

    def test_person_uuid(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/persons/<uuid:UUID>
        возвращается ответ вида
        {
            "uuid": "uuid",
            "full_name": "str",
            "films": [
                {
                  "uuid": "uuid",
                  "roles": ["str"]
                },
                ...
            ]
        }
        """
        person_uuid = get_person_uuid()
        response = requests.get(URL_persons + person_uuid)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertIn('uuid', data)
        self.assertIn('full_name', data)
        self.assertIn('films', data)

        self.assertIsInstance(data['uuid'], str)
        self.assertIsInstance(data['full_name'], str)
        self.assertIsInstance(data['films'], list)

        self.assertIsInstance(data['films'][0], dict)

        self.assertIn('uuid', data['films'][0])
        self.assertIn('roles', data['films'][0])

        self.assertIsInstance(data['films'][0]['uuid'], str)
        self.assertIsInstance(data['films'][0]['roles'], list)

    def test_person_uuid_film(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/persons/<uuid:UUID>/film
        возвращается ответ вида
        [
            {
              "uuid": "uuid",
              "title": "str",
              "imdb_rating": "float"
            },
            ...
        ]
        """
        person_id = get_person_uuid()
        response = get_response(URL_persons + person_id + '/film')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        check_person_films_data(self, data)

    def test_genre_uuid(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/genres/<uuid:UUID>
        возвращается ответ вида
        {
        "uuid": "uuid",
        "name": "str",
        ...
        }
        """
        genre_uuid = get_genre_uuid()
        response = requests.get(URL_genres + genre_uuid)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertIn('uuid', data)
        self.assertIn('name', data)

        self.assertIsInstance(data['uuid'], str)
        self.assertIsInstance(data['name'], str)

    def test_films_rating_genre(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/films?sort=-imdb_rating&genre=<uuid:UUID>
        возвращается ответ вида
        [
            {
                "uuid": "uuid",
                "title": "str",
                "imdb_rating": "float"
            },
            ...
        ]
        """

        genre_uuid = get_genre_uuid()
        response = get_response(URL_films,
                                params={'sort': '-imdb_rating',
                                        'genre': genre_uuid,
                                        'page_size': 50,
                                        'page_number': 1}
                                )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        check_films_data(self, data)

    def test_genres(self):
        """
        Тест проверяет, что на запрос
        GET /api/v1/genres/
        возвращается ответ вида
        [
            {
              "uuid": "uuid",
              "name": "str",
              ...
            },
            ...
        ]
        """

        response = get_response(URL_genres, {'page': 1, 'page_size': 50})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIsInstance(data['results'], list)

        doc = data['results'][0]

        self.assertIsInstance(doc, dict)

        self.assertIn('uuid', doc)
        self.assertIn('name', doc)

        self.assertIsInstance(doc['uuid'], str)
        self.assertIsInstance(doc['name'], str)


if __name__ == '__main__':
    unittest.main()
