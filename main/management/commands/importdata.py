import re
from functools import partial
from itertools import filterfalse
from operator import attrgetter, methodcaller
from urllib.parse import urljoin

import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.db import connection
from lxml import html
from sqlalchemy import create_engine

from ...models import Borough

URL = 'https://www1.nyc.gov/site/finance/taxes/property-annualized-sales-update.page'


def get_single_borough_data(link, boroughs=None):
    """
    Process data for each borough
    """
    borough = link.getparent().getparent()[0].text_content().strip().upper()

    if boroughs is not None and borough not in boroughs:
        return pd.DataFrame()

    data_url = urljoin(URL, link.attrib['href'])
    year = re.search(r'(\d{2})[._]', data_url).group(1)
    df = pd.read_excel(data_url, header=4 if year > '10' else 3)
    df.columns = df.columns.str.strip()
    df['BOROUGH'] = borough

    return df


def get_all_data(url, boroughs=None):
    """
    Process data for all boroughs
    """
    resp = requests.get(url)
    tree = html.fromstring(resp.text)
    links = tree.xpath('//h3[contains(text(), "Detailed Annual Sales")]/following::table//a[contains(@href, ".xls")]')
    df = pd.concat(
        filterfalse(
            attrgetter('empty'),
            map(partial(get_single_borough_data, boroughs=boroughs), links)),
        ignore_index=True)
    df = df[df['SALE PRICE'] != 0]
    df['NEIGHBORHOOD'] = df['NEIGHBORHOOD'].str.strip()
    df['ADDRESS'] = df['ADDRESS'].str.strip()
    df[['BOROUGH', 'NEIGHBORHOOD', 'ADDRESS']] = df[['BOROUGH', 'NEIGHBORHOOD', 'ADDRESS']].fillna('')
    df = df.dropna(subset=['SALE PRICE', 'SALE DATE'])

    return df


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", help="download data from all boroughs")
        parser.add_argument("-b", "--boroughs", type=methodcaller('upper'), nargs='+')

    def handle(self, *args, **options):
        self.stdout.write("Downloading data...")
        if options['all']:
            df = get_all_data(URL)
        elif options['boroughs']:
            df = get_all_data(URL, boroughs=options['boroughs'])
        else:
            df = get_all_data(URL, boroughs=['MANHATTAN'])
        # with open('data.pickle', 'wb') as f:
        #     pickle.dump(df, f)
        # with open('data.pickle', 'rb') as f:
        #     df = pickle.load(f)
        self.stdout.write("Done!")
        self.stdout.write("Importing data...")
        neighborhoods = df[['BOROUGH', 'NEIGHBORHOOD']].drop_duplicates()

        Borough.objects.bulk_create(
            (Borough(name=b) for b in df['BOROUGH'].unique())
        )

        connection.ensure_connection()  # Important, will result in None connection if left out.
        engine = create_engine('postgresql://', creator=lambda: connection.connection)

        boroughs = pd.read_sql('select * from main_borough', engine)
        neighborhoods = neighborhoods.merge(boroughs, left_on='BOROUGH', right_on='name')
        neighborhoods = neighborhoods[['id', 'NEIGHBORHOOD']]
        neighborhoods.columns = ['borough_id', 'name']

        neighborhoods.to_sql('main_neighborhood', engine, index=False, if_exists='append')

        neighborhoods = pd.read_sql("select * from main_neighborhood", engine)
        sales = df.merge(neighborhoods, left_on='NEIGHBORHOOD', right_on='name')
        sales = sales[['id', 'ADDRESS', 'SALE PRICE', 'SALE DATE']]
        sales.columns = ['neighborhood_id', 'address', 'price', 'date']

        sales.to_sql('main_sale', engine, index=False, if_exists='append')

        self.stdout.write("Done!")
