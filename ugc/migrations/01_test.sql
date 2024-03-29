CREATE TABLE clicks (
   id UUID,
   user_id UUID
) ENGINE = MergeTree()
ORDER BY id;
