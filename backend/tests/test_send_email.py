import pytest
from unittest.mock import patch, AsyncMock
from backend.email.envio_email import send_email

class MockUser:
    def __init__(self, email):
        self.email = email

@pytest.mark.asyncio
async def test_send_email_success():
    user = MockUser(email="cliente@exemplo.com")
    
    with patch("backend.email.envio_email.FastMail") as MockFastMail:
        instance = MockFastMail.return_value
        instance.send_message = AsyncMock()

        await send_email(user) 

        args, _ = instance.send_message.call_args
        message = args[0]
        
        assert message.subject == "Relatório automático"

        recipients_list = [r.email if hasattr(r, 'email') else r for r in message.recipients]
        
        assert recipients_list == ["cliente@exemplo.com"]

@pytest.mark.asyncio
async def test_send_email_error_log(capsys):
    """Testa a captura de erro caso o servidor SMTP falhe."""
    user = MockUser(email="erro@exemplo.com")

    with patch("backend.email.envio_email.FastMail") as MockFastMail:
        instance = MockFastMail.return_value
        instance.send_message = AsyncMock(side_effect=Exception("Falha na conexão"))

        await send_email(user)

        captured = capsys.readouterr()
        assert "Ocorreu um erro ao enviar o e-mail" in captured.out