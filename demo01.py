"""
第 1 题： 使用 requests 库爬取以下链接中的产品名称 (name)、原价 (price)、产品图片 (images)、当前选中的颜色名称 (Color) 以及尺码选项 (Size)。能够在控制台中打印结果即可。 链接： https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print
"""
import re
import requests
from lxml import etree

# 请求头
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-viewport-width": "592",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
}

def get_product_info(url):
    """
    获取网页源码
    :param url: 产品链接
    :return: 网页源码
    """
    response = requests.get(url, headers=headers)
    return response.text

def parse_product_info(html):
    """
    解析网页源码
    :param html: 网页源码
    :return: 产品信息
    """
    tree = etree.HTML(html)

    # 商品名称
    name = tree.xpath("//html//div[@class='product-header__title type-headline my-0']/text()")[0].strip()
    print("名称:", name)

    # 原价
    price = tree.xpath('//meta[@property="og:price:amount"]/@content')[0]
    print("价格: $", price)

    # 从 <script product-data> 中提取颜色和尺码（JSON 混有 JS 语法，用正则提取）
    script_text = tree.xpath('//script[@product-data]/text()')[0]

    # 当前选中颜色
    color_match = re.search(r'"color"\s*:\s*"([^"]*)"', script_text)
    color = color_match.group(1) if color_match else ''
    print("颜色:", color)

    # 尺码选项
    size_match = re.search(
        r'"name":\s*"Size".*?"values":\s*\[(.*?)\]',
        script_text, re.DOTALL
    )
    size_list = []
    if size_match:
        size_list = re.findall(r'"([^"]*)"', size_match.group(1))
    print("尺码选项:", size_list)

    # 图片链接
    images = tree.xpath("//meta[@property='og:image']/@content")[0]
    if images:
        print("图片链接:", images)


def main():
    """
    主函数
    """
    # 产品链接
    url = 'https://roark.com/products/mens-bless-up-breathable-stretch-shirt-fossil-print'
    # 获取网页源码
    html = get_product_info(url)
    # 解析网页源码
    parse_product_info(html)

if __name__ == '__main__':
    main()