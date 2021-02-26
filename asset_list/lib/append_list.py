import numpy as np


def normalize(tmp_list, add_row_num, value):
    """ tmp_listの行数をadd_row_numだけ増やす。
    増やした要素はvalueで初期化する。
    リスト内包処理でリストを初期化。
    """
    col = len(tmp_list[0])
    for j in range(add_row_num):
        row = [value for i in range(col)]
        tmp_list.append(row)
    return tmp_list


def append_list(a_list, b_list, value):
    """ a_listにb_listを列として追加する。
    a_listがb_listよりも長く、数値のリストならば、valueは数値を与える。
    a_listがb_listよりも短い場合、valueは数値でも文字でも良い。
    """
    cnt_a = len(a_list)
    cnt_b = len(b_list)
    # a_listとb_listの行数を揃える。
    if cnt_a > cnt_b:
        b_list = normalize(b_list, cnt_a-cnt_b, value)
    else:
        a_list = normalize(a_list, cnt_b-cnt_a, value)
    # listをnumpyのdarrayに変換。
    a = np.array(a_list)
    b = np.array(b_list)
    # aの最終列に配列bをinsertする。
    try:
        c = np.insert(a, [len(a[0])], b, axis=1)
    except ValueError:
        print(f'{type(value)} is bad value')
    return c
