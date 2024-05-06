"""Add notifications table partitioning

Revision ID: 3908b095574e
Revises: f406973a46e5
Create Date: 2024-05-01 21:27:05.255603

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3908b095574e'
down_revision: Union[str, None] = 'f406973a46e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE notifications.new_notifications (
    id SERIAL,
    task_id INTEGER NOT NULL,
    is_sended BOOLEAN NOT NULL,
    is_error BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
    ) PARTITION BY RANGE (created_at);
    """)

    op.execute("""
    INSERT INTO notifications.new_notifications (id, task_id, is_sended, is_error, created_at)
    SELECT id, task_id, is_sended, is_error, created_at FROM notifications.notifications;
    """)

    op.execute("""
    DROP TABLE notifications.notifications;
    """)

    op.execute("""
    ALTER TABLE notifications.new_notifications RENAME TO notifications;
    """)

    op.create_index(
        'idx_task_id',
        'notifications',
        ['task_id'],
        unique=False,
        schema='notifications'
    )

    op.execute("""
    CREATE TABLE notifications.notifications_default
    PARTITION OF notifications.notifications DEFAULT;
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_default
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_05 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_05
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_06 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_06
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_07 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_07
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_08 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-08-01') TO ('2024-09-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_08
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_09 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-09-01') TO ('2024-10-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_09
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_10 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_10
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_11 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_11
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.execute("""
    CREATE TABLE notifications.notifications_2024_12 PARTITION OF notifications.notifications
    FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
    """)

    op.execute("""
    ALTER TABLE notifications.notifications_2024_12
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)


def downgrade() -> None:
    op.execute("""
    CREATE TABLE notifications.new_notifications (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL,
    is_sended BOOLEAN NOT NULL,
    is_error BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    );
    """)

    op.execute("""
    INSERT INTO notifications.new_notifications (id, task_id, is_sended, is_error, created_at)
    SELECT id, task_id, is_sended, is_error, created_at FROM notifications.notifications;
    """)

    op.execute("""
    DROP TABLE notifications.notifications;
    """)

    op.execute("""
    ALTER TABLE notifications.new_notifications RENAME TO notifications;
    """)

    op.execute("""
    ALTER TABLE notifications.notifications
    ADD CONSTRAINT fk_task_id FOREIGN KEY (task_id) REFERENCES notifications.tasks(id);
    """)

    op.create_index(
        'idx_task_id',
        'notifications',
        ['task_id'],
        unique=False,
        schema='notifications'
    )

    op.execute("""
    DROP TABLE notifications.notifications_default;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_05;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_06;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_07;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_08;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_09;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_10;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_11;
    """)

    op.execute("""
    DROP TABLE notifications.notifications_2024_12;
    """)
