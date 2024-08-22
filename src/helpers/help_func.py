import decimal
ctx = decimal.Context()


def float_to_str(f, prec=18):
    ctx.prec = prec
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')
