from src.main import main
from src.ports.event_consumer_port import EventConsumerPort
from src.ports.publisher_port import PublisherPort
from src.ports.repository_port import IoTRepositoryPort
from src.domain.entities import NormalizedIoTWindow


def test_main_wires_dependencies_and_starts_consumer(monkeypatch):
    calls = {}
    fake_collection = object()
    fake_repository = object()
    fake_publisher = object()
    fake_use_case = object()

    class FakeMongoClient:
        def __init__(self, uri):
            calls["uri"] = uri

        def __getitem__(self, database_name):
            calls["database"] = database_name
            return FakeDatabase()

    class FakeDatabase:
        def __getitem__(self, collection_name):
            calls["collection"] = collection_name
            return fake_collection

    class FakeConsumer:
        def __init__(self, use_case):
            calls["consumer_use_case"] = use_case

        def start_consuming(self):
            calls["consumer_started"] = True

    monkeypatch.setattr("src.main.MongoClient", FakeMongoClient)

    def fake_repository_factory(collection):
        calls["repository_collection"] = collection
        calls["repository_instance"] = fake_repository
        return fake_repository

    def fake_publisher_factory():
        calls["publisher_created"] = True
        calls["publisher_instance"] = fake_publisher
        return fake_publisher

    def fake_use_case_factory(repository, publisher):
        calls["use_case_repository"] = repository
        calls["use_case_publisher"] = publisher
        calls["use_case_instance"] = fake_use_case
        return fake_use_case

    monkeypatch.setattr("src.main.MongoIoTRepository", fake_repository_factory)
    monkeypatch.setattr("src.main.RabbitMQPublisher", fake_publisher_factory)
    monkeypatch.setattr("src.main.NormalizeIoTDataUseCase", fake_use_case_factory)
    monkeypatch.setattr("src.main.RabbitMQConsumer", FakeConsumer)

    main()

    assert calls["uri"] == "mongodb://localhost:27017"
    assert calls["database"] == "urbanhub"
    assert calls["collection"] == "iot_collecte"
    assert calls["repository_collection"] is fake_collection
    assert calls["publisher_created"] is True
    assert calls["use_case_repository"] is fake_repository
    assert calls["use_case_publisher"] is fake_publisher
    assert calls["consumer_use_case"] is fake_use_case
    assert calls["consumer_started"] is True


def test_event_consumer_port_abstract_method_can_be_called_via_super():
    class DummyConsumer(EventConsumerPort):
        def start_consuming(self):
            return super().start_consuming()

    assert DummyConsumer().start_consuming() is None


def test_repository_port_abstract_method_can_be_called_via_super():
    class DummyRepository(IoTRepositoryPort):
        def save(self, payload: NormalizedIoTWindow):
            return super().save(payload)

    assert DummyRepository().save(None) is None


def test_publisher_port_abstract_method_can_be_called_via_super():
    class DummyPublisher(PublisherPort):
        def publish(self, payload: NormalizedIoTWindow):
            return super().publish(payload)

    assert DummyPublisher().publish(None) is None
