from dataclasses import dataclass


@dataclass
class Search:
    check_in: str
    check_out: str


DB_STRING = "postgresql+psycopg2://yacht-stats-user:yacht-stats-password@localhost/yacht-stats-db"

BOATAROUND_ENDPOINT = 'https://api.boataround.com/v1/'

NO_CONTENT_STATUS_CODE = 204

SEARCH_LIST = [
    Search(check_in='2022-07-02', check_out='2022-07-09'),
    Search(check_in='2022-07-09', check_out='2022-07-16'),
    Search(check_in='2022-07-16', check_out='2022-07-23'),
    Search(check_in='2022-07-23', check_out='2022-07-30'),
    Search(check_in='2022-07-30', check_out='2022-08-06'),
    Search(check_in='2022-08-06', check_out='2022-08-13'),
    Search(check_in='2022-08-13', check_out='2022-08-20'),
    Search(check_in='2022-08-20', check_out='2022-08-27'),
    Search(check_in='2022-08-27', check_out='2022-09-03')
]
