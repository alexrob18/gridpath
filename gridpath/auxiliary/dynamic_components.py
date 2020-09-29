#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

"""
This module creates the DynamicComponents class, which contains the lists and
dictionaries of the names of dynamic optimization components. These are
components that are populated by GridPath modules based on the selected
features and the scenario input data.
"""

from builtins import object

# Create global variables for the dynamic component names, so that we can
# more easily import the correct names into other modules
capacity_type_operational_period_sets = "capacity_type_operational_period_sets"
storage_only_capacity_type_operational_period_sets = \
    "storage_only_capacity_type_operational_period_sets"

headroom_variables = "headroom_variables"
footroom_variables = "footroom_variables"
reserve_variable_derate_params = "reserve_variable_derate_params"
reserve_to_energy_adjustment_params = \
    "reserve_to_energy_adjustment_params"

prm_cost_group_sets = "prm_cost_groups"
prm_cost_group_prm_type = "prm_cost_group_prm_type"

tx_capacity_type_operational_period_sets = \
    "tx_capacity_type_operational_period_sets"

load_balance_production_components = "load_balance_production_components"
load_balance_consumption_components = "load_balance_consumption_components"

carbon_cap_balance_emission_components = \
    "carbon_cap_balance_emission_components"

prm_balance_provision_components = \
    "prm_balance_provision_components"
local_capacity_balance_provision_components = \
    "local_capacity_balance_provision_components"

total_cost_components = "total_cost_components"


class DynamicComponents(object):
    """
    Here we initialize the class object and its components that will contain
    the dynamic model components, i.e. lists and dictionary with the names
    of the optimization components that are populated based on whether features
    are selected (i.e. certain modules are called) and based on the scenario
    input data.
    """
    def __init__(self):
        """
        Initialize the dynamic components.
        """

        # ### Project sets and variables ### #
        # These are the names of the sets of project-operational_period by
        # capacity type;
        # The sets will be joined to make the final
        # project-operational_period set that includes all projects
        # If called, the capacity-type modules will populate these lists with
        # the name of the respective set for the capacity type
        setattr(self, capacity_type_operational_period_sets, list())
        setattr(self, storage_only_capacity_type_operational_period_sets,
                list())

        # PRM cost groups
        setattr(self, prm_cost_group_sets, list())
        setattr(self, prm_cost_group_prm_type, dict())

        # ### Operating reserves ### #
        # Headroom and footroom variables
        # These will include the project as keys and a list as value for
        # each project; the list could be empty if the project is not
        # providing any reserves, or will include the names of the
        # respective reserve-provision variable if the reserve-type is
        # modeled and a project can provide it
        setattr(self, headroom_variables, dict())
        setattr(self, footroom_variables, dict())

        # A reserve-provision derate parameter and a
        # reserve-to-energy-adjustment parameter could also be assigned to
        # project, so we make dictionaries that will link the
        # reserve-provision variable names to a derate-param name (i.e. the
        # regulation up variable will be linked to a regulation-up
        # parameter, the spinning-reserves variable will be linked to a
        # spinning reserves paramater, etc.)
        setattr(self, reserve_variable_derate_params, dict())
        setattr(self, reserve_to_energy_adjustment_params, dict())

        # ### Transmission sets and variables ### #
        setattr(self, tx_capacity_type_operational_period_sets, list())

        # ### Constraint and objective function components ### #
        # Load balance constraint
        # Modules will add component names to these lists
        setattr(self, load_balance_production_components, list())
        setattr(self, load_balance_consumption_components, list())

        # Carbon cap constraint
        # Modules will add component names to these lists
        setattr(self, carbon_cap_balance_emission_components, list())

        # PRM constraint
        # Modules will add component names to this list
        setattr(self, prm_balance_provision_components, list())

        # Local capacity constraint
        # Modules will add component names to this list
        setattr(self, local_capacity_balance_provision_components, list())

        # Objective function
        # Modules will add component names to this list
        setattr(self, total_cost_components, list())
