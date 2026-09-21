"""
使用 requests 库爬取以下 JSON 接口的内容。接口中 products 的值是一个列表，列表中的 json 即为一个产品。 采集要求： 提取每个产品的 handle、title，以及提取 variants 列表中的变体 id，并将结果保存到 CSV 文件中。 CSV 字段要求： handle、title、id（如果一个产品有多个 id，请使用 , 分割）。 链接： https://www.questnutrition.com/collections/protein-bars-all/products.json
"""
import csv
import os
import requests

# 请求头
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
}

# 请求 URL
url = 'https://www.questnutrition.com/collections/protein-bars-all/products.json'
response = requests.get(url, headers=headers)
data = response.json()

products = data.get('products', [])
# 保存到 CSV 文件
csv_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quest_products.csv')
with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as f:
    # 写入 CSV 文件头
    writer = csv.writer(f)
    writer.writerow(['handle', 'title', 'id'])

    for product in products:
        # 提取 handle、title、variants 列表中的变体 id
        handle = product.get('handle', '')
        title = product.get('title', '')
        variants = product.get('variants', [])
        variant_ids = [str(v.get('id', '')) for v in variants]
        ids = ','.join(variant_ids)
        writer.writerow([handle, title, ids])

print(f'数据已保存至 {csv_filename}，共 {len(products)} 条记录')