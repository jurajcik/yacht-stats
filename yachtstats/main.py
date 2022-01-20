import logging

from sqlalchemy import create_engine

from yachtstats.collector_service import CollectorService
from yachtstats.config import DB_STRING
from yachtstats.entities import Base
from yachtstats.logger import configure_logger

configure_logger()

log = logging.getLogger()

log.info(f'Starting Yacht Stats')

engine = create_engine(DB_STRING, echo=True, future=True)
Base.metadata.create_all(engine)

collector_service = CollectorService(engine)
collector_service.process()
