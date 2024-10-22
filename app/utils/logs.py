import logging
import socket
from datetime import datetime
from pathlib import Path
from sys import platform as so

from pytz import timezone


class LogBots(logging.Logger):
    """
    Project Log
    :param company: Company name
    :param robot_number: Number of robot
    :param robot_name: Name of robot
    """

    def __init__(
            self, company: str, robot_number: str or int, robot_name: str
    ):
        self.datetimenow = datetime.now(
            tz=timezone('America/Sao_Paulo')
        )

        if str(so).startswith('win'):
            self.log_path = "C:/logs/" + self.datetimenow.strftime(
                "%Y_%m") + "/"
        else:
            self.log_path = "logs/" + self.datetimenow.strftime(
                "%Y_%m") + "/"

        self._filename = None
        self.company = company
        self.robot_number = f"{robot_number}"
        self.robot_name = robot_name
        self.__create_dir()
        logging.Logger.__init__(self, self.filename)
        self.hostname = str(socket.gethostname())
        self.host_address = str(socket.gethostbyname(self.hostname))
        self.__set_handlers()

    def __create_dir(self):
        """
        This method creates log folder during __init__
        """
        path = Path(self.log_path)
        path.mkdir(parents=True, exist_ok=True)

    def __log_formatter(self):
        log_format = (f'%(asctime)s|{self.hostname}|{self.host_address}|'
                      f'{self.robot_number}|{self.robot_name}|'
                      f'%(levelname)s|%(message)s')

        date_format = '%d/%m/%Y|%H:%M:%S'
        return logging.Formatter(log_format, date_format)

    @property
    def filename(self):
        if self._filename:
            return self._filename
        self._filename = (
            f"{self.log_path}{self.company}_{self.robot_number}_"
            f"{self.datetimenow.strftime('%Y_%m_%d_%H_%M_%S')}.log"
        )
        return self._filename

    def __set_handlers(self):
        filename = self.filename
        formatter = self.__log_formatter()

        sh = logging.StreamHandler()
        fh = logging.FileHandler(filename)

        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        self.addHandler(sh)
        self.addHandler(fh)
