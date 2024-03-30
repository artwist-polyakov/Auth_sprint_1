CREATE TABLE IF NOT EXISTS click (
    id UUID,
    user_id UUID,
    movie_id UUID,
    created DateTime
) ENGINE = MergeTree()
ORDER BY created;
