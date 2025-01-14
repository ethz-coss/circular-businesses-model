def get_remaining_resources(self):
        return [company.raw_material.remaining for company in self.companies]
    
def get_current_costs(self):
    return [company.raw_material.get_current_cost() for company in self.companies]

def get_profits(self):
    return [company.money for company in self.companies]

def get_unsold_waste(self):
    return [company.get_unsold_waste() for company in self.companies]

def get_material_pools(self):
    for company in self.companies:
        if company.material_pool < 0:
            raise ValueError("Material pool is negative")
    return [company.material_pool for company in self.companies]

def get_prices(self):
    return [company.price if company.quantity > 0 else None for company in self.companies]

def get_quantities(self):
    return [company.quantity if company.quantity > 0 else None for company in self.companies]

def get_production_costs(self):
    return [company.production_cost_per_unit() for company in self.companies]

def get_maintenance_costs(self):
    return [company.fixed_costs_per_year() for company in self.companies]

def get_avg_cost_per_product(self):
    return [company.avg_cost_per_product for company in self.companies]

def get_total_material_purchased(self):
    return [company.total_material_purchased for company in self.companies]

def get_amount_sold(self):
    return [company.quantity - company.products for company in self.companies]