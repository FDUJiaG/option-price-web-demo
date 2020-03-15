from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import numpy as np
from scipy.stats import norm
import random

from .pkg import read_real_future_data

# Future Info
Future_Dic = {
    'SC': ['Crude Oil', 'INE'],
    'BU': ['Asphalt', 'SHFE'],
    'SP': ['Pulp', 'SHFE'],
    'AG': ['Silver', 'SHFE'],
    'RB': ['Rebar', 'SHFE'],
    'HC': ['Hot Strip', 'SHFE'],
    'AU': ['Gold', 'SHFE'],
    'ZN': ['Zinc', 'SHFE'],
    'FU': ['Fuel Oil', 'SHFE'],
    'RU': ['Rubber', 'SHFE'],
    'AL': ['Aluminum', 'SHFE'],
    'CU': ['Copper', 'SHFE'],
    'C': ['Corn', 'DCE'],
    'J': ['Coke', 'DCE'],
    'P': ['Palm Oil', 'DCE'],
    'JD': ['Egg', 'DCE'],
    'M': ['Soybean Meal', 'DCE'],
    'Y': ['Soybean Oil', 'DCE'],
    'L': ['Plastic', 'DCE'],
    'EG': ['Ethylene Glycol', 'DCE'],
    'I': ['Iron Ore', 'DCE'],
    'JM': ['Coking Coal', 'DCE'],
    'V': ['Polyvinyl Chloride', 'DCE'],
    'CS': ['Starch', 'DCE'],
    'PP': ['Polypropylene', 'DCE'],
    'CF': ['Cotton', 'CSCE'],
    # 'UR': ['Urea', 'CSCE'],           # the Sina Data API don't support it
    'CJ': ['Jujube', 'CSCE'],
    'ZC': ['Thermal Coal', 'CSCE'],
    'AP': ['Apple', 'CSCE'],
    'MA': ['Methanol', 'CSCE'],
    'FG': ['Glass', 'CSCE'],
    'RM': ['Rapeseed Meal', 'CSCE'],
    # 'SA': ['Soda Ash', 'CSCE'],       # the Sina Data API don't support it
    'SR': ['White Sugar', 'CSCE'],
    'TA': ['Pure Terephthalic Acid', 'CSCE'],
}

"""
Plain Vanilla Options (Amc/Euro Call/Put)

s=spot price
k=strick price
t=holding period
vol=volatility
rf=risk free rate
is_call=True(call);False(put)
futures=True(futures);False(stock)
"""

# set constant
# vol_list = [0.19, 0.21]
no_risk_rate = 0.03


def euro_pv_option_bs(s, k, t, vol, rf, is_call=True, futures=True):

    r = (1 - futures) * rf
    d1 = (np.log(s / k) + (r + 0.5 * vol ** 2) * t) / (vol * t ** 0.5)
    d2 = d1 - vol * t ** 0.5

    if is_call:
        price = s * norm.cdf(d1) - k * np.exp(- r * t) * norm.cdf(d2)
    else:
        price = k * np.exp(- r * t) * norm.cdf(- d2) - s * norm.cdf(- d1)
    return price * (np.exp(- rf * t) ** futures)


def page_not_found(request, exception):
    return render(request, 'options/404.html')


def page_server_error(request):
    return render(request, 'options/500.html')


@login_required
def get_options_list(request):

    delta_time = 0.1

    subject = list(Future_Dic.keys())

    subs_code = []

    for subs in subject:
        subs_code.append(subs + '0')

    code_str = ','.join(subs_code)
    price_list = read_real_future_data.read_real_future_data(code_str)

    option_list = []

    for i in range(len(subject)):

        close_price = float(price_list[i][1])

        vol_tmp = random.uniform(0.05, 0.4)
        vol_list = [vol_tmp, min(max(random.uniform(0.1, 1), vol_tmp + 0.03), 3 * vol_tmp)]


        s = k = close_price
        buy_price = euro_pv_option_bs(s, k, delta_time, vol_list[0], no_risk_rate, True, True)
        sell_price = euro_pv_option_bs(s, k, delta_time, vol_list[1], no_risk_rate, False, True)

        buy_percent = buy_price / close_price
        sell_percent = sell_price / close_price

        option_item = [
            Future_Dic[subject[i]][0],
            subject[i],
            close_price,
            format(vol_list[0], '.2%'),
            format(vol_list[1], '.2%'),
            format(buy_price, '.2f'),
            format(sell_price, '.2f'),
            format(buy_percent, '.2%'),
            format(sell_percent, '.2%')
        ]

        option_list.append(option_item)

    return render(request, 'options/index.html',
                  {
                      'subject': subject,
                      'option_list': option_list,
                  })
