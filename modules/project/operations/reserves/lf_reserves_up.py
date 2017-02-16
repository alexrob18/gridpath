#!/usr/bin/env python

"""
Add project-level components for upward load-following reserves
"""

from modules.project.operations.reserves.reserve_provision import \
    generic_determine_dynamic_components, generic_add_model_components, \
    generic_load_model_data, generic_export_module_specific_results


def determine_dynamic_components(d, scenario_directory, horizon, stage):
    """

    :param d:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :return:
    """

    generic_determine_dynamic_components(
        d=d,
        scenario_directory=scenario_directory,
        horizon=horizon,
        stage=stage,
        reserve_module="lf_reserves_up",
        headroom_or_footroom_dict="headroom_variables",
        ba_column_name="lf_reserves_up_zone",
        reserve_provision_variable_name="Provide_LF_Reserves_Up_MW",
        reserve_provision_derate_param_name="lf_reserves_up_derate",
        reserve_provision_subhourly_adjustment_param_name=
        "lf_reserves_up_provision_subhourly_energy_adjustment",
        reserve_balancing_area_param_name="lf_reserves_up_zone"
    )


def add_model_components(m, d):
    """

    :param m:
    :param d:
    :return:
    """

    generic_add_model_components(
        m=m,
        d=d,
        reserve_projects_set="LF_RESERVES_UP_PROJECTS",
        reserve_balancing_area_param="lf_reserves_up_zone",
        reserve_provision_derate_param="lf_reserves_up_derate",
        reserve_balancing_areas_set="LF_RESERVES_UP_ZONES",
        reserve_project_operational_timepoints_set=
        "LF_RESERVES_UP_PROJECT_OPERATIONAL_TIMEPOINTS",
        reserve_provision_variable_name="Provide_LF_Reserves_Up_MW",
        reserve_provision_subhourly_adjustment_param
        ="lf_reserves_up_provision_subhourly_energy_adjustment"
    )


def load_model_data(m, d, data_portal, scenario_directory, horizon, stage):
    """

    :param m:
    :param d:
    :param data_portal:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :return:
    """
    generic_load_model_data(
        m=m,
        d=d,
        data_portal=data_portal,
        scenario_directory=scenario_directory,
        horizon=horizon,
        stage=stage,
        ba_column_name="lf_reserves_up_zone",
        derate_column_name="lf_reserves_up_derate",
        reserve_balancing_area_param="lf_reserves_up_zone",
        reserve_provision_derate_param="lf_reserves_up_derate",
        reserve_projects_set="LF_RESERVES_UP_PROJECTS",
        reserve_provision_subhourly_adjustment_param
        ="lf_reserves_up_provision_subhourly_energy_adjustment",
        reserve_balancing_areas_input_file
        ="load_following_up_balancing_areas.tab"
    )


def export_module_specific_results(m, d, scenario_directory, horizon, stage):
    """
    Export project-level results for upward load-following
    :param m:
    :param d:
    :param scenario_directory:
    :param horizon:
    :param stage:
    :return:
    """

    generic_export_module_specific_results(
        m=m,
        d=d,
        scenario_directory=scenario_directory,
        horizon=horizon,
        stage=stage,
        module_name="lf_reserves_up",
        reserve_project_operational_timepoints_set=
        "LF_RESERVES_UP_PROJECT_OPERATIONAL_TIMEPOINTS",
        reserve_provision_variable_name="Provide_LF_Reserves_Up_MW"
    )
