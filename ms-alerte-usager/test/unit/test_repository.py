from unittest.mock import Mock

from src.adapters.database.models import Alert as AlertModel, Notification, User
from src.adapters.database.repository import SQLAlchemyAlertRepository
from src.domain.entities import Alert


def test_save_alert_adds_model_and_commits_session():
    session = Mock()
    repository = SQLAlchemyAlertRepository(session)
    alert = Alert(
        type="weather",
        message="Vent fort",
        severity="high",
        source="sensor",
    )

    repository.save_alert(alert)

    session.add.assert_called_once()
    saved_model = session.add.call_args.args[0]
    assert isinstance(saved_model, AlertModel)
    assert saved_model.__dict__["type"] == "weather"
    assert saved_model.__dict__["message"] == "Vent fort"
    assert saved_model.__dict__["severity"] == "high"
    assert saved_model.__dict__["source"] == "sensor"
    session.commit.assert_called_once()


def test_get_users_to_notify_returns_query_all_result():
    session = Mock()
    repository = SQLAlchemyAlertRepository(session)
    alert = Alert(
        type="weather",
        message="Pluie",
        severity="medium",
        source="sensor",
    )

    expected_users = [Mock(spec=User), Mock(spec=User)]
    session.query.return_value.all.return_value = expected_users

    result = repository.get_users_to_notify(alert)

    session.query.assert_called_once_with(User)
    session.query.return_value.all.assert_called_once_with()
    assert result == expected_users


def test_save_notification_adds_notification_and_commits_session():
    session = Mock()
    repository = SQLAlchemyAlertRepository(session)

    notification_data = {
        "channel": "email",
        "status": "pending",
    }

    repository.save_notification(notification_data)

    session.add.assert_called_once()
    saved_model = session.add.call_args.args[0]
    assert isinstance(saved_model, Notification)
    assert saved_model.__dict__["channel"] == "email"
    assert saved_model.__dict__["status"] == "pending"
    session.commit.assert_called_once()
