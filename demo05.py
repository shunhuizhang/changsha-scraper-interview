"""
第 5 题： 完成“猿人学”第 19 题，提交程序代码并保存运行成功的截图。 链接： https://match.yuanrenxue.cn/match/19
"""
import requests

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://match.yuanrenxue.cn/match/19",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "c833cqo4tvjsv7dyl17hnyn8apdghumr"
}
res_list = []

url = "https://match.yuanrenxue.cn/api/question/19"
for i in range(1, 6):
    if i == 5:
        headers['user-agent'] = 'yuanrenxue'
    params = {
        "page": str(i),
        "pageSize": "10",
        "kw": ""
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    response_json = response.json()
    data_list = response_json["data"]
    res_list += data_list
    print(data_list)
print(sum(res_list))
