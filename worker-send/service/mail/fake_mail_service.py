import logging
import os
import shutil
import subprocess
from email.message import EmailMessage

from configs.settings import get_settings
from jinja2 import Environment, FileSystemLoader
from service.mail.mail_service import MailService


class FakeMailService(MailService):
    _templates = {}

    def __init__(self):
        self._current_path = os.path.dirname(__file__)
        self._loader = FileSystemLoader(self._current_path)
        self._env = Environment(loader=self._loader)
        self._sendmail_path = shutil.which('fake_sendmail')
        if not self._sendmail_path:
            logging.error("fake_sendmail не найден в системных путях")
            raise FileNotFoundError("Executable 'fake_sendmail' not found")

        # Загружаем нужный шаблон в переменную
        self._templates['WELCOME'] = self._env.get_template('templates/welcome_template.html')

    def send(self, email: str, subject: str, data: dict, template: str) -> bool:
        logging.warning(f'Отправка письма через sendmail инициализировано {subject}')
        if template not in self._templates:
            return False

        message = EmailMessage()
        message['From'] = (f"{get_settings().get_mail_settings().login}@"
                           f"{get_settings().get_mail_settings().domain}")
        message['To'] = email
        message['Subject'] = subject
        message.set_content(self._templates[template].render(**data), subtype='html')

        try:
            # Подготовка команды sendmail
            with subprocess.Popen([self._sendmail_path, '-t'], stdin=subprocess.PIPE) as proc:
                proc.communicate(message.as_bytes())
                if proc.returncode != 0:
                    raise Exception(f"Sendmail exited with status {proc.returncode}")
            logging.info('Письмо отправлено!')
            return True
        except Exception as exc:
            logging.error(f'Не удалось отправить письмо через sendmail: {exc}')
            return False
