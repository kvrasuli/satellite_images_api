from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from urllib.parse import urljoin
import requests
import argparse


def get_uuid_of_product(username, password, filename) -> str:
    api = SentinelAPI(
        username,
        password,
        "https://scihub.copernicus.eu/dhus/",
    )

    footprint = geojson_to_wkt(read_geojson(filename))
    products = api.query(
        footprint,
        date=("NOW-60DAY", "NOW"),
        platformname="Sentinel-2",
        area_relation="Intersects",
        limit=1,
        cloudcoverpercentage=(0, 10),
    )
    return list(products.keys())[0]


def get_url_for_image(username, password, prod_id, band):
    api = requests.Session()
    api.auth = (username, password)
    api_url = "https://scihub.copernicus.eu/dhus/odata/v1/"

    url = f"Products('{prod_id}')/Nodes?$format=json"
    product = api.get(urljoin(api_url, url))
    product.raise_for_status()
    prod_name = product.json()["d"]["results"][0]["Id"]

    url = f"Products('{prod_id}')/Nodes('{prod_name}')/Nodes('GRANULE')/Nodes?$format=json"
    granules = api.get(urljoin(api_url, url))
    granules.raise_for_status()
    gran_id = granules.json()["d"]["results"][0]["Id"]

    url = f"Products('{prod_id}')/Nodes('{prod_name}')/Nodes('GRANULE')/Nodes('{gran_id}')/Nodes('IMG_DATA')/Nodes('R10m')/Nodes/?$format=json"
    bands = api.get(urljoin(api_url, url))
    bands.raise_for_status()
    # element 3 is band 4, element 4 band 8
    element = 3 if band == '4' else 4 if band == '8' else None
    band_id = bands.json()["d"]["results"][element]["Id"]

    url = f"Products('{prod_id}')/Nodes('{prod_name}')/Nodes('GRANULE')/Nodes('{gran_id}')/Nodes('IMG_DATA')/Nodes('R10m')/Nodes('{band_id}')/$value"
    return urljoin(api_url, url)


def download_picture(username, password, url, band, filename):
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    with open(f"{filename}_band{band}.jp2", "wb") as image:
        image.write(response.content)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="copernicus username")
    parser.add_argument("--password", help="copernicus password")
    parser.add_argument("--filename", help="path to geojson")
    parser.add_argument("--band", help="number of band")
    args = parser.parse_args()
    return  args.username, args.password, args.filename, args.band


if __name__ == "__main__":
    username, password, filename, band = parse_args()
    prod_id = get_uuid_of_product(username, password, filename)
    url = get_url_for_image(username, password, prod_id, band)
    download_picture(username, password, url, band, filename)
