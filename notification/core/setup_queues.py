from db.rabbit_storage import RabbitMQCore

queue_names = ['q1', 'q2', 'q3', 'q4']

with RabbitMQCore() as rabbitmq_core:
    for queue_name in queue_names:
        rabbitmq_core.create_queue(queue_name)
