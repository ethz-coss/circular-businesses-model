from mesa import Agent
import random
import numpy as np

class ConsumerAgent(Agent):

    def __init__(self, model, price_cap, cheapness=1, ecolevel=0, competition=True, spatial=False):
        super().__init__(model)
        self.price_cap = price_cap
        self.cheapness = cheapness
        # self.ecolevel = ecolevel
        self.spatial = spatial
        self.competition = competition
        self.last_company = None
        self.companies = self.model.companies

    def normalized_price(self):
            
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
        grid = self.model.grid

        neighborhood = grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=range_limit)
        nearby_companies = [
            agent for cell in neighborhood 
            for agent in grid.get_cell_list_contents(cell) 
            if not isinstance(agent, ConsumerAgent)
        ]
        self.companies = nearby_companies

    def get_value_scores(self):

        normalized_prices = self.normalized_price()

        return [
            (1 - self.cheapness) * company.circularity - self.cheapness * norm_price
            if norm_price is not None else -float('inf')
            for company, norm_price in zip(self.companies, normalized_prices)
        ]

    def monopoly_step(self):
        for company in self.companies:
            if company.price <= self.price_cap and company.products > 0:
                company.sell()

    def competition_step(self):

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
        
            