import pandas as pd
import requests

class SuperbaList:
    def __init__(self, department):
        self.department = department
        self.details = {
            '{size}' : '300x432/',
            '{quality}' : '75',
            '{extension}' : 'jpg'
        }

    def set_url(self):
        return f'https://superbalist.com/api/public/catalogue?department={self.department}&category=shoes&subcategory=sneakers'

    def make_request(self):
        url = self.set_url()
        return requests.request('GET', url)

    def get_data(self):
        self.data = self.make_request().json() 

    def refractor_image_url(self, text):
        for i, j in self.details.items():
            text = text.replace(i, j)
        return text 

    def scrapper(self):
        self.make_request()
        self.get_data()

        productName = [productname['short_name'] for productname in self.data['search']['data']]
        brand = [brandname['designer_name'] for brandname in self.data['search']['data']]
        price = [price['price_range']['max']['retail_price'] for price in self.data['search']['data']]
        image = [self.refractor_image_url(image['asset']['base_url']) for image in self.data['search']['data']]
        age = [self.department] * len(productName)

        return pd.DataFrame({
            'Product Name' : productName,
            'Brand ': brand,
            'Age ': age,
            'Image' : image,
            'Price ': price
        })

def check_gender():
    gender = input('Enter the gender(M/F): ')
    return 'men' if gender == 'M' else 'women'

def create_file():
    scrapper = SuperbaList(check_gender())
    with open('Data.csv', 'a') as f:
        scrapper.scrapper().to_csv(f, header=False, index=False)

def main():
    create_file()

if __name__ == '__main__':
    main()
