from mesa import Agent
import random
import numpy as np

class ConsumerAgent(Agent):

    def __init__(self, model, price_cap, ecolevel=0, competition=True, spatial=False):
        """
        Initializes a new consumer agent. 
        """
        super().__init__(model)
        self.price_cap = price_cap
        self.ecolevel = ecolevel
        # self.ecolevel = ecolevel
        self.spatial = spatial
        self.competition = competition
        self.last_company = None
        self.companies = self.model.companies

    def normalized_price(self):
        """
        Normalizes the prices of the companies with the min-max normalization method.
        """
        min_price = min([company.price for company in self.companies])
        max_price = max([company.price for company in self.companies])

        # min max normalization
        if max_price == min_price:
            return [0 
                if company.products > 0 and company.price <= self.price_cap else None 
                for company in self.companies
            ]
        
        return [
            (company.price - min_price) / (max_price - min_price) 
                if company.products > 0 and company.price <= self.price_cap else None
                for company in self.companies
        ]
    
    def get_companies_within_range(self, range_limit=25):
        """
        Get companies within a certain range of the consumer.
        """
        grid = self.model.grid

        neighborhood = grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=range_limit)
        nearby_companies = [
            agent for cell in neighborhood 
            for agent in grid.get_cell_list_contents(cell) 
            if not isinstance(agent, ConsumerAgent)
        ]
        self.companies = nearby_companies

    def get_value_scores(self):
        """
        Calculate the value scores of the companies based on the ecolevel of the consumer.
        """
        normalized_prices = self.normalized_price()

        return [
            self.ecolevel * company.circularity - (1 - self.ecolevel) * norm_price
            if norm_price is not None else -float('inf')
            for company, norm_price in zip(self.companies, normalized_prices)
        ]

    def monopoly_step(self):
        """
        Monopoly step where the consumer buys from all companies that meet the price cap.
        """
        for company in self.companies:
            if company.price <= self.price_cap and company.products > 0:
                company.sell()

    def competition_step(self):
        """
        Competition step where the consumer buys from a singular company based on the value scores. The company is chosen based on a softmax function with the value scores as input to determine the probabilities.
        """
        if self.companies == []:
            return

        # Sort companies by value
        value_scores = self.get_value_scores() 

        # Filter out companies with invalid scores
        valid_companies = [
            (company, score) for company, score in zip(self.companies, value_scores) 
            if score > -float('inf')
        ]

        if not valid_companies:
            return  # No valid companies to buy from

        companies, scores = zip(*valid_companies)
        
        # Softmax function to calculate probabilities
        exp_scores = np.exp(scores - np.max(scores))  # For numerical stability
        probabilities = exp_scores / exp_scores.sum()

        # Randomly choose a company based on probabilities
        chosen_company = random.choices(companies, weights=probabilities, k=1)[0]

        # print(chosen_company, chosen_company.circularity if chosen_company else None)

        if chosen_company.price <= self.price_cap and chosen_company.products > 0:
            chosen_company.sell()
            self.last_company = chosen_company   

    def step(self):
        """
        Consumer step. If competition is turned off, the consumer buys from all companies that meet the price cap. If competition is turned on, the consumer buys from a singular company based on the value scores.
        """
        if not self.competition:
            self.companies = self.model.companies
            self.monopoly_step()
                    
        else:
            if self.spatial:
                if self.companies is None:
                    self.get_companies_within_range()
                self.competition_step()
            else:
                self.companies = self.model.companies
                self.competition_step()
        
            