from nsga2.problem import Problem
from nsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math

N_TOURIST = 20000
GOV_INCOME = 20000000
SAT_TOURIST = 0.8
SAT_RESIDENT = 0.8
ENV = 0.8
INFRA = 0.8

N_RESIDENT = 30000
N_ENV_BASE = 15000
K_PRICE1 = 0.45  # 票价因子1
K_PRICE2 = 1 - K_PRICE1  # 票价因子2
K_TICKET = 0.55  # 票价因子
K_LIVE = 1 - K_TICKET  # 生活因子
K_COST = 0.4  # 花费因子
K_AD = 0.4  # 广告因子
K_SAT = 1 - K_COST - K_AD  # 满意度因子
K_TOURIST = 0.7  # 游客因子
K_RESIDENT = 1 - K_TOURIST  # 本地居民因子
K_TOURISTENV = 0.5  # 游客影响环境因子
K_TOURISTINFRA = 0.5  # 游客影响基建因子
K_ENV = 0.55  # 环境因子
K_INFRA = 1 - K_ENV  # 基建因子
K_GOVENVCOST = 1 - K_TOURISTENV  # 政府环境支出因子  
K_GOVINFRACOST = 1 - K_TOURISTINFRA  # 政府基建支出因子
K_TOURISTCOSTSAT = 0.45  # 游客花费影响满意度因子
K_RESIDENTCOSTSAT = 0.5  # 居民花费影响满意度因子
K_TOURISTENVINFRASAT = 1 - K_TOURISTCOSTSAT  # 游客环境基建影响满意度因子
K_RESIDENTENVINFRASAT = 1 - K_RESIDENTCOSTSAT  # 居民环境基建影响满意度因子
K_TOURISTSAT = 0.55  # 游客满意度因子
K_RESIDENTSAT = 1 - K_TOURISTSAT  # 居民满意度因子
PRICEBASE1 = 250  # 票价基准1
PRICEBASE2 = 200  # 票价基准2
LIVEBASE = 200  # 生活花费基准
ADBASE = 20  # 广告花费基准
ENVBASE = 25  # 环境花费基准
INFRABASE = 25  # 基建花费基准

N_RATIO_LOWER = 0.2
N_RATIO_UPPER = 2.5
N_RATIO_TURN = 0.7
ENV_RATIO_LOWER = 0.2
ENV_RATIO_UPPER = 1.4
ENV_RATIO_TURN = 0.7
INFRA_RATIO_LOWER = 0.2
INFRA_RATIO_UPPER = 1.6
INFRA_RATIO_TURN = 0.7
AD_ZEROX = 30
ENV_RATIO = 0.3
ENV_ZEROX = ENVBASE / ENV_RATIO


def normalize(basex, basescore, zerox, x):
    if x < basex:
        return (1 - x / basex * (1 - basescore))
    else:
        return max(0, basescore - (x - basex) / (zerox - basex) * basescore)

def twoline(b, turnx, turny, B, x):
    if x < turnx:
        return (b + (x - 0) * (turny - b) / (turnx - 0))
    else:
        return (turny + (x - turnx) * (B - turny) / (1 - turnx))

def FGovIncome(x):
    TicketPrice1 = x[0]  # 门票价格1
    TicketPrice2 = x[1]  # 门票价格2
    TaxResident = x[2]  # 居民税收
    CostTourist = x[3]  # 旅游者成本
    CostResident = x[4]  # 居民成本
    GovCostRatio = x[5]  # 政府成本比例
    GovAdCostRatio = x[6]  # 政府广告成本比例
    GovAd1CostRatio = x[7]  # 政府广告1成本比例
    GovEnvCostRatio = x[8]  # 政府环境成本比例
    
    GovCost = GOV_INCOME * GovCostRatio  # 政府成本
    GovAdCost = GovCost * GovAdCostRatio  # 政府广告总成本
    GovAd2CostRatio = 1 - GovAd1CostRatio  # 政府广告2成本比例
    
    TicketFactor = K_PRICE1 * normalize(PRICEBASE1, 0.95, 1500, TicketPrice1) + K_PRICE2 * normalize(PRICEBASE2, 0.95, 1000, TicketPrice2)  # 0-1
    # print("TicketFactor ==",TicketFactor)
    LiveFactor = normalize(LIVEBASE, 0.95, 1500, CostTourist * (1 + TaxResident))  # 0-1
    # print("CostTourist * (1 + TaxResident) ==",CostTourist * (1 + TaxResident))
    # print("LiveFactor ==",LiveFactor)
    CostFactor = K_TICKET * TicketFactor + K_LIVE * LiveFactor  # 0-1
    # print("CostFactor ==",CostFactor)
    AdFactor = 1 - normalize(ADBASE, 0.85, AD_ZEROX, GovAdCost / N_ENV_BASE)  # 0-1
    # print("GovAdCost / N_ENV_BASE ==",GovAdCost / N_ENV_BASE)
    # print("AdFactor ==",AdFactor)
    NFactor = K_AD * AdFactor + K_COST * CostFactor + K_SAT * SAT_TOURIST  # 0-1
    # print("NFactor ==",NFactor)
    N_Tourist = N_TOURIST * twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor)  # 旅游者数量
    # print("twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor) ==",twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor))
    # print("*********************")

    N_Tourist1 = N_Tourist * GovAd1CostRatio  # 旅游者1数量
    N_Tourist2 = N_Tourist * GovAd2CostRatio  # 旅游者2数量
    GovTicketIncome = N_Tourist1 * TicketPrice1 + N_Tourist2 * TicketPrice2  # 政府门票收入
    GovLiveIncome = (N_Tourist * CostTourist + N_RESIDENT * CostResident) * (1 + TaxResident)  # 政府生活收入
    GovIncome = GovTicketIncome + GovLiveIncome- GovCost  # 政府总收入
    
    return -GovIncome

def FEnvInfra(x):
    TicketPrice1 = x[0]  # 门票价格1
    TicketPrice2 = x[1]  # 门票价格2
    TaxResident = x[2]  # 居民税收
    CostTourist = x[3]  # 旅游者成本
    CostResident = x[4]  # 居民成本
    GovCostRatio = x[5]  # 政府成本比例
    GovAdCostRatio = x[6]  # 政府广告成本比例
    GovAd1CostRatio = x[7]  # 政府广告1成本比例
    GovEnvCostRatio = x[8]  # 政府环境成本比例
    
    GovCost = GOV_INCOME * GovCostRatio  # 政府成本
    GovAdCost = GovCost * GovAdCostRatio  # 政府广告总成本
    GovEnvInfraCost = GovCost * (1 - GovAdCostRatio)  # 政府环境基建成本
    
    TicketFactor = K_PRICE1 * normalize(PRICEBASE1, 0.95, 1500, TicketPrice1) + K_PRICE2 * normalize(PRICEBASE2, 0.95, 1000, TicketPrice2)  # 0-1
    # print("TicketFactor ==",TicketFactor)
    LiveFactor = normalize(LIVEBASE, 0.95, 1500, CostTourist * (1 + TaxResident))  # 0-1
    # print("CostTourist * (1 + TaxResident) ==",CostTourist * (1 + TaxResident))
    # print("LiveFactor ==",LiveFactor)
    CostFactor = K_TICKET * TicketFactor + K_LIVE * LiveFactor  # 0-1
    # print("CostFactor ==",CostFactor)
    AdFactor = 1 - normalize(ADBASE, 0.85, AD_ZEROX, GovAdCost / N_ENV_BASE)  # 0-1
    # print("GovAdCost / N_ENV_BASE ==",GovAdCost / N_ENV_BASE)
    # print("AdFactor ==",AdFactor)
    NFactor = K_AD * AdFactor + K_COST * CostFactor + K_SAT * SAT_TOURIST  # 0-1
    # print("NFactor ==",NFactor)
    N_Tourist = N_TOURIST * twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor)  # 旅游者数量
    # print("twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor) ==",twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor))
    # print("*********************")
    

    GovInfraCostRatio = 1 - GovEnvCostRatio
    GovEnvCost = GovEnvInfraCost * GovEnvCostRatio  # 政府环境支出
    GovInfraCost = GovEnvInfraCost * GovInfraCostRatio  # 政府基建支出
    
    # print("GovEnvCost ==",GovEnvCost)
    # print("GovInfraCost ==",GovInfraCost)
    
    # print("ENV * GovEnvCost / N_ENV_BASE ==", ENV * GovEnvCost / N_ENV_BASE)
    # print("INFRA * GovInfraCost / N_ENV_BASE ==", INFRA * GovInfraCost / N_ENV_BASE)
    
    GovEnvCostFactor = 1 - normalize(ENVBASE, ENV_RATIO, ENV_ZEROX, ENV * GovEnvCost / N_ENV_BASE)  # 0-1
    GovInfraCostFactor = 1 - normalize(INFRABASE, ENV_RATIO, ENV_ZEROX, INFRA * GovInfraCost / N_ENV_BASE)  # 0-1
    
    # print("GovEnvCostFactor ==", GovEnvCostFactor)
    # print("GovInfraCostFactor ==",GovInfraCostFactor)
    
    TouristFactor = normalize(N_ENV_BASE, 0.85, 50000, (N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT))  # 0-1
    
    # print("N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT ==",N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT)
    # print("TouristFactor ==",TouristFactor)
    
    EnvFactor = GovEnvCostFactor * K_GOVENVCOST + TouristFactor * K_TOURISTENV
    
    # print("EnvFactor ==",EnvFactor)
    
    InfraFator = GovInfraCostFactor * K_GOVINFRACOST + TouristFactor * K_TOURISTINFRA
    
    # print("InfraFator ==",InfraFator)
    
    Env = min(ENV * twoline(ENV_RATIO_LOWER, ENV_RATIO_TURN, 1, ENV_RATIO_UPPER, EnvFactor), 1)
    
    # print("Env ==",Env)
    
    Infra = min(INFRA * twoline(INFRA_RATIO_LOWER, INFRA_RATIO_TURN, 1, INFRA_RATIO_UPPER, InfraFator), 1)
    
    # print("Infra ==", Infra)
    
    EnvInfra = Env * K_ENV + Infra * K_INFRA
    
    # print("EnvInfra ==",EnvInfra)
    
    # print("******************")
    
    return -EnvInfra

def FSat(x):
    TicketPrice1 = x[0]  # 门票价格1
    TicketPrice2 = x[1]  # 门票价格2
    TaxResident = x[2]  # 居民税收
    CostTourist = x[3]  # 旅游者成本
    CostResident = x[4]  # 居民成本
    GovCostRatio = x[5]  # 政府成本比例
    GovAdCostRatio = x[6]  # 政府广告成本比例
    GovAd1CostRatio = x[7]  # 政府广告1成本比例
    GovEnvCostRatio = x[8]  # 政府环境成本比例
    
    GovCost = GOV_INCOME * GovCostRatio  # 政府成本
    GovAdCost = GovCost * GovAdCostRatio  # 政府广告总成本
    GovEnvInfraCost = GovCost * (1 - GovAdCostRatio)  # 政府环境基建成本
     
    TicketFactor = K_PRICE1 * normalize(PRICEBASE1, 0.95, 1500, TicketPrice1) + K_PRICE2 * normalize(PRICEBASE2, 0.95, 1000, TicketPrice2)  # 0-1
    # print("TicketFactor ==",TicketFactor)
    LiveFactor = normalize(LIVEBASE, 0.95, 1500, CostTourist * (1 + TaxResident))  # 0-1
    # print("CostTourist * (1 + TaxResident) ==",CostTourist * (1 + TaxResident))
    # print("LiveFactor ==",LiveFactor)
    CostFactor = K_TICKET * TicketFactor + K_LIVE * LiveFactor  # 0-1
    # print("CostFactor ==",CostFactor)
    AdFactor = 1 - normalize(ADBASE, 0.85, AD_ZEROX, GovAdCost / N_ENV_BASE)  # 0-1
    # print("GovAdCost / N_ENV_BASE ==",GovAdCost / N_ENV_BASE)
    # print("AdFactor ==",AdFactor)
    NFactor = K_AD * AdFactor + K_COST * CostFactor + K_SAT * SAT_TOURIST  # 0-1
    # print("NFactor ==",NFactor)
    N_Tourist = N_TOURIST * twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor)  # 旅游者数量
    # print("twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor) ==",twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor))
    # print("*********************")
    
    GovInfraCostRatio = 1 - GovEnvCostRatio
    GovEnvCost = GovEnvInfraCost * GovEnvCostRatio  # 政府环境支出
    GovInfraCost = GovEnvInfraCost * GovInfraCostRatio  # 政府基建支出
    
    # print("GovEnvCost ==",GovEnvCost)
    # print("GovInfraCost ==",GovInfraCost)
    
    # print("ENV * GovEnvCost / N_ENV_BASE ==", ENV * GovEnvCost / N_ENV_BASE)
    # print("INFRA * GovInfraCost / N_ENV_BASE ==", INFRA * GovInfraCost / N_ENV_BASE)
    
    GovEnvCostFactor = 1 - normalize(ENVBASE, ENV_RATIO, ENV_ZEROX, ENV * GovEnvCost / N_ENV_BASE)  # 0-1
    GovInfraCostFactor = 1 - normalize(INFRABASE, ENV_RATIO, ENV_ZEROX, INFRA * GovInfraCost / N_ENV_BASE)  # 0-1
    
    # print("GovEnvCostFactor ==", GovEnvCostFactor)
    # print("GovInfraCostFactor ==",GovInfraCostFactor)
    
    
    TouristFactor = normalize(N_ENV_BASE, 0.85, 50000, (N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT))  # 0-1
    
    # print("N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT ==",N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT)
    
    
    EnvFactor = GovEnvCostFactor * K_GOVENVCOST + TouristFactor * K_TOURISTENV
    
    # print("EnvFactor ==",EnvFactor)
    
    InfraFator = GovInfraCostFactor * K_GOVINFRACOST + TouristFactor * K_TOURISTINFRA
    
    # print("InfraFator ==",InfraFator)
    
    Env = min(ENV * twoline(ENV_RATIO_LOWER, ENV_RATIO_TURN, 1, ENV_RATIO_UPPER, EnvFactor), 1)
    
    # print("Env ==",Env)
    
    Infra = min(INFRA * twoline(INFRA_RATIO_LOWER, INFRA_RATIO_TURN, 1, INFRA_RATIO_UPPER, InfraFator), 1)
    
    # print("Infra ==", Infra)
    
    EnvInfra = Env * K_ENV + Infra * K_INFRA
    
    # print("EnvInfra ==",EnvInfra)
    
    # print("******************")
    
    
    Sat_Tourist = CostFactor * K_TOURISTCOSTSAT + EnvInfra * K_TOURISTENVINFRASAT
    
    # print("Sat_Tourist==",Sat_Tourist)
    
    CostResidentFactor = normalize(LIVEBASE, 0.9, 1000, CostResident * (1 + TaxResident))  # 0-1
    
    # print("CostResidentFactor==",CostResidentFactor)
    
    Sat_Resident = CostResidentFactor * K_RESIDENTCOSTSAT + EnvInfra * K_RESIDENTENVINFRASAT

    # print("Sat_Resident",Sat_Resident)
        
    Sat = Sat_Tourist * K_TOURISTSAT + Sat_Resident * K_RESIDENTSAT
    
    # print("Sat ==",Sat)
    
    # print("********")
    
    return -Sat



for time in range(0, 12):
    problem = Problem(num_of_variables=9, objectives=[FGovIncome, FEnvInfra, FSat], variables_range=[(0.1, 500),(0.1, 500),(0.01, 0.3),(50, 500),(20, 500),(0.01, 0.4),(0.01, 0.99),(0.01, 0.99),(0.01, 0.99)], same_range=False, expand=False)
    evo = Evolution(problem,num_of_generations=100,num_of_individuals=100,mutation_param=20)
    front = evo.evolve()
    x = [i.features for i in front]
    func = [i.objectives for i in front]
    result = []
    for i in range(len(front)):
        if x[i][0] < 500 and x[i][1] < 500 and x[i][3] < 500 and x[i][4] < 500 and func[i][0] < 0 and func[i][1] < -0.5 :
            TicketPrice1 = x[i][0]  # 门票价格1
            TicketPrice2 = x[i][1]  # 门票价格2
            TaxResident = x[i][2]  # 居民税收
            CostTourist = x[i][3]  # 旅游者成本
            CostResident = x[i][4]  # 居民成本
            GovCostRatio = x[i][5]  # 政府成本比例
            GovAdCostRatio = x[i][6]  # 政府广告成本比例
            GovAd1CostRatio = x[i][7]  # 政府广告1成本比例
            GovEnvCostRatio = x[i][8]  # 政府环境成本比例
        
            GovCost = GOV_INCOME * GovCostRatio  # 政府成本
            GovAdCost = GovCost * GovAdCostRatio  # 政府广告总成本
            GovAd2CostRatio = 1 - GovAd1CostRatio  # 政府广告2成本比例
            GovEnvInfraCost = GovCost * (1 - GovAdCostRatio)  # 政府环境基建成本
            TicketFactor = K_PRICE1 * normalize(PRICEBASE1, 0.95, 1500, TicketPrice1) + K_PRICE2 * normalize(PRICEBASE2, 0.95, 1000, TicketPrice2)  # 0-1
            LiveFactor = normalize(LIVEBASE, 0.95, 1500, CostTourist * (1 + TaxResident))  # 0-1
            CostFactor = K_TICKET * TicketFactor + K_LIVE * LiveFactor  # 0-1
            AdFactor = 1 - normalize(ADBASE, 0.85, AD_ZEROX, GovAdCost / N_ENV_BASE)  # 0-1
            NFactor = K_AD * AdFactor + K_COST * CostFactor + K_SAT * SAT_TOURIST  # 0-1
            N_Tourist = N_TOURIST * twoline(N_RATIO_LOWER, N_RATIO_TURN, 1, N_RATIO_UPPER, NFactor)  # 旅游者数量
            N_Tourist1 = N_Tourist * GovAd1CostRatio  # 旅游者1数量
            N_Tourist2 = N_Tourist * GovAd2CostRatio  # 旅游者2数量
            GovTicketIncome = N_Tourist1 * TicketPrice1 + N_Tourist2 * TicketPrice2  # 政府门票收入
            GovLiveIncome = (N_Tourist * CostTourist + N_RESIDENT * CostResident) * (1 + TaxResident)  # 政府生活收入
            GovIncome = GovTicketIncome + GovLiveIncome- GovCost  # 政府总收入
            GovInfraCostRatio = 1 - GovEnvCostRatio
            GovEnvCost = GovEnvInfraCost * GovEnvCostRatio  # 政府环境支出
            GovInfraCost = GovEnvInfraCost * GovInfraCostRatio  # 政府基建支出
            GovEnvCostFactor = 1 - normalize(ENVBASE, ENV_RATIO, ENV_ZEROX, ENV * GovEnvCost / N_ENV_BASE)  # 0-1
            GovInfraCostFactor = 1 - normalize(INFRABASE, ENV_RATIO, ENV_ZEROX, INFRA * GovInfraCost / N_ENV_BASE)  # 0-1
            TouristFactor = normalize(N_ENV_BASE, 0.85, 50000, (N_Tourist * K_TOURIST + N_RESIDENT * K_RESIDENT))  # 0-1
            EnvFactor = GovEnvCostFactor * K_GOVENVCOST + TouristFactor * K_TOURISTENV
            InfraFator = GovInfraCostFactor * K_GOVINFRACOST + TouristFactor * K_TOURISTINFRA
            Env = min(ENV * twoline(ENV_RATIO_LOWER, ENV_RATIO_TURN, 1, ENV_RATIO_UPPER, EnvFactor), 1)
            Infra = min(INFRA * twoline(INFRA_RATIO_LOWER, INFRA_RATIO_TURN, 1, INFRA_RATIO_UPPER, InfraFator), 1)
            EnvInfra = Env * K_ENV + Infra * K_INFRA
            Sat_Tourist = CostFactor * K_TOURISTCOSTSAT + EnvInfra * K_TOURISTENVINFRASAT
            CostResidentFactor = normalize(LIVEBASE, 0.9, 1000, CostResident * (1 + TaxResident))  # 0-1
            Sat_Resident = CostResidentFactor * K_RESIDENTCOSTSAT + EnvInfra * K_RESIDENTENVINFRASAT
            Sat = Sat_Tourist * K_TOURISTSAT + Sat_Resident * K_RESIDENTSAT
            if Env > 0.5 and Infra > 0.5:
                result.append([i, -GovIncome, -EnvInfra, -Sat, -N_Tourist, -Env, -Infra, -Sat_Tourist, -Sat_Resident])
                # with open('./t2.txt','a') as file:
                #     print(i, file=file) 
                #     print(x[i], file=file)
                #     print(func[i], file=file)
                #     print("N_Tourist ==", N_Tourist, file=file)
                #     print("GovIncome ==", GovIncome, file=file)
                #     print("Env ==", Env, file=file)
                #     print("Infra ==", Infra, file=file)
                #     print("Sat_Tourist ==", Sat_Tourist, file=file)
                #     print("Sat_Resident ==", Sat_Resident, file=file)
                #     print('***********\n', file=file)
                
    KEY = 2
    result.sort(key=lambda x : x[KEY])
    i = result[0][0]
    for j in range(len(result)):
        print(result[j][KEY])
        
    with open('./t2.txt','a') as file:
        print('****************************', file = file)
        
        print("time ==", time, file = file)
        TicketPrice1 = x[i][0]  # 门票价格1
        TicketPrice2 = x[i][1]  # 门票价格2
        TaxResident = x[i][2]  # 居民税收
        CostTourist = x[i][3]  # 旅游者成本
        CostResident = x[i][4]  # 居民成本
        GovCostRatio = x[i][5]  # 政府成本比例
        GovAdCostRatio = x[i][6]  # 政府广告成本比例
        GovAd1CostRatio = x[i][7]  # 政府广告1成本比例
        GovEnvCostRatio = x[i][8]  # 政府环境成本比例
        print('----------------------------', file = file)
        print(f"TicketPrice1: {TicketPrice1}", file = file)
        print(f"TicketPrice2: {TicketPrice2}", file = file)
        print(f"TaxResident: {TaxResident}", file = file)
        print(f"CostTourist: {CostTourist}", file = file)
        print(f"CostResident: {CostResident}", file = file)
        print(f"GovCostRatio: {GovCostRatio}", file = file)
        print(f"GovAdCostRatio: {GovAdCostRatio}", file = file)
        print(f"GovAd1CostRatio: {GovAd1CostRatio}", file = file)
        print(f"GovEnvCostRatio: {GovEnvCostRatio}", file = file)
        print('----------------------------', file = file)
        print("GovIncome ==", -result[0][1], file=file)
        print("EnvInfra ==", -result[0][2], file=file)
        print("Sat ==", -result[0][3], file=file)
        print('----------------------------', file = file)
        print("N_Tourist ==", -result[0][4], file=file)
        print("GovIncome ==", -result[0][1], file=file)
        print("Env ==", -result[0][5], file=file)
        print("Infra ==", -result[0][6], file=file)
        print("Sat_Tourist ==", -result[0][7], file=file)
        print("Sat_Resident ==", -result[0][8], file=file)
        print('----------------------------', file = file)
        print('****************************\n', file=file)
        
    GOV_INCOME = -result[0][1]
    N_TOURIST = -result[0][4]
    ENV = -result[0][5]
    INFRA = -result[0][6]
    SAT_TOURIST = -result[0][7]
    SAT_RESIDENT = -result[0][8]


# for i in func:
#     if i[0] < 16000 and i[1] < 0 and i[2] < 0 and i[3] < 500 and i[4] < 300 and i[4] < i[3]:
#         # 输出到txt文件
#         with open('output.txt', 'a') as f:
#             f.write(str(i) + '\n')

# function1 = [i[0] for i in func]
# function2 = [i[1] for i in func]
# plt.xlabel('Function 1', fontsize=15)
# plt.ylabel('Function 2', fontsize=15)
# plt.scatter(function1, function2)
# plt.show()
