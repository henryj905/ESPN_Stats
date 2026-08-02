def compare_defensive_tackles(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['TOT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0

def compare_defensive_solo(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['SOLO']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_defensive_sacks(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['SACKS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_defensive_tfl(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['TFL']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_defensive_pd(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['PD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_defensive_qb_hits(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['QB HITS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_defensive_td(TF_list):
    if 'defensive' in TF_list:
        list = TF_list['defensive']
        list = list['TD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0