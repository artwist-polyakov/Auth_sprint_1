from functools import wraps

STATE_KEY = "last_movies_updated"
FILM_WORK_QUERY: str = """
SELECT
    fw.id,
    fw.modified,
    fw.created,
    fw.rating AS imdb_rating,
    COALESCE (
        ARRAY_AGG(
            DISTINCT g.name
        ) FILTER (WHERE g.name is not NULL),
        '{}'
    ) AS genre,
    fw.title,
    fw.description,
    COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'director'),
       '{}'
   ) as director,
   COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'actor'),
       '{}'
   ) as actors_names,
     COALESCE (
       ARRAY_AGG(
           DISTINCT (p.full_name)
       ) FILTER (WHERE pfw.role = 'writer'),
       '{}'
   ) as writers_names
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON gfw.genre_id = g.id
WHERE fw.modified > %s
GROUP BY fw.id
ORDER BY fw.modified ASC;
"""


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner
