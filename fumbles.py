def compare_fumbles_fum(TF_list):
    if 'fumbles' in TF_list:
        list = TF_list['fumbles']
        list = list['FUM']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_fumbles_lost(TF_list):
    if 'fumbles' in TF_list:
        list = TF_list['fumbles']
        list = list['LOST']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0