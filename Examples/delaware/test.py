# test.py
# Author: Tristan Brigham
# Date: 2025-06-09
# Description: This file is used to test the delaware example.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# import the necessary libraries
from World_Sim.Agent import Agent
from World_Sim.Labor import Labor

# we create an agent for every voter in delaware according to the L2 data
