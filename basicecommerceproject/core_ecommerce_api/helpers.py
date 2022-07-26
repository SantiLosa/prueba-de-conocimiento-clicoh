import requests

class UDSPriceGetter:
    url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    usd_type = 'Dolar Blue'

    def get_price_of_dollar(self):
        response = requests.get(self.url).json()
        for dolar_type in response:
            if dolar_type['casa']['nombre'] == self.usd_type:
                blue_value = dolar_type['casa']['venta']
                break
        if not blue_value:
            print("Dolar Blue Value not available")
        return float(blue_value.replace(',','.'))