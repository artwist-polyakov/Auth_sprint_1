CREATE TABLE IF NOT EXISTS movies (
    id UUID,
    title String,
    description Nullable(String),
    imdb_rating Nullable(Float32),
    genre Array(String),
    modified DateTime,
    created DateTime,
    director Array(String),
    actors_names Array(String),
    writers_names Array(String),
) ENGINE = MergeTree()
ORDER BY (created);
