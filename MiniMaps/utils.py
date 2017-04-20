import datetime

# Get UTC today
timestamp = lambda : datetime.datetime.strftime(datetime.datetime.utcnow(), "%D %T")

# Get first row of a dataframe
row_zero = lambda data: {k : v[0] for k, v in data.items()}