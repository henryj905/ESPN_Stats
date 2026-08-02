def compare_punting_no(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['NO']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_punting_yds(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['YDS']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_punting_avg(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['AVG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_punting_TB(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['TB']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_punting_in_20(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['In 20']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0


def compare_punting_long(TF_list):
    if 'punting' in TF_list:
        list = TF_list['punting']
        list = list['LONG']
        list = list.drop(columns=['category'])
        if list.iloc[0] == True:
            return True
        elif list.iloc[0] == False:
            return False
    else:
        return 0