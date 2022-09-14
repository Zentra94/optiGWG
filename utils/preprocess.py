from datetime import datetime

import numpy as np


def fix_binaries(val, val_true="VERDADERO"):
    """
    Fix binary features
    :return:
    :rtype:
    """
    if isinstance(val, str):
        return int(val == val_true)
    if np.isnan(val):
        return val
    if isinstance(val, int) or isinstance(val, float):
        return int(val > 0)
    else:
        return


def fix_dttms(dttm):
    if not isinstance(dttm, str):
        return
    dttm_form = {"Jan": "01",
                 "Feb": "02",
                 "Mar": "03",
                 "Apr": "04",
                 "May": "05",
                 "Jun": "06",
                 "Jul": "07",
                 "Aug": "08",
                 "Sep": "09",
                 "Oct": "10",
                 "Nov": "11",
                 "Dec": "12"}
    final_dttm = []
    for i, s in enumerate(dttm.split("-")):
        if not s.isnumeric():
            return
        if i == 2:
            if 0 <= int(s) <= 22:
                final_dttm.append("20{}".format(s))
            else:
                final_dttm.append("19{}".format(s))
        else:
            if s in dttm_form:
                final_dttm.append(dttm_form[s])
            else:
                final_dttm.append(s)
    return datetime.strptime("-".join(final_dttm), '%d-%m-%Y')


def clean_str(val):
    specials = {"ã‘uã‘oa": "ñuñoa", "peã‘alolen": "peñalolen", "otra regiã³n": "otra región",
                "estaciã“n central": "estación central"}
    spanish = {"ñ": "n", "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    if not isinstance(val, str):
        return val
    val_ = val.lower()
    if val_ in specials:
        val_ = specials[val_]

    for k in spanish:
        val_.replace(k, spanish[k])

    return val_
