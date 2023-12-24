# проверяет данные
def pars(data_info={}, data_bill={}):
    result_user_info = []
    result_bill = []
    exapm_bill = {}
    examp_info = {}
    for i in data_info:
        examp_info["first_name"] = i[0]
        examp_info["phone_number"] = i[1]
        examp_info["gmail"] = i[2]
        examp_info["status_aprove"] = i[3]
        result_user_info.append(examp_info.copy())
    for i in data_bill:
        exapm_bill["type_bill"] = i[0]
        exapm_bill["ballans"] = i[1]
        exapm_bill["limit_bill"] = i[2]
        exapm_bill["status_bill"] = i[3]
        exapm_bill["bill_idd"] = i[4]
        result_bill.append(exapm_bill.copy())
    if examp_info == {} and result_bill != []:
        return {"USER_BILL": result_bill}
    elif examp_info != {} and result_bill == []:
        return {"USER_INFO": examp_info}
    elif examp_info != {} and result_bill != []:
        return {"USER_INFO": examp_info, "USER_BILL": result_bill}
    else:
        return None
