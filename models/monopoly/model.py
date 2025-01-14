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

PRICE_CAP_LOW = parameters.PRICE_CAP_LOW
PRICE_CAP_HIGH = parameters.PRICE_CAP_HIGH

class CircularEconomyModel(Model):


    def __init__(self, n=1000, width=100, height=100, seed=None):

        super().__init__(seed=seed)

        self.num_agents = n
        self.grid = MultiGrid(width, height, torus=True)

        # Create companies
        self.companies = [
            CompanyAgent(self, raw_material=RawMaterial(), circularity=0), 
            CompanyAgent(self, raw_material=RawMaterial(), circularity=0.2),
            CompanyAgent(self, raw_material=RawMaterial(), circularity=0.4),
            CompanyAgent(self, raw_material=RawMaterial(), circularity=0.6),
            CompanyAgent(self, raw_material=RawMaterial(), circularity=0.8)
        ]

        # Create and place the consumers
        for _ in range(self.num_agents):
            price_cap = random.uniform(PRICE_CAP_LOW, PRICE_CAP_HIGH)
            agent = ConsumerAgent(self, price_cap, competition=False)

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
        order = self.random_permutation(0, 5)
        for number in order:
            self.companies[number].year_start()
        self.agents.shuffle_do("step")
        for number in order:
            self.companies[number].year_end()
        self.datacollector.collect(self)
