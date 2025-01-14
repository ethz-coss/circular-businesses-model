import importlib

from mesa import Model
from mesa.datacollection import DataCollector
from agents.company import CompanyAgent
from agents.consumer import ConsumerAgent
from my_environment.raw_material import RawMaterial
import parameters
importlib.reload(parameters)
from mesa.space import MultiGrid
import random

from parameters import PRICE_CAP_LOW, PRICE_CAP_HIGH, NUM_COMPANIES, NUM_CONSUMERS

# Import functions from the new file
from models.common import (
    get_remaining_resources,
    get_current_costs,
    get_profits,
    get_unsold_waste,
    get_material_pools,
    get_prices,
    get_quantities,
    get_production_costs,
    get_maintenance_costs,
    get_avg_cost_per_product,
    get_total_material_purchased,
    get_amount_sold
)

class CircularEconomyModel(Model):


    def __init__(self, n=NUM_CONSUMERS, width=100, height=100, seed=None):

        super().__init__(seed=seed)

        self.num_agents = n
        self.grid = MultiGrid(width, height, torus=True)

        raw_material = RawMaterial()

        # Create companies
        self.companies = [
            CompanyAgent(self, raw_material=raw_material, circularity=0, competition=NUM_COMPANIES-1), 
            CompanyAgent(self, raw_material=raw_material, circularity=0.2, competition=NUM_COMPANIES-1),
            CompanyAgent(self, raw_material=raw_material, circularity=0.4, competition=NUM_COMPANIES-1),
            CompanyAgent(self, raw_material=raw_material, circularity=0.6, competition=NUM_COMPANIES-1),
            CompanyAgent(self, raw_material=raw_material, circularity=0.8, competition=NUM_COMPANIES-1)
        ]

        # Create and place the consumers
        for _ in range(self.num_agents):
            price_cap = random.uniform(PRICE_CAP_LOW, PRICE_CAP_HIGH)
            cheapness = random.uniform(0, 1)
            # ecolevel = random.uniform(0, 0.5)
            agent = ConsumerAgent(self, price_cap, cheapness)

            # Add agent to random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Data collector
        self.datacollector = DataCollector(
            model_reporters={
                "Profits": get_profits,
                "Prices": get_prices,
                "Quantities": get_quantities,
                "Waste": get_unsold_waste,
                "Remaining Resources": get_remaining_resources,
                "Material Pools": get_material_pools,
                "Resource Costs": get_current_costs,
                "Production Costs": get_production_costs,
                "Maintenance Costs": get_maintenance_costs,
                "Avg Cost Per Product": get_avg_cost_per_product,
                "Total Material Purchased": get_total_material_purchased,
                "Amount Sold": get_amount_sold
            }
        )

    def random_permutation(self, min_value, max_value):
        numbers = list(range(min_value, max_value))
        random.shuffle(numbers)
        return numbers

    def step(self):
        order = self.random_permutation(0, NUM_COMPANIES)
        for number in order:
            self.companies[number].year_start()
        self.agents.shuffle_do("step")
        for number in order:
            self.companies[number].year_end()
        self.datacollector.collect(self)