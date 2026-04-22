import os
import asyncio
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from core.models import User

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = int(os.getenv("MAIL_PORT")),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(user: User):
    """
    Envia o e-mail para o endereço do usuário (user.email).
    :param user: Objeto que contém o atributo 'email'
    :param file_path: Caminho do arquivo (PDF) já existente para anexo
    """
    try:

        message = MessageSchema(
            subject="Relatório automático",
            recipients=[user.email], 
            body="Olá, segue em anexo o relatório gerado.",
            subtype=MessageType.plain,
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")

if __name__ == "__main__":

    class MockUser:
        def __init__(self, email):
            self.email = email

    test_user = MockUser(email="yan_teste@exemplo.com")
    
    try:
        asyncio.run(send_email(user=test_user))
    finally:
        pass