from datetime import datetime
import requests
from core_ecommerce_api.utils import check_age_of_data

class UDSPriceGetter:
    url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    usd_type = 'Dolar Blue'
    refresh_cache_time_in_minutes = 10
    cache_dir = '/home/santilosa2295/prueba-de-conocimiento-clicoh/basicecommerceproject/core_ecommerce_api/cache_files/price_cache.txt'
    proxies = {
        'http': 'http://santilosa2295.pythonanywhere.com/',
        'https': 'https://santilosa2295.pythonanywhere.com/',
    }

    def get_cached_price_of_blue(self):
        with open(self.cache_dir) as c:
            lines = c.readlines()
            if not lines:
                return False
            updated = check_age_of_data(lines[0].strip(), self.refresh_cache_time_in_minutes)
            return updated, lines[1].strip()

    def get_price_of_dollar(self):
        updated, blue_value = self.get_cached_price_of_blue()
        if not updated:
            try:
                response = requests.get(self.url).json()
                for dolar_type in response:
                    if dolar_type['casa']['nombre'] == self.usd_type:
                        blue_value = dolar_type['casa']['venta']
                        date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        with open(self.cache_dir, 'w') as c:
                            c.write(f"{date}\n")
                            c.write(blue_value)
                        break
            except:
                print("conection failed, using outdated blue value")
                pass
        return float(blue_value.replace(',','.'))