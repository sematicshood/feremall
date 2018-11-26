def month(start, end):
    bulan           =   ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

    start_month     =   start.split("-")[1]
    end_month       =   end.split("-")[1]

    if start_month == end_month:
        return bulan[int(start_month) - 1]
    else:
        return bulan[(int(start_month) - 1):int(end_month)]