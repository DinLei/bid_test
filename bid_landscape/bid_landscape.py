#!/usr/bin/python


class BidLandscape:
    """The landscape making and storage class."""

    def __init__(self, dataset, camp_id, laplace=1):
        self.dataset = dataset
        self.dataset.init_landscape(self)
        self.camp_id = camp_id
        self.laplace = laplace if laplace > 1 else 1
        self.init_distribution()
        self.make_distribution()
        print("Inited Bid Landscape.")

    def get_campaign_id(self):
        return self.camp_id

    def init_distribution(self):
        self.max_price = self.dataset.get_max_price()
        self.min_price = self.dataset.get_min_price()
        self.pacing_distribution = [0.0 * i for i in range(0, self.max_price + 1)]
        self.imp_distribution = [0.0 * i for i in range(0, self.max_price + 1)]

    def get_pacing_distribution(self):
        return self.pacing_distribution

    def make_distribution(self):  # make the original distribution with laplace smoothing
        mp_dict = {}
        iter_id = self.dataset.init_index()
        # 参竞  曝光  点击  到站  出价
        while not self.dataset.reached_tail(iter_id):
            data = self.dataset.get_next_data(iter_id)
            mp = data[4]
            if mp in mp_dict:
                mp_dict[mp] = mp_dict[mp] + 1
            else:
                mp_dict[mp] = 1
        total_num = self.dataset.get_size() + (self.max_price + 1) * self.laplace
        for p in range(0, self.max_price + 1):
            if p not in mp_dict:
                self.pacing_distribution[p] = 1.0 * self.laplace / total_num
            else:
                self.pacing_distribution[p] = 1.0 * (mp_dict[p] + self.laplace) / total_num
        print("Landscape made.")

    def get_probability(self, price):  # get the probability of the given price in the landscape
        price = int(price)
        probability = 0.0
        if price > self.max_price:
            probability = self.pacing_distribution[self.max_price]
        elif price < 0:
            probability = self.pacing_distribution[0]
        else:
            probability = self.pacing_distribution[price]
        return probability


def main():
    print("main method.")


if __name__ == '__main__':
    main()
