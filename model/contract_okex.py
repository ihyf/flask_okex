class ContractOkEx(object):
    def __init__(self, this_week_name, this_week_price, next_week_name, next_week_price,
                 this_quarter_name, this_quarter_price, this_week_vs_next_week, this_week_vs_quarter, next_week_vs_quarter):
        self.this_week_name = this_week_name
        self.this_week_price = this_week_price
        self.next_week_name = next_week_name
        self.next_week_price = next_week_price
        self.this_quarter_name = this_quarter_name
        self.this_quarter_price = this_quarter_price
        self.this_week_vs_next_week = this_week_vs_next_week
        self.this_week_vs_quarter = this_week_vs_quarter
        self.next_week_vs_quarter = next_week_vs_quarter
