import requests


def read_real_future_data(future_code):

    # Read Real Time Data From Sina
    # Input: Contract Name
    # Output：Contract Detail in Array

    # future_code ='M0'
    # 0 means continuous contract

    # Sina Data Url
    url_str = ('http://hq.sinajs.cn/list=' + future_code)
    req = requests.get(url_str)

    # Data Processing
    future_code_list = future_code.split(',')
    req_list = list(req)

    req_b = b''
    for i in range(len(req_list)):
        req_b += req_list[i]

    req_str = str(req_b, 'utf-8', "ignore")
    str_fen = req_str.split(';')

    future_data = []

    for i in range(len(future_code_list)):

        future_item = []
        future_item.append(future_code_list[i])

        str_dou = str_fen[i].split(',')
        future_item.append(str_dou[6])

        future_data.append(future_item)

    return future_data


if __name__ == '__main__':
    future_data = read_real_future_data('BU0,SU0,BU0')
    # print('code name date,open,high,low,close,vol')
    print(future_data)
