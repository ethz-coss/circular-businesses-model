from mesa import Agent
from agents.consumer import ConsumerAgent
from parameters import MAINTENANCE_COST, PRODUCTINO_COST_PER_UNIT_SCALE_FACTOR, WASTE_PENALTY, CIRCULARITY_SUBSIDY_SCALE_FACTOR, PRICE_CAP_LOW, PRICE_CAP_HIGH, NUM_CONSUMERS, RAW_PRICE_MULTIPLIER, MATERIAL_PURCHASE_LIMIT
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import utils

class CompanyAgent(Agent):

    def __init__(self, model, raw_material, circularity=0, competition=0, color="red"):
        super().__init__(model)
        self.money = 0 #INITIAL_MONEY
        self.raw_material = raw_material

        self.circularity = circularity
        self.competition = competition

        self.price = 0
        self.products = 0
        self.quantity = 0

        self.material_pool = 0
        self.total_unsold_waste = 0

        self.total_material_purchased = 0
        self.avg_cost_per_product = 0

        self.color = color

        self.sol1_prices = []
        self.sol2_prices = []
        self.sol3_prices = []

        self.sol1_quants = []
        self.sol2_quants = []
        self.sol3_quants = []

        self.sol1_profits = []
        self.sol2_profits = []
        self.sol3_profits = []

    def has_supply(self):
        return self.quantity >= 1

    def sell(self):
        # if self.products <= 0:
        #     # print(f"Company {self.circularity} tried to sell but has no products.")
        #     return
        self.products -= 1
        self.money += self.price

    def fixed_costs_per_year(self):
        return MAINTENANCE_COST * (1 + self.circularity)

    def production_cost_per_unit(self):
        return PRODUCTINO_COST_PER_UNIT_SCALE_FACTOR * (1 + self.circularity)
    
    def circularity_subsidy(self):
        return CIRCULARITY_SUBSIDY_SCALE_FACTOR * self.circularity
    
    def material_cost_for_quantity(self, quantity):
        # Check leftovers if you were to take the material from the pool

        if self.material_pool >= quantity:
            return 0, 0
        else:
            leftover = quantity - self.material_pool
            
        return leftover, self.raw_material.cost(leftover)

    def variable_costs_for_quantity(self, quantity, take=False):

        production_cost = self.production_cost_per_unit() * quantity
        leftover, expected_material_cost = self.material_cost_for_quantity(quantity)

        if take:
            if self.material_pool >= quantity:
                leftover = 0
                self.material_pool -= quantity
            else:
                leftover = quantity - self.material_pool
                self.material_pool = 0

            material_cost = self.raw_material.take_raw_material(leftover)
            assert material_cost == expected_material_cost

            self.total_material_purchased += leftover

        return production_cost + expected_material_cost
    
    def get_unsold_waste(self):

        unsold_waste = self.quantity * (1 - self.circularity)
        self.money -= unsold_waste * WASTE_PENALTY

        self.total_unsold_waste += unsold_waste
        return self.total_unsold_waste
    
    def add_unsold_material_to_material_pool(self, unsold):
        self.material_pool += int(unsold * self.circularity)

    def add_sold_material_to_material_pool(self, sold):
        self.material_pool += int(sold * self.circularity * 0.8)

    def year_start(self):
        self.price = 0
        self.quantity = 0
        self.products = 0
        self.avg_cost_per_product = 0
        self.money += self.circularity_subsidy()

        fixed_costs = self.fixed_costs_per_year()
        self.money -= fixed_costs

        # if self.total_material_purchased > MATERIAL_PURCHASE_LIMIT:
        #     return

        # print(self.price, self.quantity)
        self.get_best_price()

        var_costs = self.variable_costs_for_quantity(self.quantity, take=True)
        self.money -= var_costs

        self.products = self.quantity
        if self.quantity > 0:
            self.avg_cost_per_product = (fixed_costs + var_costs) / self.quantity
        else:
            self.avg_cost_per_product = 0
    
    def year_end(self):
        self.add_unsold_material_to_material_pool(self.products)
        self.add_sold_material_to_material_pool(self.quantity - self.products)

    def get_best_price(self):

        if self.material_pool <= 0 and self.raw_material.remaining <= 0:
            self.price = PRICE_CAP_HIGH
            self.quantity = 0
            print(f"Company {self.circularity} decided not to produce anything due to lack of raw material.")
            return

        # define variables as in report
        b = PRICE_CAP_HIGH
        A = RAW_PRICE_MULTIPLIER
        N = NUM_CONSUMERS
        M = self.material_pool
        C = 1 + self.competition
        l_p = self.production_cost_per_unit()

        beta = (1.2 * N) / C
        zeta = self.raw_material.remaining - beta + self.material_pool

        # Define best price and profit to be 0 (case 1.2 and worst case)
        best_price = b
        best_profit = 0

        # First try case 1.0 from report (q(p) <= M))
        price = (b + l_p)/2
        profit = self.test_price(price)
        if profit is not None and profit > best_profit:
            best_price = price
            best_profit = profit

        # Try case 1.3 from report
        price = b * (1 - M/beta)
        profit = self.test_price(price)
        if profit is not None and profit > best_profit:
            best_price = price
            best_profit = profit

        # Try case 2.0 from report (q(p) > M)
        quad_a = -2 * beta
        quad_b = beta * b + beta * l_p - 2 * zeta * b
        quad_c = zeta * b**2 + zeta * b * l_p + A * b
        p1, p2 = utils.quadratic_solver(quad_a, quad_b, quad_c)
        for price in [p1, p2]:
            profit = self.test_price(price)
            if profit is not None and profit > best_profit:
                best_price = price
                best_profit = profit


        # price1, quantity1 = self.hyperopt_price_optimizer(with_quantity=True)

        # price1 *= PRICE_CAP_HIGH
        # quantity1 *= NUM_CONSUMERS * 1.2

        # price2, _ = self.hyperopt_price_optimizer()
        # price2 *= PRICE_CAP_HIGH
        # quantity2 = beta * (1 - price2 / b)
        
        self.price = best_price
        self.quantity = int(beta * (1 - best_price / b))

        # profits1, profits2, profits3 = self.test_price(price1, quantity1), self.test_price(price2, quantity2), self.test_price(best_price, self.quantity)

        # self.sol1_prices.append(price1)
        # self.sol2_prices.append(price2)
        # self.sol3_prices.append(best_price)

        # self.sol1_quants.append(quantity1)
        # self.sol2_quants.append(quantity2)
        # self.sol3_quants.append(self.quantity)

        # self.sol1_profits.append(profits1)
        # self.sol2_profits.append(profits2)
        # self.sol3_profits.append(profits3)

        # print("Profits", self.test_price(self.price), self.test_price(price1), self.test_price(price2))
        # print("Prices", self.price, price1, price2)
        # print("Quantities", self.quantity, quantity1, quantity2)
        # print(quantity, self.quantity)

    def test_price(self, p, q=None, hyperopt=False):

        if hyperopt:
            p *= PRICE_CAP_HIGH
            if q is not None:
                q *= NUM_CONSUMERS * 1.2

        if p < PRICE_CAP_LOW or p > PRICE_CAP_HIGH:
            return -float('inf')
        
        if q is not None and q < 0:
            return -float('inf')

        b = PRICE_CAP_HIGH
        N = NUM_CONSUMERS
        C = 1 + self.competition
    
        beta = (1.2 * N) / C
        # beta = N
        if q is None:
            q = beta * (1 - p / b)
    
        s = min(beta * (1 - p / b), q)

        return p * s - self.variable_costs_for_quantity(q, take=False)
    
    def hyperopt_price_optimizer(self, with_quantity=False):
        
        # Define the search space for price and quantity
        space = {
            'price': hp.uniform('price', 0, 1)
        }

        if with_quantity:
            space['quantity'] = hp.uniform('quantity', 0, 1)

        # Define the objective function
        def objective(params):
            if with_quantity:
                price = params['price']
                quantity = params['quantity']
                profit = self.test_price(price, quantity, hyperopt=True)
            else:
                price = params['price']
                profit = self.test_price(price, hyperopt=True)
            return {'loss': -profit, 'status': STATUS_OK}
        
        # Run the optimization
        trials = Trials()
        best = fmin(
            fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=250,  # Number of iterations to search
            trials=trials
        )

        return best['price'], best['quantity'] if with_quantity else None

    def step(self):
        pass

        


        