def compare_passing_yds(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['YDS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_avg(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['AVG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_td(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['TD']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_int(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['INT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_sacks(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['SACKS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_comp(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['COMP']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_att(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['ATT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_passing_comp_pct(TF_list):
    if 'passing' in TF_list:
        list = TF_list['passing']
        list = list['COMP_PCT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0