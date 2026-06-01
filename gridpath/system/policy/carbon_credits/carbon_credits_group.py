# Copyright 2016-2023 Blue Marble Analytics LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Minimum and maximum credits purchase by period and carbon credit groups.
"""

import csv
import os.path
import pandas as pd
from pyomo.environ import Set, Param, Constraint, NonNegativeReals, Expression, value

from gridpath.auxiliary.auxiliary import get_required_subtype_modules
from gridpath.common_functions import duals_wrapper, none_dual_type_error_wrapper
from gridpath.auxiliary.db_interface import import_csv, directories_to_db_values


def add_model_components(
    m,
    d,
    scenario_directory,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
):
    """
    The following Pyomo model components are defined in this module:

    +-------------------------------------------------------------------------+
    | Sets                                                                    |
    +=========================================================================+
    | | :code:`CARBON_CREDITS_GROUP_PERIODS`                                  |
    |                                                                         |
    | A two-dimensional set of group-period combinations for which there may  |
    | be group carbon credits requirements.                                   |
    +-------------------------------------------------------------------------+
    | | :code:`CARBON_CREDITS_GROUPS`                                         |
    |                                                                         |
    | The groups of projects for which there may be group of carbon credits   |
    | requirements.                                                           |
    +-------------------------------------------------------------------------+
    | | :code:`CARBON_CREDITS_IN_CARBON_CREDITS_GROUPS`                       |
    |                                                                         |
    | The list of carbon credits by carbon credits group.                     |
    +-------------------------------------------------------------------------+

    +-------------------------------------------------------------------------+
    | Optional Input Params                                                   |
    +=========================================================================+
    | | :code:`carbon_credits_group_buy_min`                               |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                        |
    | | *Within*: :code:`NonNegativeReals`                                    |
    | | *Default*: :code:`0`                                                  |
    |                                                                         |
    | The minimum amount of credits (in Mt CO2) that can be purchase          |
    | in this group in a given period.                                        |
    +-------------------------------------------------------------------------+
    | | :code:`carbon_credits_group_buy_max`                                  |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    | | *Within*: :code:`NonNegativeReals`                                    |
    | | *Default*: :code:`inf`                                                |
    |                                                                         |
    | The maximum amount of credits (in Mt CO2) that can be purchase          |
    | in this group in a given period.                                        |
    +-------------------------------------------------------------------------+
    | | :code:`carbon_credits_group_sell_min`                                 |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    | | *Within*: :code:`NonNegativeReals`                                    |
    | | *Default*: :code:`0`                                                  |
    |                                                                         |
    | The minimum amount of credits (in Mt CO2) that can be sold              |
    | in this group in a given period.                                        |
    +-------------------------------------------------------------------------+
    | | :code:`carbon_credits_group_sell_max`                                 |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    | | *Within*: :code:`NonNegativeReals`                                    |
    | | *Default*: :code:`inf`                                                |
    |                                                                         |
    | The maximum amount of credits (in Mt CO2) that can be sold              |
    | in this group in a given period.                                        |
    +-------------------------------------------------------------------------+

    |

    +-------------------------------------------------------------------------+
    | Expressions                                                             |
    +=========================================================================+
    | | :code:`Group_Carbon_Credits_Buy_in_Period `                            |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | The Carbon credits purchased in this group in this period.              |
    +-------------------------------------------------------------------------+
    | | :code:`Group_Carbon_Credits_Sell_in_Period `                           |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | The Carbon credits sold in this group in this period.                   |
    +-------------------------------------------------------------------------+

    |

    +-------------------------------------------------------------------------+
    | Constraints                                                             |
    +=========================================================================+
    | | :code:`Min_Group_Carbon_Credits_Buy_in_Period_Constraint`             |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | Requires the amount of credits purchased in each group in each period.  |
    +-------------------------------------------------------------------------+
    | | :code:`Max_Group_Carbon_Credits_Buy_in_Period_Constraint`             |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | Limits the amount of credits purchased in each group in each period.    |
    +-------------------------------------------------------------------------+
    | | :code:`Min_Group_Carbon_Credits_Sell_in_Period_Constraint`            |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | Requires the amount of credits sold in each group in each period.       |
    +-------------------------------------------------------------------------+
    | | :code:`Max_Group_Carbon_Credits_Sell_in_Period_Constraint`            |
    | | *Defined over*: :code:`CARBON_CREDITS_GROUP_PERIODS`                  |
    |                                                                         |
    | Limits a certain amount of credits sold  in each group in each period.  |
    +-------------------------------------------------------------------------+

    """

    # Sets
    m.CARBON_CREDITS_GROUP_PERIODS = Set(dimen=2)

    m.CARBON_CREDITS_GROUPS = Set(
        initialize=lambda mod: sorted(
            list(set([g for (g, p) in mod.CARBON_CREDITS_GROUP_PERIODS]))
        )
    )

    m.CARBON_CREDITS_IN_CARBON_CREDITS_GROUPS = Set(m.CARBON_CREDITS_GROUPS, within=m.CARBON_CREDITS_ZONES)

    # Params
    m.carbon_credits_group_buy_min = Param(
        m.CARBON_CREDITS_GROUP_PERIODS, within=NonNegativeReals, default=0
    )
    m.carbon_credits_group_buy_max = Param(
        m.CARBON_CREDITS_GROUP_PERIODS, within=NonNegativeReals, default=float("inf")
    )
    m.carbon_credits_group_sell_min = Param(
        m.CARBON_CREDITS_GROUP_PERIODS, within=NonNegativeReals, default=0
    )
    m.carbon_credits_group_sell_max = Param(
        m.CARBON_CREDITS_GROUP_PERIODS, within=NonNegativeReals, default=float("inf")
    )

    # Expressions
    def group_carbon_credits_buy_in_period_rule(mod, grp, prd):
        return sum(
            mod.Buy_Carbon_Credits[cred_z, prd]
            for cred_z in mod.CARBON_CREDITS_IN_CARBON_CREDITS_GROUPS[grp]
        )

    m.Group_Carbon_Credits_Buy_in_Period = Expression(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=group_carbon_credits_buy_in_period_rule
    )

    def group_carbon_credits_sell_in_period_rule(mod, grp, prd):
        return sum(
            mod.Sell_Carbon_Credits[cred_z, prd]
            for cred_z in mod.CARBON_CREDITS_IN_CARBON_CREDITS_GROUPS[grp]
        )

    m.Group_Carbon_Credits_Sell_in_Period = Expression(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=group_carbon_credits_sell_in_period_rule
    )

    # Constraints
    # Capacity build
    # Limit the min and max amount of new build in a group-period
    m.Max_Group_Carbon_Credits_Buy_in_Period_Constraint = Constraint(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=carbon_credits_group_buy_max_rule
    )

    m.Min_Group_Carbon_Credits_Buy_in_Period_Constraint = Constraint(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=carbon_credits_group_buy_min_rule
    )

    # Limit the min and max amount of total capacity in a group-period
    m.Max_Group_Carbon_Credits_Sell_in_Period_Constraint = Constraint(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=carbon_credits_group_sell_max_rule
    )

    m.Min_Group_Carbon_Credits_Sell_in_Period_Constraint = Constraint(
        m.CARBON_CREDITS_GROUP_PERIODS, rule=carbon_credits_group_sell_min_rule
    )


# Constraint Formulation Rules
###############################################################################
def carbon_credits_group_buy_max_rule(mod, grp, prd):
    if mod.carbon_credits_group_buy_max[grp, prd] == float("inf"):
        return Constraint.Feasible
    else:
        return (
            mod.Group_Carbon_Credits_Buy_in_Period[grp, prd]
            <= mod.carbon_credits_group_buy_max[grp, prd]
        )


def carbon_credits_group_buy_min_rule(mod, grp, prd):
    if mod.carbon_credits_group_buy_min[grp, prd] == 0:
        return Constraint.Feasible
    else:
        return (
            mod.Group_Carbon_Credits_Buy_in_Period[grp, prd]
            >= mod.carbon_credits_group_buy_min[grp, prd]
        )


def carbon_credits_group_sell_max_rule(mod, grp, prd):
    if mod.carbon_credits_group_sell_max[grp, prd] == float("inf"):
        return Constraint.Feasible
    else:
        return (
            mod.Group_Carbon_Credits_Sell_in_Period[grp, prd]
            <= mod.carbon_credits_group_sell_max[grp, prd]
        )


def carbon_credits_group_sell_min_rule(mod, grp, prd):
    if mod.carbon_credits_group_sell_min[grp, prd] == 0:
        return Constraint.Feasible
    else:
        return (
            mod.Group_Carbon_Credits_Sell_in_Period[grp, prd]
            >= mod.carbon_credits_group_sell_min[grp, prd]
        )


# Input-Output
###############################################################################


def load_model_data(
    m,
    d,
    data_portal,
    scenario_directory,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
):
    """ """
    # Only load data if the input files were written; otehrwise, we won't
    # initialize the components in this module

    req_file = os.path.join(
        scenario_directory,
        weather_iteration,
        hydro_iteration,
        availability_iteration,
        subproblem,
        stage,
        "inputs",
        "carbon_credits_group_requirements.tab",
    )
    if os.path.exists(req_file):
        data_portal.load(
            filename=req_file,
            index=m.CARBON_CREDITS_GROUP_PERIODS,
            param=(
                m.carbon_credits_group_buy_min,
                m.carbon_credits_group_buy_max,
                m.carbon_credits_group_sell_min,
                m.carbon_credits_group_sell_max,
            ),
        )

    prj_file = os.path.join(
        scenario_directory,
        weather_iteration,
        hydro_iteration,
        availability_iteration,
        subproblem,
        stage,
        "inputs",
        "carbon_credits_group_credits_zone.tab",
    )
    if os.path.exists(prj_file):
        cred_groups_df = pd.read_csv(prj_file, delimiter="\t")
        cred_groups_dict = {
            g: v["carbon_credits_zone"].tolist()
            for g, v in cred_groups_df.groupby("carbon_credits_group")
        }
        data_portal.data()["CARBON_CREDITS_IN_CARBON_CREDITS_GROUPS"] = cred_groups_dict


def export_results(
    scenario_directory,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
    m,
    d,
):
    """ """
    req_file = os.path.join(
        scenario_directory,
        weather_iteration,
        hydro_iteration,
        availability_iteration,
        subproblem,
        stage,
        "inputs",
        "carbon_credits_group_requirements.tab",
    )
    prj_file = os.path.join(
        scenario_directory,
        weather_iteration,
        hydro_iteration,
        availability_iteration,
        subproblem,
        stage,
        "inputs",
        "carbon_credits_group_credits_zone.tab",
    )

    if os.path.exists(req_file) and os.path.exists(prj_file):
        with open(
            os.path.join(
                scenario_directory,
                weather_iteration,
                hydro_iteration,
                availability_iteration,
                subproblem,
                stage,
                "results",
                "carbon_credits_group_credits.csv",
            ),
            "w",
            newline="",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "carbon_credits_group",
                    "period",
                    "carbon_credits_group_buy",
                    "carbon_credits_group_sell",
                    "carbon_credits_group_buy_min",
                    "carbon_credits_group_buy_max",
                    "carbon_credits_group_sell_min",
                    "carbon_credits_group_sell_max",
                    "carbon_credits_group_buy_min_dual",
                    "carbon_credits_group_buy_max_dual",
                    "carbon_credits_group_sell_min_dual",
                    "carbon_credits_group_sell_max_dual",
                    "carbon_credits_group_buy_min_marginal_cost",
                    "carbon_credits_group_buy_max_marginal_cost",
                    "carbon_credits_group_sell_min_marginal_cost",
                    "carbon_credits_group_sell_max_marginal_cost",
                ]
            )

            for grp, prd in sorted(m.CAPACITY_GROUP_PERIODS):
                writer.writerow(
                    [
                        grp,
                        prd,
                        value(m.Group_Carbon_Credits_Buy_in_Period[grp, prd]),
                        value(m.Group_Carbon_Credits_Sell_in_Period[grp, prd]),
                        value(m.carbon_credits_group_buy_min[grp, prd]),
                        value(m.carbon_credits_group_buy_max[grp, prd]),
                        value(m.carbon_credits_group_sell_min[grp, prd]),
                        value(m.carbon_credits_group_sell_max[grp, prd]),

                        (
                            duals_wrapper(
                                m,
                                getattr(
                                    m, "Min_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )[grp, prd],
                            )
                            if (grp, prd)
                               in [
                                   idx
                                   for idx in getattr(
                                    m, "Min_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )
                               ]
                            else None
                        ),
                        (
                            duals_wrapper(
                                m,
                                getattr(
                                    m, "Max_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )[grp, prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Max_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                        (
                            duals_wrapper(
                                m,
                                getattr(
                                    m, "Min_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )[grp, prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Min_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                        (
                            duals_wrapper(
                                m,
                                getattr(
                                    m, "Max_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )[grp, prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Max_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                        (
                            none_dual_type_error_wrapper(
                                duals_wrapper(
                                    m,
                                    getattr(
                                        m,
                                        "Min_Group_Carbon_Credits_Buy_in_Period_Constraint",
                                    )[grp, prd],
                                ),
                                m.period_objective_coefficient[prd],
                            )
                            if (grp, prd)
                               in [
                                   idx
                                   for idx in getattr(
                                    m, "Min_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )
                               ]
                            else None
                        ),
                        (
                            none_dual_type_error_wrapper(
                                duals_wrapper(
                                    m,
                                    getattr(
                                        m,
                                        "Max_Group_Carbon_Credits_Buy_in_Period_Constraint",
                                    )[grp, prd],
                                ),
                                m.period_objective_coefficient[prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Max_Group_Carbon_Credits_Buy_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                        (
                            none_dual_type_error_wrapper(
                                duals_wrapper(
                                    m,
                                    getattr(
                                        m,
                                        "Min_Group_Carbon_Credits_Sell_in_Period_Constraint",
                                    )[grp, prd],
                                ),
                                m.period_objective_coefficient[prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Min_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                        (
                            none_dual_type_error_wrapper(
                                duals_wrapper(
                                    m,
                                    getattr(
                                        m,
                                        "Max_Group_Carbon_Credits_Sell_in_Period_Constraint",
                                    )[grp, prd],
                                ),
                                m.period_objective_coefficient[prd],
                            )
                            if (grp, prd)
                            in [
                                idx
                                for idx in getattr(
                                    m, "Max_Group_Carbon_Credits_Sell_in_Period_Constraint"
                                )
                            ]
                            else None
                        ),
                    ]
                )


# Database
###############################################################################


def get_inputs_from_database(
    scenario_id,
    subscenarios,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
    conn,
):
    """
    :param subscenarios: SubScenarios object with all subscenario info
    :param subproblem:
    :param stage:
    :param conn: database connection
    :return:
    """

    c1 = conn.cursor()
    cred_grp_reqs = c1.execute(
        """
        SELECT carbon_credits_group, period,
        carbon_credits_group_buy_min, carbon_credits_group_buy_max,
        carbon_credits_group_sell_min, carbon_credits_group_sell_max,
        FROM inputs_project_capacity_group_requirements
        WHERE carbon_credits_group_requirement_scenario_id = {}
        """.format(
            subscenarios.CARBON_CREDITS_GROUP_REQUIREMENT_SCENARIO_ID
        )
    )

    c2 = conn.cursor()
    cap_grp_prj = c2.execute(
        """
        SELECT carbon_credits_group, carbon_credits_zone
        FROM inputs_carbon_credits_groups
        WHERE carbon_credits_group_scenario_id = {carb_cred_group_id}
        AND carbon_credits_zone in (
            SELECT DISTINCT carbon_credits_zone
            FROM inputs_geography_carbon_credits_zones
            WHERE carbon_credits_zone_scenario_id = {carb_cred_zone_id}
            )
        """.format(
            carb_cred_group_id=subscenarios.CARBON_CREDITS_GROUP_SCENARIO_ID,
            carb_cred_zone_id=subscenarios.CARBON_CREDITS_ZONE_SCENARIO_ID,
        )
    )

    return cred_grp_reqs, cap_grp_prj


def write_model_inputs(
    scenario_directory,
    scenario_id,
    subscenarios,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
    conn,
):
    """ """

    (
        db_weather_iteration,
        db_hydro_iteration,
        db_availability_iteration,
        db_subproblem,
        db_stage,
    ) = directories_to_db_values(
        weather_iteration, hydro_iteration, availability_iteration, subproblem, stage
    )

    cap_grp_reqs, cap_grp_prj = get_inputs_from_database(
        scenario_id,
        subscenarios,
        db_weather_iteration,
        db_hydro_iteration,
        db_availability_iteration,
        db_subproblem,
        db_stage,
        conn,
    )

    # Write the input files only if a subscenario is specified
    if subscenarios.CARBON_CREDITS_GROUP_REQUIREMENT_SCENARIO_ID != "NULL":
        with open(
            os.path.join(
                scenario_directory,
                weather_iteration,
                hydro_iteration,
                availability_iteration,
                subproblem,
                stage,
                "inputs",
                "carbon_credits_group_requirements.tab",
            ),
            "w",
            newline="",
        ) as req_file:
            writer = csv.writer(req_file, delimiter="\t", lineterminator="\n")

            # Write header
            writer.writerow(
                [
                    "carbon_credits_group",
                    "period",
                    "carbon_credits_group_buy_min",
                    "carbon_credits_group_buy_max",
                    "carbon_credits_group_sell_min",
                    "carbon_credits_group_sell_max",
                ]
            )

            for row in cap_grp_reqs:
                replace_nulls = ["." if i is None else i for i in row]
                writer.writerow(replace_nulls)

    if subscenarios.CARBON_CREDITS_GROUP_SCENARIO_ID != "NULL":
        with open(
            os.path.join(
                scenario_directory,
                weather_iteration,
                hydro_iteration,
                availability_iteration,
                subproblem,
                stage,
                "inputs",
                "carbon_credits_group_credits_zone.tab",
            ),
            "w",
            newline="",
        ) as prj_file:
            writer = csv.writer(prj_file, delimiter="\t", lineterminator="\n")

            # Write header
            writer.writerow(["carbon_credits_group", "carbon_credits_zone"])

            for row in cap_grp_prj:
                writer.writerow(row)


def save_duals(
    scenario_directory,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
    instance,
    dynamic_components,
):
    instance.constraint_indices["Max_Group_Carbon_Credits_Buy_in_Period_Constraint"] = [
        "carbon_credits_group",
        "period",
        "dual",
    ]

    instance.constraint_indices["Min_Group_Carbon_Credits_Buy_in_Period_Constraint"] = [
        "carbon_credits_group",
        "period",
        "dual",
    ]
    instance.constraint_indices["Max_Group_Carbon_Credits_Sell_in_Period_Constraint"] = [
        "carbon_credits_group",
        "period",
        "dual",
    ]

    instance.constraint_indices["Min_Group_Carbon_Credits_Sell_in_Period_Constraint"] = [
        "carbon_credits_group",
        "period",
        "dual",
    ]


def import_results_into_database(
    scenario_id,
    weather_iteration,
    hydro_iteration,
    availability_iteration,
    subproblem,
    stage,
    c,
    db,
    results_directory,
    quiet,
):
    which_results = "carbon_credits_group_credits"
    # Import only if a results-file was exported
    results_file = os.path.join(results_directory, f"{which_results}.csv")
    if os.path.exists(results_file):
        import_csv(
            conn=db,
            cursor=c,
            scenario_id=scenario_id,
            weather_iteration=weather_iteration,
            hydro_iteration=hydro_iteration,
            availability_iteration=availability_iteration,
            subproblem=subproblem,
            stage=stage,
            quiet=quiet,
            results_directory=results_directory,
            which_results=which_results,
        )
