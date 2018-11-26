def month(start, end):
    bulan           =   ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

    start_month     =   start.split("-")[1]
    end_month       =   end.split("-")[1]

    if start_month == end_month:
        return bulan[int(start_month) - 1]
    else:
        return bulan[(int(start_month) - 1):int(end_month)]

def month_to_number(start, end):
    no_bulan           =   [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    start_month     =   start.split("-")[1]
    end_month       =   end.split("-")[1]

    if start_month == end_month:
        return [no_bulan[int(start_month) - 1]]
    else:
        return no_bulan[(int(start_month) - 1):int(end_month)]

def date_to_month_number(data):
    return int(data.split("-")[1])