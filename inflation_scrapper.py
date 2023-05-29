import argparse
from datetime import datetime
import pandas as pd
import calendar
import requests
import tabula
from tabula.io import read_pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="date in DD/MM/YYYY format")
    args = vars(ap.parse_args())
    scrapper_spi(args)

def scrapper_spi(args):

    date_time_str = args['date']
    scrape_date = datetime.strptime(date_time_str, '%d/%m/%Y')
    get_pdf_from_pbs(scrape_date)

def get_pdf_from_pbs(scrape_date):

    day=scrape_date.strftime('%d')
    month=scrape_date.strftime('%m')
    year=scrape_date.strftime('%Y')
    
    scrape_url = f'''https://www.pbs.gov.pk/sites/default/files/price_statistics/weekly_spi/SPI_Annex%26USCP_{day}{month}{year}.pdf'''

    scrapped_pdf = requests.get(scrape_url)
    with open('weekly_spi-{}-{}-{}.pdf'.format(day,month,year), 'wb') as f:
        f.write(scrapped_pdf.content)
    print('weekly_spi-{}-{}-{}.pdf'.format(day,month,year)," saved")
    convert_to_csv(day,month,year)

def convert_to_csv(day,month,year):
    file_path='weekly_spi-{}-{}-{}.pdf'.format(day,month,year)
    scrapped_pdf= read_pdf(file_path,pages="all",guess=True)
    df=scrapped_pdf[0]
    df.to_csv('weekly_spi-{}-{}-{}.csv'.format(day,month,year))
    print('weekly_spi-{}-{}-{}.csv'.format(day,month,year)," saved")


if __name__ == "__main__":
    main()
