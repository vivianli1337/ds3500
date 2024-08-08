from drv import DRV

def main():
    burger = DRV({250: .25, 500: .25, 750: .25, 1000: .25})
    fries = DRV({200: .10, 500: .30, 1000: .40, 5000: .20})
    coke = DRV({100: .05, 1000: .80, 2000: .15})

    profit = .25 * burger + 0.50 * fries + 1.0 * coke

    expenses = DRV({2500:1})
    net = profit - expenses
    annual_net = .365 * net # 100k units

    annual_net.plot()


if __name__ == '__main__':
    main()
