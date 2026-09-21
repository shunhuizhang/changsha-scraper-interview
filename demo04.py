"""
第 4 题： 给定一个包含重复元素的列表 [3, 1, 2, 3, 4, 1, 2]，请使用 三种不同 的方法去除重复的元素，同时保持元素原本的出现顺序。结果在控制台打印即可。
"""
data = [3, 1, 2, 3, 4, 1, 2]

# 方法一
def dedupe_by_dict_record(items):
    seen = {}
    result = []
    for item in items:
        if item not in seen:
            seen[item] = True   # 用字典记录已经出现过的元素
            result.append(item)
    return result

# 方法二
def dedupe_by_set(items):
    return list(set(items))


# 方法三
def dedupe_by_dict(items):
    return list(dict.fromkeys(items))


print("原列表：", data)
print("方法一：", dedupe_by_dict_record(data))
print("方法二：", dedupe_by_set(data))
print("方法三：", dedupe_by_dict(data))