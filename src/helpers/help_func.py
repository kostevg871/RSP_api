import decimal
ctx = decimal.Context()


def float_to_str(f, prec=18):  # 18 знаков хватит всем (c) BG
    ctx.prec = prec
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')
