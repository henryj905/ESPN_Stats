def compare_kicking_pct(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['PCT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_long(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['LONG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_pts(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['PTS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_fg_made(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['FG MADE']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_fg_att(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['FG ATT']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_ex_made(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['EX MADE']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_kicking_ex_att(TF_list):
    if 'kicking' in TF_list:
        list = TF_list['kicking']
        list = list['EX MADE']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0
