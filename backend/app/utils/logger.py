import logging
from app.config import constants


class Logger:
    _logger = None
    _initialized = False
    
    @classmethod
    def _initialize(cls):
        if not cls._initialized:
            cls._logger = logging.getLogger("app")
            cls._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            cls._logger.addHandler(console_handler)
            
            cls._initialized = True
    
    @classmethod
    def debug(cls, message):
        cls._initialize()
        cls._logger.debug(message)
    
    @classmethod
    def info(cls, message):
        cls._initialize()
        cls._logger.info(message)
    
    @classmethod
    def error(cls, message):
        cls._initialize()
        cls._logger.error(message)
