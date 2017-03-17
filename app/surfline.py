from multiprocessing import Pool
from requests import Session

SURFLINE_URI = 'http://api.surfline.com/v1/forecasts'


def fetch_spots(spot_ids):
    pool = Pool(5)
    uris = [f'{SURFLINE_URI}/{spot_id}' for spot_id in spot_ids]
    with Session() as session:
        res = pool.map(session.get, uris)
        pool.close()
        pool.join()
        return res
