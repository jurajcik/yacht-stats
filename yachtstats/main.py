import logging
from datetime import timedelta, datetime

import pytz
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from collector_service import CollectorService
from config import DB_STRING
from config import MINIMAL_TIME_PERIOD_OF_RUNS
from entities import Base
from entities import PricePoint
from logger import configure_logger


def allow_new_run() -> bool:
    session = Session(engine)
    last_run_date = session.query(func.max(PricePoint.created_at).label("last")).one().last

    allow = last_run_date + timedelta(hours=MINIMAL_TIME_PERIOD_OF_RUNS) < pytz.UTC.localize(datetime.now())
    log.info(f'Last run was at {last_run_date}, allow next run is {allow}')

    return allow


configure_logger()

log = logging.getLogger()

log.info(f'Starting Yacht Stats')

engine = create_engine(DB_STRING, echo=True, future=True)
Base.metadata.create_all(engine)

if allow_new_run():
    collector_service = CollectorService(engine)
    collector_service.process()
