def compare_rushing_car(TF_list):
    if 'rushing' in TF_list:
        list = TF_list['rushing']
        list = list['CAR']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_rushing_yds(TF_list):
    if 'rushing' in TF_list:
        list = TF_list['rushing']
        list = list['YDS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_rushing_avg(TF_list):
    if 'rushing' in TF_list:
        list = TF_list['rushing']
        list = list['AVG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_rushing_td(TF_list):
    if 'rushing' in TF_list:
        list = TF_list['rushing']
        list = list['TD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_rushing_long(TF_list):
    if 'rushing' in TF_list:
        list = TF_list['rushing']
        list = list['LONG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0