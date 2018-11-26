"""
    Month Filter
    Parameter QTR, MONTH dan Year (Opsional)
"""
def bulan(qtr = None, month = None, year = None):
    bulan           =   ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    result          =   bulan

    if qtr != None and qtr != 'null' and year != None and year != 'null':
        if qtr == "1":
            result           =   bulan[0:3]

        if qtr == "2":
            result           =   bulan[3:6]

        if qtr == "3":
            result           =   bulan[6:9]

        if qtr == "4":
            result           =   bulan[9:12]

    if month != None and month != 'null' and year != None and year != 'null':
        if month == "1":
            result           =   bulan[0:1]

        if month == "2":
            result           =   bulan[1:2]

        if month == "3":
            result           =   bulan[2:3]

        if month == "4":
            result           =   bulan[3:4]
        
        if month == "5":
            result           =   bulan[4:5]

        if month == "6":
            result           =   bulan[5:6]

        if month == "7":
            result           =   bulan[6:7]

        if month == "8":
            result           =   bulan[7:8]

        if month == "9":
            result           =   bulan[8:9]

        if month == "10":
            result           =   bulan[9:10]

        if month == "11":
            result           =   bulan[10:11]

        if month == "12":
            result           =   bulan[11:12]

    return result

"""
    Month ID
    Parameter QTR, MONTH dan Year (Opsional)
"""
def bulan_int(qtr = None, month = None, year = None):
    bulan_int       =   [1,2,3,4,5,6,7,8,9,10,11,12]
    result          =   bulan_int

    if qtr != None and qtr != 'null' and year != None and year != 'null':
        if qtr == "1":
            result       =   bulan_int[0:3]

        if qtr == "2":
            result       =   bulan_int[3:6]

        if qtr == "3":
            result       =   bulan_int[6:9]

        if qtr == "4":
            result       =   bulan_int[9:12]

    if month != None and month != 'null' and year != None and year != 'null':
        if month == "1":
            result       =   bulan_int[0:1]

        if month == "2":
            result       =   bulan_int[1:2]

        if month == "3":
            result       =   bulan_int[2:3]

        if month == "4":
            result       =   bulan_int[3:4]
        
        if month == "5":
            result       =   bulan_int[4:5]

        if month == "6":
            result       =   bulan_int[5:6]

        if month == "7":
            result       =   bulan_int[6:7]

        if month == "8":
            result       =   bulan_int[7:8]

        if month == "9":
            result       =   bulan_int[8:9]

        if month == "10":
            result       =   bulan_int[9:10]

        if month == "11":
            result       =   bulan_int[10:11]

        if month == "12":
            result       =   bulan_int[11:12]

    return result

def separate(nominal, separate = None):
    if separate == '1':
        bagi = 1000
    elif separate == '2':
        bagi = 1000000
    elif separate == '3':
        bagi = 1000000000

    if separate == None:
        return nominal
    else:
        return nominal // bagi

def total(arr, field):
    result = 0
    
    for a in arr:
        result += getattr(a, field)

    return result