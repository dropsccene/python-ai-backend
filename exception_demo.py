 # 写一个 try/except，里面做 1/0，捕获 ZeroDivisionError 并 print 一句话
try:
   result = 1/0
except ZeroDivisionError as e:
    print("捕获到异常：", e)

# 写一个 try/except，访问字典里不存在的 key，捕获 KeyError 并 print 一句话
try :
    my_dict = {"a":1,"b":2}
    print(my_dict["c"])
except KeyError as e :
    print("捕获到异常：", e)

# 写一个 try/except，把字符串和整数相加，捕获 TypeError 并 print 一句话
try :
    result = "string" + 123
except TypeError as e :
    print("捕获到异常：", e)

# try/except/else — else 只在 try 没抛异常时执行

try :
    result = 1 + 1
except Exception as e :
    print("捕获到异常：", e)
else :
    print("没有异常，结果是：", result)

# else 在有异常时不执行
try :
    result = 1 / 0
except ZeroDivisionError as e :
    print("捕获到异常：", e)
else :
    print("没有异常，结果是：", result)

# finally 在没异常时也执行
try :
    result = 1 + 1
except Exception as e :
    print("捕获到异常：", e)
finally :
    print("没异常,但finally 还是会执行这句话")

# try/except/finally — finally 无论是否抛异常都执行
try :
    result = 1 / 0
except ZeroDivisionError as e :
    print("捕获到异常：", e)
finally :
    print("无论如何都会执行这句话")


# 四件套 try/except/else/finally
try :
    result = 1 / 0
except ZeroDivisionError as e :
    print("捕获到异常：", e)
else :
    print("没有异常，结果是：", result)
finally :
    print("无论如何都会执行这句话")

# 自定义异常
class TaskNotFoundError(Exception):
    pass

try :
    raise TaskNotFoundError("任务未找到")
except TaskNotFoundError as e :
    print("捕获到自定义异常：", e)