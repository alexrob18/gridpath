# Copyright 2016-2020 Blue Marble Analytics LLC.
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

from __future__ import print_function
from __future__ import absolute_import

from pyomo.environ import Var, Constraint, NonNegativeReals, Expression, value
from .reserve_balance import (
    generic_add_model_components,
    generic_export_results,
    generic_save_duals,
    generic_import_results_to_database,
)


def add_model_components(m, d, scenario_directory, subproblem, stage):
    """

    :param m:
    :param d:
    :return:
    """

    # Penalty for violation
    setattr(
        m,
        "Inertia_Reserves_Violation_MW",
        Var(getattr(m, "INERTIA_RESERVES_ZONES"), m.TMPS, within=NonNegativeReals),
    )

    def violation_expression_rule(mod, ba, tmp):
        """

        :param mod:
        :param ba:
        :param tmp:
        :return:
        """
        return (
                getattr(mod, "inertia_reserves_allow_violation")[ba]
                * getattr(mod, "Inertia_Reserves_Violation_MW")[ba, tmp]
        )

    setattr(
        m,
        "Inertia_Reserves_Violation_MW_Expression",
        Expression(
            getattr(m, "INERTIA_RESERVES_ZONES"), m.TMPS, rule=violation_expression_rule
        ),
    )

    # Reserve constraints
    def meet_reserve_rule(mod, ba, tmp):
        return (
                getattr(mod, "Total_Inertia_Reserves_Provision_MW")[ba, tmp]
                + getattr(mod, "Inertia_Reserves_Violation_MW_Expression")[ba, tmp]
                >= getattr(mod, "Iner_Requirement")[ba, tmp]
        )

    setattr(
        m,
        "Meet_Inertia_Reserves_Constraint",
        Constraint(getattr(m, "INERTIA_RESERVES_ZONES"), m.TMPS, rule=meet_reserve_rule),
    )


def export_results(scenario_directory, subproblem, stage, m, d):
    """

    :param scenario_directory:
    :param subproblem:
    :param stage:
    :param m:
    :param d:
    :return:
    """
    generic_export_results(
        scenario_directory,
        subproblem,
        stage,
        m,
        d,
        "inertia_reserves_violation.csv",
        "inertia_reserves_violation_mw",
        "INERTIA_RESERVES_ZONES",
        "Inertia_Reserves_Violation_MW_Expression",
    )


def save_duals(scenario_directory, subproblem, stage, instance, dynamic_components):
    """

    :param m:
    :return:
    """
    generic_save_duals(instance, "Meet_Inertia_Reserves_Constraint")


def import_results_into_database(
    scenario_id, subproblem, stage, c, db, results_directory, quiet
):
    """

    :param scenario_id:
    :param c:
    :param db:
    :param results_directory:
    :param quiet:
    :return:
    """
    if not quiet:
        print("system inertia reserves balance")

    generic_import_results_to_database(
        scenario_id=scenario_id,
        subproblem=subproblem,
        stage=stage,
        c=c,
        db=db,
        results_directory=results_directory,
        reserve_type="inertia_reserves",
    )
