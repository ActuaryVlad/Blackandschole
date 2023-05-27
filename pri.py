from datetime import datetime, date, time
import math
import scipy.stats as stats
import py_vollib.black_scholes.implied_volatility as iv

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
strike3 = 3830
#precio de la opcion
target3 = 1.55

#caso 4
#precio del activo subyacente
spot4 = 3907.25
# Precio Strike 
strike4 = 3830
#precio de la opcion
target4 = 1.55


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


time = (maturity - timestamp) / (365 * 24 * 60 * 60)

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
print(f"The implied volatility for the Put option is: {standard_deviation * 100}%")

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

print(delta())
print(gamma())
print(theta())
print(vega())
print(rho())

#Caso 2

#Sell/Buy
sell_buy = "STO"
#Volumen 1 o -1
volumen = -1
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
        if put_option_new(mid) > target2:  # Aquí debe ser target2, no target
            high = mid
        else:
            low = mid
        mid = (high + low) / 2.0

    return mid

standard_deviation2 = implied_put_volatility_new()
print(f"The implied volatility for the Put option is: {standard_deviation2 * 100}%")

#Calculo de las griegas

# Variables a asignar
style = "European"
direction = "Buy"
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
        return math.exp(-dividend * T) * Nd1
    else:
        return math.exp(-dividend * T) * (Nd1 - 1)

def gamma2():
    T = time1
    d1, _ = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)

    return (math.exp(-dividend * T) / (spot2 * standard_deviation2 * math.sqrt(T))) * (1 / math.sqrt(2 * math.pi)) * math.exp(-(d1 ** 2) / 2)

def theta2():
    T = time1
    d1, d2 = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)
    Nd1 = stats.norm.cdf(d1)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return 1 / 365 * (-(spot2 * standard_deviation2 * math.exp(-dividend * T) / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) - risk_free * strike1 * math.exp(-risk_free * T) * Nd2 + dividend * spot2 * math.exp(-dividend * T) * Nd1)
    else:
        Nmind1 = stats.norm.cdf(-d1)
        Nmind2 = stats.norm.cdf(-d2)

        return 1 / 365 * (-(spot2 * standard_deviation2 * math.exp(-dividend * T) / (2 * math.sqrt(T)) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)) + risk_free * strike1 * math.exp(-risk_free * T) * Nmind2 - dividend * spot2 * math.exp(-dividend * T) * Nmind1)

def vega2():
    T = time1
    d1, _ = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)

    return 1 / 100 * spot2 * math.exp(-dividend * T) * math.sqrt(T) * 1 / math.sqrt(2 * math.pi) * math.exp(-(d1 ** 2) / 2)

def rho2():
    T = time1
    _, d2 = calculate_d1_d2_2(T, spot2, strike1, risk_free, dividend, standard_deviation2)
    Nd2 = stats.norm.cdf(d2)

    if call_put == "Call":
        return (1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nd2
    else:
        Nmind2 = stats.norm.cdf(-d2)

        return -(1 / 100) * (strike1 * T * math.exp(-risk_free * T)) * Nmind2

print(delta2())
print(gamma2())
print(theta2())
print(vega2())
print(rho2())
