# list列表 - 有序、可变的序列

nums = [3,1,4,1,5,9]
# 在末尾添加元素2
nums.append(2)
print(nums)  # 输出: [3, 1, 4, 1, 5, 9, 2]
# 取第0个元素
print(nums[0])  # 输出: 3
# 取最后一个元素
print(nums[-1])  # 输出: 2
# 取索引1到3的元素（不包括索引3）
print(nums[1:3])  # 输出: [1, 4]
# 取长度
len(nums)  # 输出: 7
# 在索引0插入元素6
nums.insert(0, 6)
print(nums)  # 输出: [6, 3, 1, 1, 5, 9, 2]
# 删除索引2的元素
nums.pop(2)
print(nums)  # 输出: [6, 3, 1, 5, 9, 2]
# 进行从升序排序
nums.sort()
print(nums)  # 输出: [1, 1, 2, 3, 5, 6, 9]

# dict字典 - 键值对、O(1)查找
person = {"name":"张三","age":25}
# 取值
print(person["name"])  # 输出: 张三
# 新增 Key
person["gender"] = "男"
print(person)  # 输出: {'name': '张三', 'age': 25, 'gender': '男'}
# 取键
print(person.keys())  # 输出: dict_keys
# 取值
print(person.values())  # 输出: dict_values
# 取键值对
print(person.items())
# 安全取值，没有就返回默认值None
print(person.get("hobby"))
# 检查键是否存在
"name" in person  # 输出: True

# set集合 - 无序、唯一的元素集合
a = {1,2,3}
b = {3,4,5}
# 并集
print(a|b)  # 输出: {1, 2, 3, 4, 5}
# 交集
print(a&b) # 输出: {3}
# 差集
print(a-b) # 输出: {1, 2}
# 添加元素
print(a.add(6))  # 输出: {1, 2, 3, 6}  

# tuple元组 - 有序、不可变的序列
point = (3,4)
# 取第0个元素
print(point[0])  # 输出: 3
# 取最后一个元素
print(point[-1])  # 输出: 4
try:
    # 尝试修改元素
    point[0] = 5
except TypeError as e:
    print(e)  # 输出: 'tuple' object does not support item assignment

# 列表推导式
# 输出: [0, 3, 6, 9]
print([x for x in range(10) if x % 3 == 0])