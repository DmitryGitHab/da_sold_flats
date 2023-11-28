import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from PIL._imaging import display

from geopy.geocoders import Nominatim
from geopy.geocoders import options


data_sold_flats = pd.read_csv('sold_flats_2020-09-30.csv', sep=",")
display(data_sold_flats.info())

duplicates = data_sold_flats.copy()
duplicates = duplicates.drop('id', axis=1)
duplicates_df = duplicates[duplicates.duplicated(subset=duplicates.columns, keep=False)]
display(duplicates_df)

options.default_user_agent = "my-custom-user-agent"


def find_location(geolocator, lat, lon):
    try:
        location = geolocator.reverse(f"{lat}, {lon}")
        address = location.raw['address']
        city = address.get('city', np.nan)
        region = address.get('state', np.nan)
        country = address.get('country', np.nan)
    except Exception:
        city = np.nan
        region = np.nan
        country = np.nan

    display(city, region, country)
    return city, region,country



geolocator = Nominatim(user_agent='my-custom-user-agent')


# Если координаты не пропущены и удалось получить адрес по координатам, записываем город, регион, страну в отдельные столбцы
# Если возникла ошибка, записываем координаты в файл и возвращаем None
data_sold_flats[['city', 'region', 'country']] = data_sold_flats.apply(lambda row: pd.Series(find_location(geolocator, row['latitude'], row['longitude'])), axis=1)

data_sold_flats.to_excel('data_sold_flats_location.xlsx', index=False)