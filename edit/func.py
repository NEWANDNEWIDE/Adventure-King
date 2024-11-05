func_d = {}
"""
此处用来编写按钮的响应函数， 每一个函数定义体后接上func_d[name]=func
其中name是为了方便查找函数的自定义名字，func是函数体
例如:
    func(a, b):
        return a+b
    func_d["add"]=func
    
当界面中的按钮响应:
    #假定储存按钮参数的列表是button_list
    button_list[i]定义了三个变量list[bool, tuple(rect:tuple, size:tuple), func_name:str]
    调用时则会:
        func_d[button_list[i][2]](*args)
    例如:
        button_list.append([True, ((0, 0), (50, 50)), "add"]) #源代码在button.Button的bind函数里
        响应时则会:
        func_d[button_list[1][2]](1, 1) #button_list[0]储存的是按钮的数量
"""


def func(a, b):
    return a + b


func_d["add"] = func
