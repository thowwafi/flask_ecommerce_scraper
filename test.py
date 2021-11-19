
import cloudscraper  
import requests
import csv
from bs4 import BeautifulSoup

key = input('Masukkan keyword : ')
write = csv.writer(open('results/{}.csv'.format(key), 'w', newline=''))
header = ['Nama', 'Harga', 'Stok', 'Rating', 'Kondisi', 'Deskripsi', 'Kategori', 'Rilis', 'Kota', 'Provinsi']
write.writerow(header)

url = 'https://api.bukalapak.com/multistrategy-products'
for page in range(1,11):
    parameter = {
        'prambanan_override': True,
        'keywords': key,
        'limit': 50,
        'offset': 50,
        'page': page,
        'facet': True,
        'access_token': 'vO2WPU-U_3FWT7YHhfvDq5_qbPE-aGNz-SQjJFsHyLW8gg'
        # 'access_token': 'SOL1DrmPvC7sHmnmLlsn3saXrd3688DxGy5h9PtUvbAbHg'
    }

    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
    res = scraper.get(url, params=parameter)
    invoice_url = "https://api.bukalapak.com/invoices?types[]=addon-indihome&types[]=airport-train&types[]=attraction&types[]=bpjs-kesehatan&types[]=buka-pengiriman&types[]=bullion-purchase&types[]=bus&types[]=cable-tv&types[]=coupon-deals&types[]=credit-card-bill&types[]=data-plan-prepaid&types[]=donation-adhoc&types[]=digital-voucher&types[]=electricity_postpaid&types[]=electricity-prepaid&types[]=electricity-non-bill&types[]=event-ticket&types[]=flight&types[]=game-voucher&types[]=government-revenue&types[]=insurance-bill&types[]=mandiri-emoney&types[]=micro-insurances&types[]=multifinance&types[]=pdam&types[]=phone-credit-postpaid&types[]=phone-credit-prepaid&types[]=product&types[]=promoted-push-budget&types[]=property-tax&types[]=push-package&types[]=qr-payment&types[]=telkom-postpaid&types[]=train&types[]=vehicle-tax&types[]=zakat&types[]=covid-standalone-insurance&limit=1&states[]=pending&access_token=vO2WPU-U_3FWT7YHhfvDq5_qbPE-aGNz-SQjJFsHyLW8gg"
    res2 = scraper.get(invoice_url, params=parameter)
    import pdb; pdb.set_trace()
    res.json()

    # get product field
    products = res['data']

    # collect product info
    for p in products:
        nama = p['name']
        harga = p['price']
        stok = p['stock']
        rating = p['rating']['average_rate']
        kondisi = p['condition']
        deskripsi = BeautifulSoup(p['description']).get_text()
        kategori = p['category']['structure']
        rilis = p['relisted_at']
        kota = p['store']['address']['city']
        provinsi = p['store']['address']['province']
        write = csv.writer(open('results/{}.csv'.format(key), 'a', newline=''))
        data = [nama, harga, stok, rating, kondisi, deskripsi, kategori, rilis, kota, provinsi]
        write.writerow(data)


# d1dJrjSc782ORnl_90vzIeW0iaeO9J35Cpefvo8LDwNq0A

# UdXmQnvHy+Q9Ok4yN2lLPb8ZjDyHJUmK8OGzX8Fd0Uv8ZMsq6R51A4KGwVlqIUFcca+7W7xr4UaYIbhgq8dcMA==
# UdXmQnvHy+Q9Ok4yN2lLPb8ZjDyHJUmK8OGzX8Fd0Uv8ZMsq6R51A4KGwVlqIUFcca+7W7xr4UaYIbhgq8dcMA==
# 7f43a2b5-40ac-49e3-8a5f-bf75cb5b9621 86781
# 7461bfae-8276-481b-9d98-97f30896b06f 49426
# bff307f3-8fee-4a53-a6a6-9995ec0eb5a7 14581
# 941c1f04-367f-4ccf-b3f4-685758a6873d 37645