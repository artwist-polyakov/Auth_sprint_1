CREATE TABLE movie (
    id UUID,
    title String,
    description Nullable(String),
    imdb_rating Nullable(Float),
    genre Array(String),
    modified DateTime,
    created DateTime,
    director Array(String),
    actors_names Array(String),
    writers_names Array(String),
    actors Array(Nested(name String)),
    writers Array(Nested(name String))
) ENGINE = MergeTree()
ORDER BY (created, modified);
