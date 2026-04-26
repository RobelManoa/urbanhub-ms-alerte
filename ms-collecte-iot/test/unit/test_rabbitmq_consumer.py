from unittest.mock import Mock

import pika
from pika.exceptions import AMQPConnectionError

from src.adapters.rabbitmq.consumer import RabbitMQConsumer


def test_callback_builds_raw_payload_and_calls_use_case():
    use_case = Mock()
    consumer = RabbitMQConsumer(use_case)

    payload = (
        b'{"id":"sensor-1","loc":"A","ts-d":"11/04/26 10:00:00",'
        b'"ts-e":"11/04/26 10:00:15","data":[{"spd":"45km/h","veh":"car"}]}'
    )

    consumer.callback(None, None, None, payload)

    use_case.execute.assert_called_once()
    raw_payload = use_case.execute.call_args.args[0]
    assert raw_payload.sensor_id == "sensor-1"
    assert raw_payload.location == "A"
    assert raw_payload.started_at == "11/04/26 10:00:00"
    assert raw_payload.ended_at == "11/04/26 10:00:15"
    assert raw_payload.data[0].speed == "45km/h"
    assert raw_payload.data[0].vehicle_type == "car"


def test_start_consuming_configures_queue_and_callback(monkeypatch):
    use_case = Mock()
    consumer = RabbitMQConsumer(use_case)

    fake_channel = Mock()
    fake_connection = Mock()
    fake_connection.channel.return_value = fake_channel

    captured = {}

    def fake_connection_parameters(host):
        captured["host"] = host
        return "params"

    def fake_blocking_connection(params):
        captured["params"] = params
        return fake_connection

    monkeypatch.setattr(pika, "ConnectionParameters", fake_connection_parameters)
    monkeypatch.setattr(pika, "BlockingConnection", fake_blocking_connection)

    consumer.start_consuming()

    assert captured["host"] == consumer.rabbitmq_host
    assert captured["params"] == "params"
    fake_connection.channel.assert_called_once()
    fake_channel.queue_declare.assert_called_once_with(queue=consumer.queue_name)
    kwargs = fake_channel.basic_consume.call_args.kwargs
    assert kwargs["queue"] == consumer.queue_name
    assert kwargs["on_message_callback"] == consumer.callback
    assert kwargs["auto_ack"] is True
    fake_channel.start_consuming.assert_called_once()


def test_start_consuming_handles_connection_error(monkeypatch, capsys):
    use_case = Mock()
    consumer = RabbitMQConsumer(use_case)

    def fake_blocking_connection(_):
        raise AMQPConnectionError("cannot connect")

    monkeypatch.setattr(pika, "BlockingConnection", fake_blocking_connection)

    consumer.start_consuming()

    output = capsys.readouterr().out
    assert "RabbitMQ indisponible" in output
