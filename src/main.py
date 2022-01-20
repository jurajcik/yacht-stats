from dataclasses import dataclass
from datetime import datetime
from typing import List
import logging
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sys
from src.config import BOATAROUND_ENDPOINT, Search, NO_CONTENT_STATUS_CODE, SEARCH_LIST, DB_STRING
from src.entities import Boat, Base, PricePoint

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
log = logging.getLogger()
log.setLevel(logging.INFO)

output_file_handler = logging.FileHandler("output.log")
output_file_handler.setFormatter(logFormatter)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logFormatter)

log.addHandler(output_file_handler)
log.addHandler(stdout_handler)


@dataclass
class Result:
    boataround_data: object
    rent_start: datetime


def process():
    results: List[Result] = []
    now: datetime = datetime.now()

    log.info("Collecting data started")

    for search in SEARCH_LIST:
        search_result = collect(search)
        log.info(f"Collecting data for {search} collected {len(search_result)}")
        results.extend(search_result)

    log.info(f"Collecting data finished, found {len(results)}")

    session = Session(engine)

    boats_new = extract_boats(results, now)
    persist_new_boats(boats_new, session)

    boats = session.query(Boat).all()

    for result in results:
        price_point = extract_price_point(result, boats, now)
        session.add(price_point)

    session.commit()

    log.info(f'Persisted {len(results)} price points')


def extract_price_point(result: Result, boats: List[Boat], now: datetime) -> PricePoint:
    data = result.boataround_data
    boat = next(x for x in boats if x.boataround_ref == data['slug'])

    return PricePoint(
        boat_id=boat.id,
        base_price=data['price'],
        total_price=data['totalPrice'],
        discount=data['discount'],
        created_at=now,
        rent_start=result.rent_start
    )


def persist_new_boats(boats_new: List[Boat], session: Session) -> None:
    boats_current = session.query(Boat).all()
    refs_current = map(lambda x: x.boataround_ref, boats_current)

    for boat in boats_new:
        if boat.boataround_ref not in refs_current:
            log.info(f'Persisting new boat {boat}')
            session.add(boat)

    session.flush()


def extract_boats(results: List[Result], now: datetime) -> List[Boat]:
    boats = {}

    for result in results:
        data = result.boataround_data
        if data['slug'] not in boats:

            water_tank = None

            if 'water_tank' in data['parameters']:
                water_tank = data['parameters']['water_tank']

            boats[data['slug']] = Boat(
                boataround_ref=data['slug'],
                title=data['title'],
                charter=data['charter'],
                length=data['parameters']['length'],
                year=data['parameters']['year'],
                water_tank=water_tank,
                sail=data['sail'],
                manufacturer=data['manufacturer'],
                model=data['model'],
                region=data['region'],
                city=data['city'],
                marina=data['marina'],
                created_at=now
            )

    return boats.values()


def collect(search: Search) -> List[Result]:
    log.info(f'Collecting data for {search}')

    page = 0
    results = []
    rent_start = datetime.strptime(search.check_in, '%Y-%m-%d')

    while True:
        page += 1
        data = request_data(search.check_in, search.check_out, page)

        if data['statusCode'] == NO_CONTENT_STATUS_CODE:
            return results
        else:
            for one in data['data'][0]['data']:
                results.append(Result(
                    boataround_data=one,
                    rent_start=rent_start
                ))


# https://api.boataround.com/v1/search?destinations=split%2Csibenik%2Czadar&category=sailing-yacht&page=1&checkIn=2022-07-09&checkOut=2022-07-16&cabins=3&year=2017-&boatLength=12-14&lang=en_EN&currency=EUR&equipment=bow-thruster
def request_data(check_in: str, check_out: str, page: int):
    params = {'checkIn': check_in,
              'checkOut': check_out,
              'destinations': 'split,sibenik,zadar',
              'category': 'sailing-yacht',
              'equipment': 'bow-thruster',
              'cabins': '3',
              'year': '2017-',
              'boatLength': '12-14',
              'lang': 'en_EN',
              'currency': 'EUR',
              'page': page  # starts with 1
              }

    r = requests.get(BOATAROUND_ENDPOINT + 'search/', params=params)

    if r.status_code != requests.codes.ok:
        raise Exception('Failed to collect boats for {}, response={}'.format(params, r))
    else:
        return r.json()


engine = create_engine(DB_STRING, echo=True, future=True)

Base.metadata.create_all(engine)

process()
