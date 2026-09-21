# 爬虫开发岗位 - 面试题答案

本仓库包含长沙智拓无界信息科技有限公司爬虫开发岗位面试题的完整答案。

## 题目列表

| 题号 | 文件 | 说明 |
|------|------|------|
| 第1题 | `demo01.py` | 爬取 Roark 产品页信息（名称、价格、图片、颜色、尺码） |
| 第2题 | `demo02.py` | 爬取 COSRX 全部商品数据并保存为 CSV |
| 第3题 | `demo03.py` | 爬取 Quest Nutrition JSON 接口数据并保存为 CSV |
| 第4题 | `demo04.py` | 三种方法去除列表重复元素并保持顺序 |
| 第5题 | `demo05.py` | 猿人学第19题 |

## 数据文件

| 文件 | 说明 |
|------|------|
| `products.csv` | 第2题爬取的 COSRX 商品数据 |
| `quest_products.csv` | 第3题爬取的 Quest Nutrition 产品数据 |
| `img.png` | 第5题运行成功的截图 |

## 运行环境

- Python 3.12
- requests
- lxml

## 运行方式

```bash
pip install requests lxml
python demo01.py
python demo02.py
python demo03.py
python demo04.py
python demo05.py
```
