import math
from datetime import datetime, timedelta

def isVacation(jumlah_cuti_bersama, tanggal_join_str, tanggal_rencana_str, durasi_cuti):
    cuti_pribadi = 14 - jumlah_cuti_bersama
    tanggal_join = datetime.strptime(tanggal_join_str, "%Y-%m-%d")
    tanggal_rencana = datetime.strptime(tanggal_rencana_str, "%Y-%m-%d")

    # Add 180 days
    limited_vacation_date = tanggal_join + timedelta(days=180)
    if (tanggal_rencana<limited_vacation_date):
        return False, "Karena belum 180 hari sejak tanggal join karyawan"

    year_join = tanggal_join.year
    end_date_based_year = datetime(year_join, 12, 31)
    different_days = (end_date_based_year - limited_vacation_date).days
    total_vacation_able_take = math.floor((different_days/365)*cuti_pribadi)
    if (durasi_cuti>total_vacation_able_take):
        return False, f"Karena hanya boleh mengambil {total_vacation_able_take} hari cuti"
    
    if (durasi_cuti>3):
        return False, "Karena hanya boleh mengambil max 3 hari berurutan"
    
    return True, ""
    




if __name__ == "__main__":
    jumlah_cuti_bersama = 7
    tanggal_join = "2021-05-01"
    tanggal_rencana = "2021-11-05"
    durasi_cuti = 3
    output, reason = isVacation(jumlah_cuti_bersama, tanggal_join, tanggal_rencana, durasi_cuti)
    
    print(output)
    if(output == False):
        print(f"Alasan {reason}")
