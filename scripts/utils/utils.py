import datetime


def strip_0x_from_address(address):
    if address[:2] == "0x":
        address = address[2:]
    return address


def hexunit256_to_int(num_string):
    uint_max_value = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    if num_string == uint_max_value:
        return -1
    else:
        return int(num_string, 16)


def sort_dict_by_value(dict, reverse):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=reverse)}


def round_dict_values(dict, decimal_points):
    return {k: round(v, decimal_points) for k, v in dict.items()}


# input:    1606836555
# output:   2020-12-01T00:00:00
def timestamp_to_simple_iso(timestamp, shouldStripTime):
    date = datetime.datetime.utcfromtimestamp(timestamp)
    if shouldStripTime:
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return date.isoformat()
