MONEY_FRACTION = [
    {
    "value": 100000,
    "type" : "lembar"
    },
    {
    "value": 50000,
    "type" : "lembar"
    },
    {
    "value": 20000,
    "type" : "lembar"
    },
    {
    "value": 10000,
    "type" : "lembar"
    },
    {
    "value": 5000,
    "type" : "lembar"
    },
    {
    "value": 2000,
    "type" : "lembar"
    },
    {
    "value": 1000,
    "type" : "lembar"
    },
    {
    "value": 500,
    "type" : "koin"
    },
    {
    "value": 200,
    "type" : "koin"
    },
    {
    "value": 100,
    "type" : "koin"
    }                          
]

def format_price(int):
    return "{:,.0f}".format(int).replace(",", ".")

def shopping_payment(total_price, payment):
    result_fractions = []
    print(f"Total belanja seorang customer: Rp {format_price(total_price)}")
    print(f"Pembeli membayar: Rp {format_price(payment)}\n")

    if (payment-total_price<0):
        return print("False, kurang bayar")
    
    change = payment-total_price
    rounded_change = ((change) // 100) * 100

    if (change!=rounded_change):
        print(f"Kembalian yang harus diberikan kasir: {format_price(change)}, dibulatkan menjadi \033[1m{format_price(rounded_change)}\033[0m \n")
    else:
        print(f"Kembalian yang harus diberikan kasir: {format_price(change)}\n")
    
    if change == 0:
        return False
    
    for money_frac in MONEY_FRACTION:
        result_count = 0
        if ((rounded_change-money_frac["value"])<0):
            continue
        else:
            while ((rounded_change-money_frac["value"])>=0):
                rounded_change -= money_frac["value"]
                result_count+=1
            result_fractions.append(    
                {
                "value": money_frac["value"],
                "type" : money_frac["type"],
                "count":result_count
                })
    
    if (len(result_fractions)!=0):
        print("Pecahan uang:")
        for result in result_fractions:
            print(f"{result["count"]} {result["type"]} {format_price(result["value"])}")
    

if __name__ == "__main__":
    input_total_price = 575650
    input_payment = 58000
    result = shopping_payment(input_total_price,input_payment)

    if ( result==False):
        print("False, kurang bayar")
