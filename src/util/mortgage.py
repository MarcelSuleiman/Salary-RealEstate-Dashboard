import numpy_financial as npf


def get_payment_for_mortgage(price, rate, years):
    m_rate = rate / 12
    months = years * 12
    m_payment = npf.pmt(rate=m_rate, nper=months, pv=price)

    return -m_payment


if __name__ == "__main__":

    # real_estate_price = 59000
    # average_salary_netto = 1040
    real_estate_price = 280000
    average_salary_netto = 1340+1682 # +340

    rates = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]  # % in mathematical explanation 0.07 == 7%

    additional_finance = get_payment_for_mortgage(price=real_estate_price * 0.2, rate=0.06, years=8)

    for r in rates:
        mortgage_payment = get_payment_for_mortgage(price=real_estate_price * 0.8, rate=r, years=35)
        percentage_from_salary = (mortgage_payment * 100) / average_salary_netto
        percentage_from_salary_with_add_f = ((mortgage_payment+additional_finance) * 100) / average_salary_netto

        # print(
        #     f"Splátka vo výške: {round(mortgage_payment, 2)}€ predstavuje "
        #     f"zaťaženie vo výške {round(percentage_from_salary, 2)}% z platu."
        # )

        msg = (
            f"uroková sadzba: {round(r*100, 2)}%\n"
            f"Pri cene nehnutelnosti {real_estate_price}€ by človek musel "
            f"mesačne zaplatiť: {round(mortgage_payment+additional_finance, 2)}€ čo predstavuje "
            f"celkové zaťaženie {round(percentage_from_salary_with_add_f, 2)}% z platu."
        )
        print(msg)

