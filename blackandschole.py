from datetime import datetime, date, time
import math
import scipy.stats as stats
import py_vollib.black_scholes.implied_volatility as iv
from scipy.stats import norm


#Colocar variables para los casos
#1
#precio del activo subyacente
spot = 3907.25
# Precio Strike 
strike = 3830
#precio de la opcion
target = 1.55

#2
#precio del activo subyacente
spot2 = 3907.25
# Precio Strike 
strike2 = strike1 = 3810
#precio de la opcion
target2 = 3.8
# Fecha de expiracion 
fecha_exp = date(2023 , 3, 11)

#caso 3
#precio del activo subyacente
spot3 = 3907.25
# Precio Strike 
strike3 = 3995
#precio de la opcion
target3 = 0.6

#caso 4
#precio del activo subyacente
spot4 = 3907.25
# Precio Strike 
strike4 = 4015
#precio de la opcion
target4 = 1.15


# Dividendo
dividend = 0.0000001  # Dividendo
#tasa de interes libre de riesgo
risk_free = 0.0027
# Crear variable con la fecha de hoy
#hoy = date.today()
hoy = date(2023 , 3, 10)
# Crear variable con una hora específica (por ejemplo, las 15:30)
hora_exacta = time(10, 30)
# Combinar la fecha y la hora en un objeto datetime
fecha_y_hora = datetime.combine(hoy, hora_exacta)
# Convertir el objeto datetime a un timestamp
timestamp = datetime.timestamp(fecha_y_hora)

# Crear una nueva hora específica para fecha de vencimiento
hora_especifica = time(16, 00)

# Combinar la fecha y la hora especificas en un objeto datetime
fecha_y_hora1 = datetime.combine(hoy, hora_especifica)


#fecha_exp =
# Combinar la fecha y la hora especificas  de fecha de vencimiento en un objeto datetime
fecha_y_hora2 = datetime.combine(fecha_exp, hora_especifica)

# Convertir el objeto datetime2 a un timestamp
maturity2 = datetime.timestamp(fecha_y_hora2)

# Convertir el objeto datetime a un timestamp
maturity = datetime.timestamp(fecha_y_hora1)


#CASO 1


#Sell/Buy
sell_buy = "BTO"
#Volumen 1 o -1
volumen = 1
#Type p o c
option_type = "p"


time = time2 =  (maturity - timestamp) / (365 * 24 * 60 * 60)

# calcular el iv
def d_one(volatility):
    return (math.log(spot / strike) + (risk_free - dividend + 0.5 * volatility ** 2) * time) / (volatility * math.sqrt(time))

def nd_one(volatility):
    return math.exp(-(d_one(volatility) ** 2) / 2) / (math.sqrt(2 * math.pi))

def d_two(volatility):
    return d_one(volatility) - volatility * math.sqrt(time)

def nd_two(volatility):
    return stats.norm.cdf(d_two(volatility))

def call_option(volatility):
    return math.exp(-dividend * time) * spot * stats.norm.cdf(d_one(volatility)) - strike * math.exp(-risk_free * time) * stats.norm.cdf(d_two(volatility))

def put_option(volatility):
    return strike * math.exp(-risk_free * time) * stats.norm.cdf(-d_two(volatility)) - math.exp(-dividend * time) * spot * stats.norm.cdf(-d_one(volatility))

def implied_put_volatility():
    high = 5.0
    low = 0.0
    mid = (high + low) / 2.0

    while (high - low) > 0.000001:
        if put_option(mid) > target:
            high = mid
        else:
            low = mid
        mid = (high + low) / 2.0

    return mid

# Calculation
standard_deviation = implied_put_volatility()
##print(f"The implied volatility for the Put option is: {standard_deviation * 100}%")

#Calculo de las griegas

# Variables a asignar
style = "European"
direction = "Buy"
call_put = "Put"

def calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation):
    dt = standard_deviation * math.sqrt(T)
    d1 = (math.log(spot / strike) + (risk_free - dividend + (standard_deviation ** 2 / 2)) * T) / dt
    d2 = d1 - dt
    return d1, d2

def delta():
    T = time
    d1, d2 = calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation)
    Nd1 = stats.norm.cdf(d1)

    if call_put == "Call":
        return math.exp(-dividend * T) * Nd1
    else:
        return math.exp(-dividend * T) * (Nd1 - 1)

def gamma():
    T = time
    d1, _ = calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation)

    return (math.exp(-dividend * T) / (spot * standard_deviation * math.sqrt(T))) * (1 / math.sqrt(2 * math.pi)) * math.exp(-(d1 ** 2) / 2)

def theta():
    T = time
    d1, d2 = calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation)
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return 1 / 365 * (-(spot * standard_deviation * math.exp(-dividend * T) / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) - risk_free * strike * math.exp(-risk_free * T) * Nd2 + dividend * spot * math.exp(-dividend * T) * Nd1)
    else:
        Nmind1 = stats.norm.cdf(-d1)
        Nmind2 = stats.norm.cdf(-d2)

        return 1 / 365 * (-(spot * standard_deviation * math.exp(-dividend * T) / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) + risk_free * strike * math.exp(-risk_free * T) * Nmind2 - dividend * spot * math.exp(-dividend * T) * Nmind1)

def vega():
    T = time
    d1, _ = calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation)

    return 1 / 100 * spot * math.exp(-dividend * T) * math.sqrt(T) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)

def rho():
    T = time
    _, d2 = calculate_d1_d2(T, spot, strike, risk_free, dividend, standard_deviation)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return (1 / 100) * (strike * T * math.exp(-risk_free * T)) * Nd2
    else:
        Nmind2 = stats.norm.cdf(-d2)

        return -(1 / 100) * (strike * T * math.exp(-risk_free * T)) * Nmind2

##print(delta())
##print(gamma())
##print(theta())
##print(vega())
##print(rho())

#Caso 2

#Sell/Buy
sell_buy1 = "STO"
#Volumen 1 o -1
volumen2 = -1
#Type p o c
option_type = "p"

# Nueva variable de tiempo
time1 = (maturity2 - timestamp) / (365 * 24 * 60 * 60)

def d_one_new(volatility2):
    return (math.log(spot2 / strike2) + (risk_free - dividend + 0.5 * volatility2 ** 2) * time1) / (volatility2 * math.sqrt(time1))

def nd_one_new(volatility2):
    return math.exp(-(d_one_new(volatility2) ** 2) / 2) / (math.sqrt(2 * math.pi))

def d_two_new(volatility2):
    return d_one_new(volatility2) - volatility2 * math.sqrt(time1)

def nd_two_new(volatility2):
    return stats.norm.cdf(d_two_new(volatility2))

def call_option_new(volatility2):
    return math.exp(-dividend * time1) * spot2 * stats.norm.cdf(d_one_new(volatility2)) - strike2 * math.exp(-risk_free * time1) * stats.norm.cdf(d_two_new(volatility2))

def put_option_new(volatility2):
    return strike2 * math.exp(-risk_free * time1) * stats.norm.cdf(-d_two_new(volatility2)) - math.exp(-dividend * time1) * spot2 * stats.norm.cdf(-d_one_new(volatility2))

def implied_put_volatility_new():
    high = 5.0
    low = 0.0
    mid = (high + low) / 2.0

    while (high - low) > 0.000001:
        if put_option_new(mid) > target2:  
            high = mid
        else:
            low = mid
        mid = (high + low) / 2.0

    return mid

standard_deviation2 = implied_put_volatility_new()
##print(f"The implied volatility for the Put option is: {standard_deviation2 * 100}%")

#Calculo de las griegas

# Variables a asignar
style = "European"
direction = "Sell"
call_put = "Put"

def calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2):
    dt = standard_deviation2 * math.sqrt(T)
    d1 = (math.log(spot2 / strike1) + (risk_free - dividend + (standard_deviation2 ** 2 / 2)) * T) / dt
    d2 = d1 - dt
    return d1, d2

def delta2():
    T = time1
    d1, d2 = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)
    Nd1 = stats.norm.cdf(d1)

    if call_put == "Call":
        return math.exp(-dividend * T) * Nd1 * volumen2
    else:
        return math.exp(-dividend * T) * (Nd1 - 1) * volumen

def gamma2():
    T = time1
    d1, _ = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)

    return (math.exp(-dividend * T) * volumen2 / (spot2 * standard_deviation2 * math.sqrt(T))) * (1 / math.sqrt(2 * math.pi)) * math.exp(-(d1 ** 2) / 2)

def theta2():
    T = time1
    d1, d2 = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return 1 / 365 * (-(spot2 * standard_deviation2 * math.exp(-dividend * T) * volumen2 / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) - risk_free * strike1 * math.exp(-risk_free * T) * Nd2 + dividend * spot2 * math.exp(-dividend * T) * Nd1)
    else:
        Nmind1 = stats.norm.cdf(-d1)
        Nmind2 = stats.norm.cdf(-d2)

        return 1 / 365 * (-(spot2 * standard_deviation2 * math.exp(-dividend * T) * volumen / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) + risk_free * strike1 * math.exp(-risk_free * T) * Nmind2 - dividend * spot2 * math.exp(-dividend * T) * Nmind1)

def vega2():
    T = time1
    d1, _ = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)

    return 1 / 100 * spot2 * math.exp(-dividend * T) * volumen * math.sqrt(T) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)

def rho2():
    T = time1
    _, d2 = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return (1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nd2
    else:
        Nmind2 = stats.norm.cdf(-d2)

        return -(1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nmind2 * volumen2

##print(delta2())
##print(gamma2())
##print(theta2())
##print(vega2())
##print(rho2())

#caso 3

#Sell/Buy
sell_buy = "BTO"
#Volumen 1 o -1
volumen3 = 1
#Type p o c
option_type3 = "c"

def d_one_new3(volatility3):
    return (math.log(spot3 / strike3) + (risk_free - dividend + 0.5 * volatility3 ** 2) * time2) / (volatility3 * math.sqrt(time2))

def nd_one_new3(volatility3):
    return math.exp(-(d_one_new3(volatility3) ** 2) / 2) / (math.sqrt(2 * math.pi))

def d_two_new3(volatility3):
    return d_one_new3(volatility3) - volatility3 * math.sqrt(time2)

def nd_two_new3(volatility3):
    return stats.norm.cdf(d_two_new3(volatility3))

def call_option_new3(volatility3):
    return math.exp(-dividend * time2) * spot3 * stats.norm.cdf(d_one_new3(volatility3)) - strike3 * math.exp(-risk_free * time2) * stats.norm.cdf(d_two_new3(volatility3))

def put_option_new3(volatility3):
    return strike3 * math.exp(-risk_free * time2) * stats.norm.cdf(-d_two_new3(volatility3)) - math.exp(-dividend * time2) * spot3 * stats.norm.cdf(-d_one_new3(volatility3))

def implied_call_volatility_new3():
    high = 5.0
    low = 0.0
    mid = (high + low) / 2.0

    while (high - low) > 0.000001:
        if call_option_new3(mid) > target3:  
            high = mid
        else:
            low = mid
        mid = (high + low) / 2.0

    return mid

standard_deviation3 = implied_call_volatility_new3()
##print(f"The implied volatility for the Call option is: {standard_deviation3 * 100}%")

#Calculo de las griegas

# Variables a asignar
style = "European"
direction3 = "Buy"
call_put3 = "Call"

def calculate_d1_d2_3(T, spot3, strike3, risk_free, dividend, standard_deviation3):
    dt = standard_deviation3 * math.sqrt(T)
    d1 = (math.log(spot3 / strike3) + (risk_free - dividend + (standard_deviation3 ** 2 / 2)) * T) / dt
    d2 = d1 - dt
    return d1, d2

def delta3():
    T = time
    d1, d2 = calculate_d1_d2_3(T, spot3, strike3, risk_free, dividend, standard_deviation3)
    Nd1 = stats.norm.cdf(d1)

    if call_put3 == "Call":
        return math.exp(-dividend * T) * Nd1 * volumen
    else:
        return math.exp(-dividend * T) * (Nd1 - 1) * volumen
    

def gamma3():
    T = time
    d1, _ = calculate_d1_d2_3(T, spot3, strike3, risk_free, dividend, standard_deviation3)

    return (math.exp(-dividend * T) * volumen / (spot2 * standard_deviation3 * math.sqrt(T))) * (1 / math.sqrt(2 * math.pi)) * math.exp(-(d1 ** 2) / 2)

def theta3():
    T = time
    d1, d2 = calculate_d1_d2_3(T, spot3, strike3, risk_free, dividend, standard_deviation3)
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)

    if call_put3 == "Call":
        return 1 / 365 * (-(spot3 * standard_deviation3 * math.exp(-dividend * T) * volumen / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) - risk_free * strike3 * math.exp(-risk_free * T) * Nd2 + dividend * spot3 * math.exp(-dividend * T) * Nd1)
    else:
        Nmind1 = stats.norm.cdf(-d1)
        Nmind2 = stats.norm.cdf(-d2)

        return 1 / 365 * (-(spot3 * standard_deviation3 * math.exp(-dividend * T) * volumen / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) + risk_free * strike3 * math.exp(-risk_free * T) * Nmind2 - dividend * spot3 * math.exp(-dividend * T) * Nmind1)

def vega3():
    T = time
    d1, _ = calculate_d1_d2_3(T, spot3, strike3, risk_free, dividend, standard_deviation3)

    return 1 / 100 * spot3 * math.exp(-dividend * T) * volumen * math.sqrt(T) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)

def rho3():
    T = time
    _, d2 = calculate_d1_d2_2(T, spot3, strike3, risk_free, dividend, standard_deviation3)
    Nd2 = stats.norm.cdf(d2)

    if call_put3 == "Call":
        return (1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nd2
    else:
        Nmind2 = stats.norm.cdf(-d2)

        return -(1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nmind2 * volumen

##print(delta3())
##print(gamma3())
##print(theta3())
##print(vega3())
##print(rho3())

#caso 4

# Sell/Buy
sell_buy = "STO"
# Volumen 1 o -1
volumen4 = -1
# Type p o c
option_type = "c"

def d_one_new4(volatility4):
    return (math.log(spot4 / strike4) + (risk_free - dividend + 0.5 * volatility4 ** 2) * time2) / (volatility4 * math.sqrt(time1))

def nd_one_new4(volatility4):
    return math.exp(-(d_one_new4(volatility4) ** 2) / 2) / (math.sqrt(2 * math.pi))

def d_two_new4(volatility4):
    return d_one_new4(volatility4) - volatility4 * math.sqrt(time1)

def nd_two_new4(volatility4):
    return stats.norm.cdf(d_two_new4(volatility4))

def call_option_new4(volatility4):
    return math.exp(-dividend * time1) * spot4 * stats.norm.cdf(d_one_new4(volatility4)) - strike4 * math.exp(-risk_free * time1) * stats.norm.cdf(d_two_new4(volatility4))

def put_option_new4(volatility4):
    return strike4 * math.exp(-risk_free * time1) * stats.norm.cdf(-d_two_new4(volatility4)) - math.exp(-dividend * time1) * spot4 * stats.norm.cdf(-d_one_new4(volatility4))

def implied_call_volatility_new4():
    high = 5.0
    low = 0.0
    mid = (high + low) / 2.0

    while (high - low) > 0.000001:
        if call_option_new4(mid) > target4:  
            high = mid
        else:
            low = mid
        mid = (high + low) / 2.0

    return mid

standard_deviation4 = implied_call_volatility_new4()
#print(f"The implied volatility for the Call option is: {standard_deviation4 * 100}%")

# Calculo de las griegas

# Variables a asignar
style = "European"
direction4 = "Buy"
call_put4 = "Call"

def calculate_d1_d2_4(T, spot4, strike4, risk_free, dividend, standard_deviation4):
    dt = standard_deviation4 * math.sqrt(T)
    d1 = (math.log(spot4 / strike4) + (risk_free - dividend + (standard_deviation4 ** 2 / 2)) * T) / dt
    d2 = d1 - dt
    return d1, d2

def delta4():
    T = time1
    d1, d2 = calculate_d1_d2_4(T, spot4, strike4, risk_free, dividend, standard_deviation4)
    Nd1 = stats.norm.cdf(d1)

    if call_put4 == "Call":
        return math.exp(-dividend * T) * Nd1 * volumen4
    else:
        return math.exp(-dividend * T) * (Nd1 - 1) * volumen4
    

def gamma4():
    T = time1
    d1, _ = calculate_d1_d2_4(T, spot4, strike4, risk_free, dividend, standard_deviation4)

    return (math.exp(-dividend * T) * volumen4 / (spot4 * standard_deviation4 * math.sqrt(T))) * (1 / math.sqrt(2 * math.pi)) * math.exp(-(d1 ** 2) / 2)

def theta4():
    T = time1
    d1, d2 = calculate_d1_d2_4(T, spot4, strike4, risk_free, dividend, standard_deviation4)
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return 1 / 365 * (-(spot4 * standard_deviation4 * math.exp(-dividend * T) * volumen4 / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) - risk_free * strike4 * math.exp(-risk_free * T) * Nd2 + dividend * spot4 * math.exp(-dividend * T) * Nd1)
    else:
        Nmind1 = stats.norm.cdf(-d1)
        Nmind2 = stats.norm.cdf(-d2)

        return 1 / 365 * (-(spot4 * standard_deviation4 * math.exp(-dividend * T) * volumen4 / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) + risk_free * strike4 * math.exp(-risk_free * T) * Nmind2 - dividend * spot4 * math.exp(-dividend * T) * Nmind1)

def vega4():
    T = time1
    d1, _ = calculate_d1_d2_4(T, spot4, strike4, risk_free, dividend, standard_deviation4)

    return 1 / 100 * spot4 * math.exp(-dividend * T) * volumen4 * math.sqrt(T) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)

def rho4():
    T = time1
    _, d2 = calculate_d1_d2_2(T, spot4, strike4, risk_free, dividend, standard_deviation4)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return (1 / 100) * (strike4 * T * math.exp(-risk_free * T)) * Nd2
    else:
        Nmind2 = stats.norm.cdf(-d2)

        return -(1 / 100) * (strike4 * T * math.exp(-risk_free * T)) * Nmind2 * volumen

##print(f"delta {delta4()}")
##print(gamma4())
##print(theta4())
##print(vega4())
##print(rho4())



# p y l



#otro codigo
import math
import numpy as np
from scipy.stats import norm

# Payoff
def payoff(s, x, premium, flag, qty):
    if flag == "C":
        return max(s - x, 0) * qty - premium * qty
    else:
        return max(x - s, 0) * qty - premium * qty

# Intrinsic
def intrinsic(s1, x1, flag1):
    if flag1 == "C":
        return max(s1 - x1, 0)
    else:
        return max(x1 - s1, 0)

# PnL

def pnl(style, direction, call_put, s, x, pricing_date, maturity, risk_free, volatility, dividend, qty, multiplier, premium):
    if pricing_date == maturity:
        pnl_value = intrinsic(s, x, call_put) * qty * multiplier - premium * qty * multiplier
        intr = intrinsic(s, x, call_put)
        #print(f"intrinsic : {intr}")
        #print(f"PnL for {call_put} option at maturity: {pnl_value}")
        return pnl_value
    else:
        option_price = abs(option_pricer(style, direction, call_put, s, x, pricing_date, maturity, risk_free, volatility, dividend))
        pnl_value2 = option_price * qty * multiplier - premium * qty * multiplier
        #print(f"PnL for {call_put} option: {pnl_value2}")
        return pnl_value2

# Option_Pricer
def option_pricer(style, direction, Call_Put, spot, strike, pricing_date, maturity, risk_free, standard_deviation, dividend):
    t = (maturity - pricing_date).days / 365
    dt = standard_deviation * math.sqrt(t)
    d1 = (np.log(spot / strike) + (risk_free - dividend + (standard_deviation ** 2 / 2)) * t) / dt
    d2 = d1 - dt

    nd1 = norm.cdf(d1)
    nd2 = norm.cdf(d2)
    nmind2 = norm.cdf(-d2)
    nmind1 = norm.cdf(-d1)

    if Call_Put == "Call" and style == "European":
        return (spot * math.exp(-dividend * t) * nd1) - (strike * math.exp(-risk_free * t) * nd2)
    elif Call_Put == "Put" and style == "European":
        return (strike * math.exp(-risk_free * t) * nmind2) - (spot * math.exp(-dividend * t) * nmind1)
    else:
        if Call_Put == "Call":
            q = 1
            rf = risk_free
            div2 = dividend
        else:
            q = -1
            rf = dividend
            div2 = rf
            asset_spot = spot
            spot = strike
            strike = asset_spot

        volat = standard_deviation * (t) ** 0.5
        drift = risk_free - dividend
        volat2 = standard_deviation ** 2

        if (q * (risk_free - dividend) >= rf):
            if Call_Put == "Call":
                result = option_pricer("European", "Buy", "Call", spot, strike, pricing_date, maturity, risk_free, standard_deviation, dividend)
            else:
                result = option_pricer("European", "Buy", "Put", spot, strike, pricing_date, maturity, risk_free, standard_deviation, div2)

        return result
import datetime

#prueba
from datetime import datetime

import datetime
#caso 1

# parte del bucle
Style = "European"
Direction = "Buy"
Call_Put = "Put"
Strike = 3830
Spot = 3795
PricingDate = datetime.datetime(2023, 3, 10)
Maturity = datetime.datetime(2023, 3, 10)
RiskFree = 0.0027
StandardDeviation = 0.54
Dividend = 0.00001
Qty = 1
Multiplier = 100
Premium = 1.55

#para ver 1 resultado 
pnl_result = pnl(Style, Direction, Call_Put, Spot, Strike, PricingDate, Maturity, RiskFree, StandardDeviation, dividend, Qty, Multiplier, Premium)
print("El PnL es:", pnl_result)

pnl_results = {}

# Range de valores para Spot
for i in range(-12, 13): 
    Spot = Strike + i*15 if i <= 0 else Strike + (i-1)*15
    pnl_result = pnl(Style, Direction, Call_Put, Spot, Strike, PricingDate, Maturity, RiskFree, StandardDeviation, Dividend, Qty, Multiplier, Premium)
    pnl_results[Spot] = pnl_result

#for spot, pnl_result in pnl_results.items():
    #print(f'El PnL1 para Spot = {spot} es: {pnl_result}')


#grafico1
import matplotlib.pyplot as plt

# Extraer los valores de spot y pnl de pnl_results
spots = list(pnl_results.keys())
pnls = list(pnl_results.values())

# Crear el gráfico
plt.figure(figsize=(10,6))  # Se puede ajustar el tamaño del gráfico
plt.plot(spots, pnls, marker='o')  # Usamos 'o' para marcar cada punto
plt.title('PnL vs Spot')  # Título del gráfico
plt.xlabel('Spot')  # Etiqueta del eje x
plt.ylabel('PnL')  # Etiqueta del eje y
plt.grid(True)  # Muestra una grilla para facilitar la lectura
#plt.show()  # Muestra el gráfico

#caso 2
Style = "European"
Direction = "Sell"
Call_Put = "Put"
Spot = 3795
Strike = 3810
PricingDate = datetime.datetime(2023, 3, 10)
Maturity9 = datetime.datetime(2023, 3, 11)
RiskFree = 0.0027
StandardDeviation = 0.3444
Dividend = 0.000001
Qty = -1
Multiplier = 100
Premium = 3.80
#para ver un resultado
pnl_result2 = pnl(Style, Direction, Call_Put, Spot, Strike, PricingDate, Maturity9, RiskFree, StandardDeviation, Dividend, Qty, Multiplier, Premium)
print("El PnL2 es:", pnl_result2)

pnl_results = {}

# Range de valores para Spot
for i in range(-12, 13):
    Spott = strike + i*15
    pnl_result = pnl(Style, Direction, Call_Put, Spott, Strike, PricingDate, Maturity, RiskFree, StandardDeviation, Dividend, Qty, Multiplier, Premium)
    pnl_results[Spott] = pnl_result

#for spot, pnl_result in pnl_results.items():
    #print(f'El PnL2 para Spot = {spot} es: {pnl_result}')


#caso 3

# parte del bucle
Style = "European"
Direction = "Buy"
Call_Put = "Call"
call_put = "C"
Strike = 3995
Spot = 3795
PricingDate = datetime.datetime(2023, 3, 10)
Maturity = datetime.datetime(2023, 3, 10)
RiskFree = 0.0027
StandardDeviation = 0.4811
Dividend = 0.00001
Qty = 1
Multiplier = 100
Premium = 0.6

#para ver 1 resultado 
pnl_result3 = pnl(Style, Direction, call_put, Spot, Strike, PricingDate, Maturity, RiskFree, StandardDeviation, dividend, Qty, Multiplier, Premium)
print("El PnL3 es:", pnl_result3)

pnl_results3 = {}

# Range de valores para Spot
for i in range(-12, 13): 
    Spot3 = Spot + i*15 if i <= 0 else Strike + (i-1)*15
    pnl_result3 = pnl(Style, Direction, Call_Put, Spot3, Strike, PricingDate, Maturity, RiskFree, StandardDeviation, Dividend, Qty, Multiplier, Premium)
    pnl_results3[Spot] = pnl_result3

#for spot, pnl_result in pnl_results.items():
    #print(f'El PnL3 para Spot = {spot} es: {pnl_result3}')

#caso 4
Style = "European"
Direction = "Sell"
Call_Put = "Call"
Spot = 3795
Strike = 4015
PricingDate = datetime.datetime(2023, 3, 10)
Maturity9 = datetime.datetime(2023, 3, 11)
RiskFree = 0.0027
StandardDeviation = 0.2754
Dividend = 0.000001
Qty = -1
Multiplier = 100
Premium = 1.15
#para ver un resultado
pnl_result4 = pnl(Style, Direction, Call_Put, Spot, Strike, PricingDate, Maturity9, RiskFree, StandardDeviation, Dividend, Qty, Multiplier, Premium)
print("El PnL4 es:", pnl_result4)
