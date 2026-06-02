import sys
# 函数定义时给参数一个默认值，调用时可以不传
def add_item(item,items=none):
    if items is None:
        items = []
    else:
        items.append(item)
    return items

print(add_item('apple'))
print(add_item('banana'))

# *args 把调用时多出来的位置参数打包成一个 tuple
def sum_all(*numbers):
    number_sum = 0
    for number in numbers:
        number_sum += number
    return number_sum

# **kwargs 把调用时多出来的关键字参数打包成一个 dict
def describe(**info):
    print(info)

describe(name='Alice', age=30, city='New York')


# 匿名函数：lambda 参数: 返回值表达式。只能用一行表达式，不能有语句
print(sorted([{"name":"c"},{"name":"a"}], key=lambda x: x["name"]))

# 列表推导式 [x*2 for x in range(n)] 一次性生成全部数据占内存。
# 生成器表达式 (x*2 for x in range(n))每次只产出一个值，省内存
print(sys.getsizeof([x*2 for x in range(1000)])) # 列表占用内存
print(sys.getsizeof((x*2 for x in range(1000)))) # 生成器占用内存