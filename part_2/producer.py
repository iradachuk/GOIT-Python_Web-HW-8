import pika
from faker import Faker

from models import User
import connect


fake = Faker()


def create_user(quantity):
    for _ in range(quantity):
        User(fullname=fake.name(),
             email=fake.email()).save()


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='hw8_2_mock', exchange_type='direct')
channel.queue_declare(queue='hw8_2_queue', durable=True)
channel.queue_bind(exchange='hw8_2_mock', queue='hw8_2_queue')


def main():
    for user in User.objects():
        message = str(user.id)

        channel.basic_publish(
            exchange='hw8_2_mock',
            routing_key='hw8_2_queue',
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print('[x] Sent %r' % message)
    connection.close()


if __name__ == '__main__':
    if not User.objects():
        create_user(30)
    main()
