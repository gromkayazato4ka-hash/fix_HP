def info(op, message):
    op.report({"INFO"}, message)


def warning(op, message):
    op.report({"WARNING"}, message)
