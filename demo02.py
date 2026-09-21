"""
使用 requests 库爬取以下链接中的所有商品（共 4 页），并将数据存储到 CSV 文件中。 字段要求： 产品名称 (name)、原价 (price)、产品图片 (images)（多张图片请使用 , 分割）、成分 (Key Ingredients)、尺码选项 (Size)。 链接： https://www.cosrx.com/collections/all
"""
import re
import csv
import time
import requests
from lxml import etree


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "\"page_cache:51337756828:CollectionDetailsController:a05e0c58004e9937a2f4203f563b9c96:56a7f1f0b8bbac90d1f39d6df878c80f\"",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-viewport-width": "592",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
}

url = 'https://www.cosrx.com/collections/all'


def get_html(url, page=1, max_retries=3):
    """
    获取列表页源码
    """
    params = {
        "page": str(page)
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            return response.text
        except Exception as e:
            print(f'  列表页请求失败(第{attempt + 1}次): {e}')
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                raise


def parse_product_list(html):
    """
    解析列表页商品url
    :param html: 列表页源码
    :return: 商品url列表
    """
    tree = etree.HTML(html)
    product_urls = tree.xpath(
        '//div[@class="image-cont image-cont--with-secondary-image "]/a[@class="product-link"]/@href')
    if product_urls:
        return product_urls
    else:
        return []


def get_product_info(refererurl, url, max_retries=3):
    """
    refererurl:商品详情页url
    url:请求链接
    """
    req_headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "if-none-match": "\"page_cache:51337756828:ProductDetailsController:2ebad7fe90565c09a02da45f4e0a1ace\"",
        "priority": "u=1, i",
        "referer": refererurl,
        "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-ch-viewport-width": "729",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=req_headers, timeout=30)
            return response.json()
        except Exception as e:
            print(f'    请求失败(第{attempt + 1}次): {e}')
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise


def parse_product_info(data):
    """
    解析商品详情页数据
    :param data: 商品详情页 JSON 数据
    :return: 商品详情字典
    """
    name = data.get('title', '')

    # 原价：优先取 compare_at_price，为空则取 price（价格单位为分，需除以 100）
    raw_price = data.get('compare_at_price') or data.get('price') or 0
    price = raw_price / 100

    # 产品图片：拼接 https: 前缀，多张用逗号分割
    images = data.get('images', [])
    image_urls = []
    for img in images:
        if img.startswith('//'):
            image_urls.append('https:' + img)
        elif img.startswith('http'):
            image_urls.append(img)
        else:
            image_urls.append('https://' + img)
    images_str = ','.join(image_urls)

    # 从 description 中提取 Key Ingredients（成分）和 Size（尺码）
    description = data.get('description', '')
    # 先去除所有 HTML 标签，得到纯文本后再提取
    plain_text = re.sub(r'<[^>]+>', ' ', description)
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()

    # 提取 Key Ingredients（到 Size 或换行/结尾为止）
    key_ingredients = ''
    ingredients_match = re.search(
        r'Key\s*Ingredients\s*[:：]\s*(.+?)(?:\s*Size\s*[:：]|\n|$)',
        plain_text, re.IGNORECASE
    )
    if ingredients_match:
        key_ingredients = ingredients_match.group(1).strip()

    # 提取 Size
    size = ''
    size_match = re.search(
        r'Size\s*[:：]\s*(.+?)(?:\n|$)',
        plain_text, re.IGNORECASE
    )
    if size_match:
        size = size_match.group(1).strip()

    # 如果 description 中没有 Size，尝试从 variants 中提取尺码选项
    if not size:
        variants = data.get('variants', [])
        size_options = []
        for v in variants:
            for opt in [v.get('option1'), v.get('option2'), v.get('option3')]:
                if opt and opt != 'Default Title' and opt not in size_options:
                    # 过滤掉包含 HTML/CSS 噪音的选项
                    if not re.search(r'[<>;{}]|rem|px|rgb|font', opt):
                        size_options.append(opt)
        if size_options:
            size = ', '.join(size_options)

    return {
        'name': name,
        'price': price,
        'images': images_str,
        'key_ingredients': key_ingredients,
        'size': size
    }


def save_to_csv(products, filename='products.csv'):
    """
    保存商品数据到 CSV 文件
    :param products: 商品数据列表
    :param filename: CSV 文件名
    """
    fieldnames = ['name', 'price', 'images', 'key_ingredients', 'size']
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    print(f'共保存 {len(products)} 条商品数据到 {filename}')


def main():
    """
    主函数
    """
    all_products = []

    # 遍历 4 页列表
    for page in range(1, 5):
        print(f'正在获取第 {page} 页...')
        try:
            html = get_html(url, page=page)
        except Exception as e:
            print(f'第 {page} 页获取失败: {e}')
            continue

        product_urls = parse_product_list(html)
        print(f'第 {page} 页共解析到 {len(product_urls)} 个商品链接')

        if not product_urls:
            print(f'第 {page} 页没有获取到商品，停止翻页')
            break

        # 遍历商品url列表，构建商品详情页url
        for idx, product_url in enumerate(product_urls):
            product_url_name = product_url.split('/')[-1]
            product_info_refererurl = "https://www.cosrx.com" + product_url
            product_info_url = "https://www.cosrx.com/products/" + product_url_name + ".js"

            print(f'  [{idx + 1}/{len(product_urls)}] 正在获取: {product_url_name}')

            try:
                product_data = get_product_info(product_info_refererurl, product_info_url)
                product_info = parse_product_info(product_data)
                all_products.append(product_info)
                print(f'    名称: {product_info["name"]}, 价格: {product_info["price"]}')
            except Exception as e:
                print(f'    获取失败: {e}')
                continue

            # 请求间隔，避免请求过快被限流
            time.sleep(0.5)

        print(f'已完成第 {page} 页\n')

    # 保存到 CSV
    if all_products:
        save_to_csv(all_products)
    else:
        print('没有获取到任何商品数据')


if __name__ == '__main__':
    main()