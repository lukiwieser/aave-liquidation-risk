import json


class UserData:
    def __init__(self):
        self.debt_timeline = dict()
        self.collateral_timeline = dict()

    def add_borrow(self, asset, amount, timestamp):
        if asset not in self.debt_timeline:
            self.debt_timeline[asset] = []
        self.debt_timeline[asset].append(["borrow", amount, str(timestamp)])

    def add_repay(self, asset, amount, timestamp):
        if asset not in self.debt_timeline:
            self.debt_timeline[asset] = []
        self.debt_timeline[asset].append(["repay", amount, str(timestamp)])

    def add_liquidation_victim(self, debt_asset, debt_to_cover, timestamp):
        if debt_asset not in self.debt_timeline:
            self.debt_timeline[debt_asset] = []
        self.debt_timeline[debt_asset].append(["liquidation", debt_to_cover, str(timestamp)])

    def add_deposit(self, asset, amount, timestamp):
        if asset not in self.collateral_timeline:
            self.collateral_timeline[asset] = []
        self.collateral_timeline[asset].append(["deposit", amount, str(timestamp)])

    def add_withdraw(self, asset, amount, timestamp):
        if asset not in self.collateral_timeline:
            self.collateral_timeline[asset] = []
        self.collateral_timeline[asset].append(["withdraw", amount, str(timestamp)])

    def sort_timelines(self):
        for asset, events in self.debt_timeline.items():
            self.debt_timeline[asset] = sorted(events, key=lambda x: x[2])
        for asset, events in self.collateral_timeline.items():
            self.collateral_timeline[asset] = sorted(events, key=lambda x: x[2])

    def to_json(self):
        data = dict()
        data["debt_timeline"] = self.debt_timeline
        data["collateral_timeline"] = self.collateral_timeline
        return json.dumps(data)