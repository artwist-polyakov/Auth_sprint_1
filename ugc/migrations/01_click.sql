CREATE TABLE IF NOT EXISTS click (
    id UUID,
    user_id String,
    movie_id String,
    timestamp DateTime64(9)
) ENGINE = MergeTree()
ORDER BY timestamp;
