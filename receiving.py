def compare_receiving_rec(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['REC']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_receiving_yds(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['YDS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_receiving_avg(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['AVG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_receiving_td(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['TD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_receiving_long(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['LONG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_receiving_tgts(TF_list):
    if 'receiving' in TF_list:
        list = TF_list['receiving']
        list = list['TGTS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0