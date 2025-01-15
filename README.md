

# Agent-Based Modelling for the Transition to a Circular Economy: Addressing Market Dynamics and Policy Interventions

## Description

In this agent-based model, I aim to model circular practices in businesses. I specifically focus on the area of non-renewable and finite resources. I use the idea of a material pool to represent the reuse, recycling, repairing, and refurbishing of raw materials within the business. I assume a profit-maximization strategy by the companies and look at how different regulatory policies and consumer preferences impact the choices the effects on the profit of the businesses. I also look at the spatial implications on such a model, when the businesses are located throughout space. 

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Feature 1: "Monopolistic" setup - each company has access to its own set of raw resources and there is no competition in the market.
- Feature 2: "Competitive" setup - each company shares access to one set of raw resources and there is competition in the market.
- Feature 3: "Spatial" influence - here I look at the effect of spatial dynamics in the competitive market. I consider both cases in which everyone in the space shares the same resources as well as when there are different resources in each zone.

## Installation

### Prerequisites

- The `requirements.txt` file contains all libraries required.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ethz-coss/circular-businesses-model.git
   cd circular-businesses-model
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Update the `parameters.txt` file with desired parameters
4. Run the `main.py` file.
