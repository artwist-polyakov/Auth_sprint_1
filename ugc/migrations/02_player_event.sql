CREATE TABLE IF NOT EXISTS player_event (
    id UUID,
    user_id String,
    movie_id String,
    type String,
    event_value String,
    timestamp DateTime64(9)
) ENGINE = MergeTree()
ORDER BY timestamp;
