from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math

N_TOURIST = 20000
N_RESIDENT = 30000
N_ENVBASE = 8000
N_GOVBASE = 10000



def func1(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    N_tourist = N_TOURIST  # 游客总人数
    N_env_base = N_ENVBASE  # 平衡环境游客基数

    Ad = Ad_g + Ad_other  # 总宣传费用
    N_tourist_g = N_tourist * (Ad_g/Ad)  # 冰川游客人数
    N_tourist_other = N_tourist * (Ad_other / Ad)  # 其他景点人数

    k_env_g = 0.7  # 冰川景点的环境影响因子 归一化
    k_env_other = 0.3  # 其余景点的环境影响因子
    k_env = 0.6  # 环境的影响因子
    Fenv = k_env *(k_env_g * N_tourist_g + k_env_other * N_tourist_other - N_env_base)  # 人数
    
    return Fenv

def func2(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    N_tourist = N_TOURIST  # 游客总人数
    N_env_base = N_ENVBASE  # 平衡环境游客基数
    N_resident = N_RESIDENT  # 本地人数

    Ad = Ad_g + Ad_other  # 总宣传费用
    N_tourist_g = N_tourist * (Ad_g/Ad)  # 冰川游客人数
    N_tourist_other = N_tourist * (Ad_other / Ad)  # 其他景点人数

    Feco = (N_tourist_g * Ticket_g + N_tourist_other * Ticket_other) * Tax_tourist + (N_tourist * Cost_tourist_other + N_resident * Cost_resident) * Tax_other - Ad * N_env_base  # 政府收入每天

    return -Feco

def func3(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    N_tourist = N_TOURIST  # 游客总人数
    N_gov_base = N_GOVBASE  # 平衡基础设施游客基数
    N_resident = N_RESIDENT  # 本地人数
    N_tot = N_tourist + N_resident  # 总人数

    k_gov = 0.4  # 政府基建影响因子
    Fgov = k_gov * (N_tot - N_gov_base)  # 人数

    return Fgov

def func4(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    N_tourist = N_TOURIST  # 游客总人数

    Ad = Ad_g + Ad_other  # 总宣传费用
    N_tourist_g = N_tourist * (Ad_g/Ad)  # 冰川游客人数
    N_tourist_other = N_tourist * (Ad_other / Ad)  # 其他景点人数

    Ftourist = (N_tourist_g * Ticket_g + N_tourist_other * Ticket_other) * (1 + Tax_tourist) + (N_tourist * Cost_tourist_other) * (1 + Tax_other)
    Ftourist = Ftourist / N_tourist  # 游客人均支出每天

    return Ftourist

def func5(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    N_tourist = N_TOURIST  # 游客总人数
    N_resident = N_RESIDENT  # 本地人数

    Ad = Ad_g + Ad_other  # 总宣传费用
    N_tourist_g = N_tourist * (Ad_g/Ad)  # 冰川游客人数
    N_tourist_other = N_tourist * (Ad_other / Ad)  # 其他景点人数

    Fcomp = N_tourist_g * Ticket_g + N_tourist_other * Ticket_other + N_tourist * Cost_tourist_other + N_resident * Cost_resident  # 企业收入每天
    return -Fcomp

def func6(arr):
    Tax_tourist = arr[0]  # 游客税 百分比
    Tax_other = arr[1]  # 其他税 百分比
    Ticket_g = arr[2]  # 游客冰川门票花费 单个人
    Ticket_other = arr[3]  # 游客其他景点门票花费 单个人
    Cost_tourist_other = arr[4]  # 游客其余花费 单个人
    Cost_resident = arr[5]  # 本地花费 单个人
    Ad_g = arr[6]  # 冰川宣传花费
    Ad_other = arr[7]  # 其余景点宣传花费

    Fres = Cost_resident * (1 + Tax_other)  # 居民人均支出每天
    return Fres




problem = Problem(num_of_variables=8, objectives=[func1, func2, func3, func4, func5, func6], variables_range=[(0.1, 0.5),(0.1, 0.5),(20, 1000),(20, 1000),(20, 1000),(20, 1000),(0.1,500),(0.1,500)], same_range=False, expand=False)
evo = Evolution(problem,num_of_generations=500,num_of_individuals=500,mutation_param=20)
func = [i.objectives for i in evo.evolve()]
for i in func:
    if i[1] < 0 and i[4] < 0 and i[3] < 1000 and i[5] < i[3] and i[0] < 0:
        print(i)

# function1 = [i[0] for i in func]
# function2 = [i[1] for i in func]
# plt.xlabel('Function 1', fontsize=15)
# plt.ylabel('Function 2', fontsize=15)
# plt.scatter(function1, function2)
# plt.show()
