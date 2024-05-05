import logging

from configs.settings import get_settings
from service.mail.mail_service import MailService
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os


class SMTPMailService(MailService):
    _templates = {}

    def __init__(self):
        mail_settings = get_settings().get_mail_settings()
        self._smtp_server = mail_settings.smtp_server
        self._smtp_port = mail_settings.smtp_port
        self._login = mail_settings.login
        self._password = mail_settings.password
        self._domain = mail_settings.domain

        self._server = smtplib.SMTP_SSL(
            self._smtp_server,
            self._smtp_port
        )

        self._server.login(
            self._login,
            self._password
        )

        self._current_path = os.path.dirname(__file__)
        self._loader = FileSystemLoader(self._current_path)
        self._env = Environment(loader=self._loader)

        # Загружаем нужный шаблон в переменную
        self._templates['welcome'] = self._env.get_template('templates/welcome_template.html')

    def __del__(self):
        try:
            self._server.close()
        except Exception as exc:
            logging.error(f'Не удалось закрыть соединение с сервером. {exc}')

    def send(
            self,
            email: str,
            subject: str,
            data: dict,
            template: str
    ) -> bool:
        if template not in self._templates:
            return False
        message = EmailMessage()
        message['From'] = self._login + '@' + self._domain
        message['To'] = email
        message['Subject'] = subject
        output = self._templates[template].render(**data)
        message.add_alternative(output, subtype='html')
        try:
            self._server.sendmail(self._login + '@' + self._domain, [email], message.as_string())
        except smtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            logging.error(f'Не удалось отправить письмо. {reason}')
        else:
            logging.info('Письмо отправлено!')
