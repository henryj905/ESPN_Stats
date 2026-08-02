def compare_interceptions_int(TF_list):
    if 'interceptions' in TF_list:
        list = TF_list['interceptions']
        list = list['INT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_interceptions_yds(TF_list):
    if 'interceptions' in TF_list:
        list = TF_list['interceptions']
        list = list['YDS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_interceptions_td(TF_list):
    if 'interceptions' in TF_list:
        list = TF_list['interceptions']
        list = list['TD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0
