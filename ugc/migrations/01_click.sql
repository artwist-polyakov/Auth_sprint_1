CREATE TABLE IF NOT EXISTS click (
    id UUID,
    user_id String,
    movie_id String,
    timestamp DateTime64(9, 'Europe/Moscow')
) ENGINE = MergeTree()
ORDER BY timestamp;
