CREATE TABLE IF NOT EXISTS other_event (
    id UUID,
    user_id String,
    type String,
    timestamp DateTime64(9)
) ENGINE = MergeTree()
ORDER BY timestamp;
