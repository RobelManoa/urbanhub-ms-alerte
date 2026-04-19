from types import SimpleNamespace
from unittest.mock import Mock, call

from src.application.process_alert_usecase import ProcessAlertUseCase
from src.domain.entities import Alert


def test_execute_saves_alert_and_sends_notifications_for_all_channels():
    notification_port = Mock()
    repository = Mock()

    user_with_both = SimpleNamespace(email="user1@example.com", phone="+221700000001")
    user_email_only = SimpleNamespace(email="user2@example.com", phone=None)
    user_phone_only = SimpleNamespace(email=None, phone="+221700000002")
    repository.get_users_to_notify.return_value = [
        user_with_both,
        user_email_only,
        user_phone_only,
    ]

    use_case = ProcessAlertUseCase(notification_port, repository)
    alert = Alert(
        type="weather",
        message="Alerte meteo",
        severity="high",
        source="sensor",
    )

    use_case.execute(alert)

    repository.save_alert.assert_called_once_with(alert)
    repository.get_users_to_notify.assert_called_once_with(alert)
    assert notification_port.send.call_count == 4
    notification_port.send.assert_has_calls(
        [
            call(alert, "email", "user1@example.com"),
            call(alert, "sms", "+221700000001"),
            call(alert, "email", "user2@example.com"),
            call(alert, "sms", "+221700000002"),
        ],
        any_order=False,
    )


def test_execute_does_not_send_notification_when_no_destination():
    notification_port = Mock()
    repository = Mock()
    repository.get_users_to_notify.return_value = [
        SimpleNamespace(email=None, phone=None)
    ]

    use_case = ProcessAlertUseCase(notification_port, repository)
    alert = Alert(
        type="system",
        message="Alerte interne",
        severity="low",
        source="monitor",
    )

    use_case.execute(alert)

    repository.save_alert.assert_called_once_with(alert)
    notification_port.send.assert_not_called()
