CREATE TABLE IF NOT EXISTS other_event (
    id UUID,
    user_id UUID,
    movie_id UUID,
    type String,
    created DateTime
) ENGINE = MergeTree()
ORDER BY created;
