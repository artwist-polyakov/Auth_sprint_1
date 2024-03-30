CREATE TABLE IF NOT EXISTS player_event (
    id UUID,
    user_id UUID,
    movie_id UUID,
    type String,
    depth Int32,
    created DateTime
) ENGINE = MergeTree()
ORDER BY created;
