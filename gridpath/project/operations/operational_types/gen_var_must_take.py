#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.

"""
This operational type is like the *gen_var* type with two main differences.
First, the project's output is must-take, i.e. curtailment (dispatch down) is
not allowed. Second, because the project's output is not controllable, projects
of this operational type cannot provide operational reserves .
"""

import csv
import os.path
from pyomo.environ import Param, Set, NonNegativeReals, Constraint
import warnings

from gridpath.auxiliary.auxiliary import generator_subset_init, \
    write_validation_to_database, get_projects_by_reserve, \
    check_projects_for_reserves
from gridpath.auxiliary.dynamic_components import headroom_variables, \
    footroom_variables
from gridpath.project.common_functions import \
    check_if_linear_horizon_first_timepoint
from gridpath.project.operations.operational_types.common_functions import \
    load_var_profile_inputs, get_var_profile_inputs_from_database, \
    write_tab_file_model_inputs


def add_module_specific_components(m, d):
    """
    The following Pyomo model components are defined in this module:

    +-------------------------------------------------------------------------+
    | Sets                                                                    |
    +=========================================================================+
    | | :code:`GEN_VAR_MUST_TAKE`                                             |
    |                                                                         |
    | The set of generators of the :code:`gen_var_must_take` operational type.|
    +-------------------------------------------------------------------------+
    | | :code:`GEN_VAR_MUST_TAKE_OPR_TMPS`                                    |
    |                                                                         |
    | Two-dimensional set with generators of the :code:`gen_var_must_take`    |
    | operational type and their operational timepoints.                      |
    +-------------------------------------------------------------------------+

    |

    +-------------------------------------------------------------------------+
    | Required Input Params                                                   |
    +=========================================================================+
    | | :code:`gen_var_must_take_cap_factor`                                  |
    | | *Defined over*: :code:`GEN_VAR_MUST_TAKE`                             |
    | | *Within*: :code:`NonNegativeReals`                                    |
    |                                                                         |
    | The project's power output in each operational timepoint as a fraction  |
    | of its available capacity (i.e. the capacity factor).                   |
    +-------------------------------------------------------------------------+

    |

    +-------------------------------------------------------------------------+
    | Constraints                                                             |
    +=========================================================================+
    | | :code:`GenVarMustTake_No_Upward_Reserves_Constraint`                  |
    | | *Defined over*: :code:`GEN_VAR_MUST_TAKE_OPR_TMPS`                    |
    |                                                                         |
    | Variable must-take generator projects cannot provide upward reserves.   |
    +-------------------------------------------------------------------------+
    | | :code:`GenVarMustTake_No_Downward_Reserves_Constraint`                |
    | | *Defined over*: :code:`GEN_VAR_MUST_TAKE_OPR_TMPS`                    |
    |                                                                         |
    | Variable must-take generator projects cannot provide downward reserves. |
    +-------------------------------------------------------------------------+


    """

    # Sets
    ###########################################################################

    m.GEN_VAR_MUST_TAKE = Set(
        within=m.PROJECTS,
        initialize=generator_subset_init("operational_type",
                                         "gen_var_must_take")
    )

    m.GEN_VAR_MUST_TAKE_OPR_TMPS = Set(
        dimen=2, within=m.PRJ_OPR_TMPS,
        rule=lambda mod:
        set((g, tmp) for (g, tmp) in mod.PRJ_OPR_TMPS
            if g in mod.GEN_VAR_MUST_TAKE)
    )

    # Required Params
    ###########################################################################

    # TODO: allow cap factors greater than 1, but throw a warning?
    m.gen_var_must_take_cap_factor = Param(
        m.GEN_VAR_MUST_TAKE_OPR_TMPS,
        within=NonNegativeReals
    )

    # Constraints
    ###########################################################################

    # TODO: remove this constraint once input validation is in place that
    #  does not allow specifying a reserve_zone if 'gen_var_must_take' type
    def no_upward_reserve_rule(mod, g, tmp):
        """
        **Constraint Name**: GenVarMustTake_No_Upward_Reserves_Constraint
        **Enforced Over**: GEN_VAR_MUST_TAKE_OPR_TMPS

        Upward reserves should be zero in every operational timepoint.
        """
        if getattr(d, headroom_variables)[g]:
            warnings.warn(
                """project {} is of the 'gen_var_must_take' operational 
                type and should not be assigned any upward reserve BAs since it 
                cannot provide  upward reserves. Please replace the upward 
                reserve BA for project {} with '.' (no value) in projects.tab. 
                Model will add  constraint to ensure project {} cannot provide 
                upward reserves
                """.format(g, g, g)
            )
            return sum(getattr(mod, c)[g, tmp]
                       for c in getattr(d, headroom_variables)[g]) == 0
        else:
            return Constraint.Skip

    m.GenVarMustTake_No_Upward_Reserves_Constraint = Constraint(
        m.GEN_VAR_MUST_TAKE_OPR_TMPS,
        rule=no_upward_reserve_rule
    )

    # TODO: remove this constraint once input validation is in place that
    #  does not allow specifying a reserve_zone if 'gen_var_must_take' type
    def no_downward_reserve_rule(mod, g, tmp):
        """
        **Constraint Name**: GenVarMustTake_No_Downward_Reserves_Constraint
        **Enforced Over**: GEN_VAR_MUST_TAKE_OPR_TMPS

        Downward reserves should be zero in every operational timepoint.
        """
        if getattr(d, footroom_variables)[g]:
            warnings.warn(
                """project {} is of the 'gen_var_must_take' operational 
                type and should not be assigned any downward reserve BAs since 
                it cannot provide downward reserves. Please replace the
                downward reserve BA for project {} with '.' (no value) in 
                projects.tab. Model will add constraint to ensure project {} 
                cannot provide downward reserves.
                """.format(g, g, g)
            )
            return sum(getattr(mod, c)[g, tmp]
                       for c in getattr(d, footroom_variables)[g]) == 0
        else:
            return Constraint.Skip

    m.GenVarMustTake_No_Downward_Reserves_Constraint = Constraint(
        m.GEN_VAR_MUST_TAKE_OPR_TMPS,
        rule=no_downward_reserve_rule
    )


# Operational Type Methods
###############################################################################

def power_provision_rule(mod, g, tmp):
    """
    Power provision from variable must-take generators is their capacity times
    the capacity factor in each timepoint.
    """

    return mod.Capacity_MW[g, mod.period[tmp]] \
        * mod.Availability_Derate[g, tmp] \
        * mod.gen_var_must_take_cap_factor[g, tmp]


def online_capacity_rule(mod, g, tmp):
    """
    Since there is no commitment, all capacity is assumed to be online.
    """
    return mod.Capacity_MW[g, mod.period[tmp]] \
        * mod.Availability_Derate[g, tmp]


def rec_provision_rule(mod, g, tmp):
    """
    REC provision from variable must-take generators is the same as power
    provision: their capacity times the capacity factor in each timepoint.
    """

    return mod.Capacity_MW[g, mod.period[tmp]] \
        * mod.Availability_Derate[g, tmp] \
        * mod.gen_var_must_take_cap_factor[g, tmp]


def scheduled_curtailment_rule(mod, g, tmp):
    """
    No curtailment allowed for must-take variable generators.
    """
    return 0


def subhourly_curtailment_rule(mod, g, tmp):
    """
    Can't provide downward reserves, so no sub-hourly curtailment.
    """
    return 0


def subhourly_energy_delivered_rule(mod, g, tmp):
    """
    Can't provide upward reserves, so no sub-hourly energy delivered.
    """
    return 0


def fuel_burn_rule(mod, g, tmp):
    """
    Variable generators should not have fuel use.
    """
    if g in mod.FUEL_PRJS:
        raise ValueError(
            "ERROR! Variable projects should not use fuel." + "\n" +
            "Check input data for project '{}'".format(g) + "\n" +
            "and change its fuel to '.' (no value)."
        )
    else:
        return 0


def variable_om_cost_rule(mod, g, tmp):
    """
    """
    return mod.Capacity_MW[g, mod.period[tmp]] \
        * mod.Availability_Derate[g, tmp] \
        * mod.gen_var_must_take_cap_factor[g, tmp] \
        * mod.variable_om_cost_per_mwh[g]


def startup_cost_rule(mod, g, tmp):
    """
    Since there is no commitment, there is no concept of starting up.
    """
    return 0


def shutdown_cost_rule(mod, g, tmp):
    """
    Since there is no commitment, there is no concept of shutting down.
    """
    return 0


def startup_fuel_burn_rule(mod, g, tmp):
    """
    Since there is no commitment, there is no concept of starting up.
    """
    return 0


def power_delta_rule(mod, g, tmp):
    """
    Exogenously defined ramp for variable must-take generators.
    """
    if check_if_linear_horizon_first_timepoint(
        mod=mod, tmp=tmp, balancing_type=mod.balancing_type_project[g]
    ):
        pass
    else:
        return \
            (mod.Capacity_MW[g, mod.period[tmp]]
             * mod.Availability_Derate[g, tmp]
             * mod.gen_var_must_take_cap_factor[g, tmp]) \
            - (mod.Capacity_MW[g, mod.period[mod.prev_tmp[
                    tmp, mod.balancing_type_project[g]]]]
               * mod.Availability_Derate[g, mod.prev_tmp[
                    tmp, mod.balancing_type_project[g]]]
               * mod.gen_var_must_take_cap_factor[g, mod.prev_tmp[
                    tmp, mod.balancing_type_project[g]]])


# Inputs-Outputs
###############################################################################

def load_module_specific_data(mod, data_portal,
                              scenario_directory, subproblem, stage):
    """
    :param mod:
    :param data_portal:
    :param scenario_directory:
    :param subproblem:
    :param stage:
    :return:
    """

    load_var_profile_inputs(
        data_portal, scenario_directory, subproblem, stage, "gen_var_must_take"
    )


# Database
###############################################################################

def get_module_specific_inputs_from_database(
        subscenarios, subproblem, stage, conn
):
    """
    :param subscenarios: SubScenarios object with all subscenario info
    :param subproblem:
    :param stage:
    :param conn: database connection
    :return: cursor object with query results
    """
    return get_var_profile_inputs_from_database(
        subscenarios, subproblem, stage, conn, "gen_var_must_take"
    )


def write_module_specific_model_inputs(
        scenario_directory, subscenarios, subproblem, stage, conn
):
    """
    Get inputs from database and write out the model input
    variable_generator_profiles.tab file.
    :param scenario_directory: string, the scenario directory
    :param subscenarios: SubScenarios object with all subscenario info
    :param subproblem:
    :param stage:
    :param conn: database connection
    :return:
    """

    data = get_module_specific_inputs_from_database(
        subscenarios, subproblem, stage, conn)
    fname = "variable_generator_profiles.tab"

    write_tab_file_model_inputs(
        scenario_directory, subproblem, stage, fname, data
    )


# Validation
###############################################################################

def validate_module_specific_inputs(subscenarios, subproblem, stage, conn):
    """
    Get inputs from database and validate the inputs
    :param subscenarios: SubScenarios object with all subscenario info
    :param subproblem:
    :param stage:
    :param conn: database connection
    :return:
    """

    validation_results = []

    # TODO: validate timepoints: make sure timepoints specified are consistent
    #   with the temporal timepoints (more is okay, less is not)
    # variable_profiles = get_module_specific_inputs_from_database(
    #     subscenarios, subproblem, stage, conn)

    # Get list of gen_var_must_take projects
    c = conn.cursor()
    var_projects = c.execute(
        """SELECT project
        FROM inputs_project_portfolios
        INNER JOIN
        (SELECT project, operational_type
        FROM inputs_project_operational_chars
        WHERE project_operational_chars_scenario_id = {}) as prj_chars
        USING (project)
        WHERE project_portfolio_scenario_id = {}
        AND operational_type = '{}'""".format(
            subscenarios.PROJECT_OPERATIONAL_CHARS_SCENARIO_ID,
            subscenarios.PROJECT_PORTFOLIO_SCENARIO_ID,
            "gen_var_must_take"
        )
    )
    var_projects = [p[0] for p in var_projects.fetchall()]

    # Check that the project does not show up in any of the
    # inputs_project_reserve_bas tables since gen_var_must_take can't
    # provide any reserves
    projects_by_reserve = get_projects_by_reserve(subscenarios, conn)
    for reserve, projects in projects_by_reserve.items():
        project_ba_id = "project_" + reserve + "_ba_scenario_id"
        table = "inputs_project_" + reserve + "_bas"
        validation_errors = check_projects_for_reserves(
            projects_op_type=var_projects,
            projects_w_ba=projects,
            operational_type="gen_var_must_take",
            reserve=reserve
        )
        for error in validation_errors:
            validation_results.append(
                (subscenarios.SCENARIO_ID,
                 subproblem,
                 stage,
                 __name__,
                 project_ba_id.upper(),
                 table,
                 "Mid",
                 "Invalid {} BA inputs".format(reserve),
                 error
                 )
            )

    # Write all input validation errors to database
    write_validation_to_database(validation_results, conn)
