def check_duplicates_in_list(list):
    set_list = set()
    for item in list:
        if item in set_list:
            return True
        else:
            set_list.add(item)
    return False
