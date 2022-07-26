from datetime import datetime
import requests
from core_ecommerce_api.utils import check_age_of_data

class UDSPriceGetter:
    url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    usd_type = 'Dolar Blue'
    refresh_cache_time_in_minutes = 10
    cache_dir = 'core_ecommerce_api/cache_files/price_cache.txt'

    def get_cached_price_of_blue(self):
        with open(self.cache_dir) as c:
            lines = c.readlines()
            if not lines:
                return False
            if check_age_of_data(lines[0].strip(), self.refresh_cache_time_in_minutes):
                return lines[1].strip()

    def get_price_of_dollar(self):
        blue_value = self.get_cached_price_of_blue()
        if not blue_value:
            response = requests.get(self.url).json()
            for dolar_type in response:
                if dolar_type['casa']['nombre'] == self.usd_type:
                    blue_value = dolar_type['casa']['venta']
                    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    with open('core_ecommerce_api/cache_files/price_cache.txt', 'w') as c:
                        c.write(f"{date}\n")
                        c.write(blue_value)
                    break
        return float(blue_value.replace(',','.'))