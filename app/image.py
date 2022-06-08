from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
import os
from urllib.parse import urljoin
import requests


def get_uuid_of_product() -> str:
    api = SentinelAPI(
        os.getenv("COPERNICUS_USERNAME"),
        os.getenv("COPERNICUS_PASSWORD"),
        "https://scihub.copernicus.eu/dhus/",
    )

    footprint = geojson_to_wkt(read_geojson("map.geojson"))
    products = api.query(
        footprint,
        date=("NOW-30DAY", "NOW"),
        platformname="Sentinel-2",
        area_relation="Intersects",
        limit=1,
        cloudcoverpercentage=(0, 10),
    )
    return list(products.keys())[0]


def get_url_for_image(prod_id: str):
    api = requests.Session()
    api.auth = (
        os.getenv("COPERNICUS_USERNAME"),
        os.getenv("COPERNICUS_PASSWORD"),
    )
    print
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
    band_id = bands.json()["d"]["results"][3]["Id"]

    url = f"Products('{prod_id}')/Nodes('{prod_name}')/Nodes('GRANULE')/Nodes('{gran_id}')/Nodes('IMG_DATA')/Nodes('R10m')/Nodes('{band_id}')/$value"
    return urljoin(api_url, url)


def download_picture(url: str):
    response = requests.get(
        url,
        auth=(
            os.getenv("COPERNICUS_USERNAME"),
            os.getenv("COPERNICUS_PASSWORD"),
        ),
    )
    response.raise_for_status()
    with open("ddd.jp2", "wb") as image:
        image.write(response.content)


if __name__ == "__main__":
    
    prod_id = get_uuid_of_product()
    url = get_url_for_image(prod_id)
    download_picture(url)
