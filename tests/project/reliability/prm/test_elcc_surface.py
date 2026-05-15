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


from collections import OrderedDict
from importlib import import_module
import os.path
import sys
import unittest

from tests.common_functions import create_abstract_model, add_components_and_load_data

TEST_DATA_DIRECTORY = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "test_data"
)

# Import prerequisite modules
PREREQUISITE_MODULE_NAMES = [
    "temporal.operations.timepoints",
    "temporal.investment.periods",
    "temporal.operations.horizons",
    "geography.load_zones",
    "geography.prm_zones",
    "project",
    "project.capacity.capacity",
    "project.reliability.prm",
    "project.reliability.prm.prm_types",
]
NAME_OF_MODULE_BEING_TESTED = "project.reliability.prm.elcc_surface"
IMPORTED_PREREQ_MODULES = list()
for mdl in PREREQUISITE_MODULE_NAMES:
    try:
        imported_module = import_module("." + str(mdl), package="gridpath")
        IMPORTED_PREREQ_MODULES.append(imported_module)
    except ImportError:
        print("ERROR! Module " + str(mdl) + " not found.")
        sys.exit(1)
# Import the module we'll test
try:
    MODULE_BEING_TESTED = import_module(
        "." + NAME_OF_MODULE_BEING_TESTED, package="gridpath"
    )
except ImportError:
    print("ERROR! Couldn't import module " + NAME_OF_MODULE_BEING_TESTED + " to test.")


class TestProjELCCSurface(unittest.TestCase):
    """ """

    def test_add_model_components(self):
        """
        Test that there are no errors when adding model components
        :return:
        """
        create_abstract_model(
            prereq_modules=IMPORTED_PREREQ_MODULES,
            module_to_test=MODULE_BEING_TESTED,
            test_data_dir=TEST_DATA_DIRECTORY,
            weather_iteration="",
            hydro_iteration="",
            availability_iteration="",
            subproblem="",
            stage="",
        )

    def test_load_model_data(self):
        """
        Test that data are loaded with no errors
        :return:
        """
        add_components_and_load_data(
            prereq_modules=IMPORTED_PREREQ_MODULES,
            module_to_test=MODULE_BEING_TESTED,
            test_data_dir=TEST_DATA_DIRECTORY,
            weather_iteration="",
            hydro_iteration="",
            availability_iteration="",
            subproblem="",
            stage="",
        )

    def test_data_loaded_correctly(self):
        """
        Test that the data loaded are as expected
        :return:
        """
        m, data = add_components_and_load_data(
            prereq_modules=IMPORTED_PREREQ_MODULES,
            module_to_test=MODULE_BEING_TESTED,
            test_data_dir=TEST_DATA_DIRECTORY,
            weather_iteration="",
            hydro_iteration="",
            availability_iteration="",
            subproblem="",
            stage="",
        )
        instance = m.create_instance(data)

        # Set: ELCC_SURFACE_PRM_ZONE_PERIODS
        expected_surface_zone_periods = sorted(
            [
                ("Nuclear", "PRM_Zone1", 2020),
                ("Nuclear", "PRM_Zone1", 2030),
                ("Wind_Solar", "PRM_Zone1", 2020),
                ("Wind_Solar", "PRM_Zone1", 2030),
                ("Wind_Solar", "PRM_Zone2", 2020),
                ("Wind_Solar", "PRM_Zone2", 2030),
            ]
        )

        actual_surface_zone_periods = sorted(
            [(s, z, p) for (s, z, p) in instance.ELCC_SURFACE_PRM_ZONE_PERIODS]
        )

        self.assertListEqual(expected_surface_zone_periods, actual_surface_zone_periods)

        # Param: prm_peak_load_mw
        expected_peak_load = OrderedDict(
            sorted(
                {
                    ("Nuclear", "PRM_Zone1", 2020): 49406.65942,
                    ("Nuclear", "PRM_Zone1", 2030): 49406.65942,
                    ("Wind_Solar", "PRM_Zone1", 2020): 49406.65942,
                    ("Wind_Solar", "PRM_Zone1", 2030): 49406.65942,
                    ("Wind_Solar", "PRM_Zone2", 2020): 49913.83791,
                    ("Wind_Solar", "PRM_Zone2", 2030): 49913.83791,
                }.items()
            )
        )

        actual_peak_load = OrderedDict(
            sorted(
                {
                    (s, z, p): instance.prm_peak_load_mw[s, z, p]
                    for (s, z, p) in instance.ELCC_SURFACE_PRM_ZONE_PERIODS
                }.items()
            )
        )

        self.assertDictEqual(expected_peak_load, actual_peak_load)

        # Param: prm_annual_load_mwh
        expected_annual_load = OrderedDict(
            sorted(
                {
                    ("Nuclear", "PRM_Zone1", 2020): 242189141,
                    ("Nuclear", "PRM_Zone1", 2030): 242189141,
                    ("Wind_Solar", "PRM_Zone1", 2020): 242189141,
                    ("Wind_Solar", "PRM_Zone1", 2030): 242189141,
                    ("Wind_Solar", "PRM_Zone2", 2020): 244545760.8,
                    ("Wind_Solar", "PRM_Zone2", 2030): 244545760.8,
                }.items()
            )
        )

        actual_annual_load = OrderedDict(
            sorted(
                {
                    (s, z, p): instance.prm_annual_load_mwh[s, z, p]
                    for (s, z, p) in instance.ELCC_SURFACE_PRM_ZONE_PERIODS
                }.items()
            )
        )

        self.assertDictEqual(expected_annual_load, actual_annual_load)

        # Param: elcc_surface_name
        expected_elcc_surface_names = OrderedDict(
            sorted(
                {
                    ("Coal", "PRM_Zone1"): None,
                    ("Coal_z2", "PRM_Zone2"): None,
                    ("Gas_CCGT", "PRM_Zone1"): None,
                    ("Gas_CCGT_New", "PRM_Zone1"): None,
                    ("Gas_CCGT_New_Binary", "PRM_Zone1"): None,
                    ("Gas_CCGT_z2", "PRM_Zone2"): None,
                    ("Gas_CT", "PRM_Zone1"): None,
                    ("Gas_CT_New", "PRM_Zone1"): None,
                    ("Gas_CT_z2", "PRM_Zone2"): None,
                    ("Nuclear", "PRM_Zone1"): "Nuclear",
                    ("Nuclear_z2", "PRM_Zone2"): None,
                    ("Wind", "PRM_Zone1"): "Wind_Solar",
                    ("Wind_z2", "PRM_Zone2"): "Wind_Solar",
                    ("Battery", "PRM_Zone1"): None,
                    ("Battery_Binary", "PRM_Zone1"): None,
                    ("Battery_Specified", "PRM_Zone1"): None,
                    ("Hydro", "PRM_Zone1"): None,
                    ("Hydro_NonCurtailable", "PRM_Zone1"): None,
                    ("Disp_Binary_Commit", "PRM_Zone1"): None,
                    ("Disp_Cont_Commit", "PRM_Zone1"): None,
                    ("Disp_No_Commit", "PRM_Zone1"): None,
                    ("Clunky_Old_Gen", "PRM_Zone1"): None,
                    ("Clunky_Old_Gen2", "PRM_Zone1"): None,
                    ("Nuclear_Flexible", "PRM_Zone1"): None,
                }.items()
            )
        )
        actual_elcc_surface_names = OrderedDict(
            sorted(
                {
                    p: instance.elcc_surface_name[p] for p in instance.PRM_PROJECTS_PRM_ZONES
                }.items()
            )
        )

        self.assertDictEqual(expected_elcc_surface_names, actual_elcc_surface_names)

        # Param: elcc_surface_cap_factor
        expected_elcc_cf = OrderedDict(
            sorted(
                {
                    ("Coal", "PRM_Zone1"): None,
                    ("Coal_z2", "PRM_Zone2"): None,
                    ("Gas_CCGT", "PRM_Zone1"): None,
                    ("Gas_CCGT_New", "PRM_Zone1"): None,
                    ("Gas_CCGT_New_Binary", "PRM_Zone1"): None,
                    ("Gas_CCGT_z2", "PRM_Zone2"): None,
                    ("Gas_CT", "PRM_Zone1"): None,
                    ("Gas_CT_New", "PRM_Zone1"): None,
                    ("Gas_CT_z2", "PRM_Zone2"): None,
                    ("Nuclear", "PRM_Zone1"): 0.123,
                    ("Nuclear_z2", "PRM_Zone2"): None,
                    ("Wind", "PRM_Zone1"): 0.123,
                    ("Wind_z2", "PRM_Zone2"): 0.123,
                    ("Battery", "PRM_Zone1"): None,
                    ("Battery_Binary", "PRM_Zone1"): None,
                    ("Battery_Specified", "PRM_Zone1"): None,
                    ("Hydro", "PRM_Zone1"): None,
                    ("Hydro_NonCurtailable", "PRM_Zone1"): None,
                    ("Disp_Binary_Commit", "PRM_Zone1"): None,
                    ("Disp_Cont_Commit", "PRM_Zone1"): None,
                    ("Disp_No_Commit", "PRM_Zone1"): None,
                    ("Clunky_Old_Gen", "PRM_Zone1"): None,
                    ("Clunky_Old_Gen2", "PRM_Zone1"): None,
                    ("Nuclear_Flexible", "PRM_Zone1"): None,
                }.items()
            )
        )

        actual_elcc_cf = OrderedDict(
            sorted(
                {
                    p: instance.elcc_surface_cap_factor[p]
                    for p in instance.PRM_PROJECTS_PRM_ZONES
                }.items()
            )
        )

        self.assertDictEqual(expected_elcc_cf, actual_elcc_cf)

        # Set: ELCC_SURFACE_PROJECTS
        expected_elcc_surf_prj = sorted(
            [
                ("Nuclear", "Nuclear", "PRM_Zone1"),
                ("Wind_Solar", "Wind", "PRM_Zone1"),
                ("Wind_Solar", "Wind_z2", "PRM_Zone2")
            ]
        )
        actual_elcc_surf_prj = sorted(
            [(s, p, z) for (s, p, z) in instance.ELCC_SURFACE_PROJECTS]
        )
        self.assertListEqual(expected_elcc_surf_prj, actual_elcc_surf_prj)

        # Set: ELCC_SURFACE_PROJECTS_BY_PRM_ZONE
        expected_surface_projects_by_zone = OrderedDict(
            sorted(
                {
                    "PRM_Zone1": [("Nuclear", "Nuclear", "PRM_Zone1"), ("Wind_Solar", "Wind", "PRM_Zone1")],
                    "PRM_Zone2": [("Wind_Solar", "Wind_z2", "PRM_Zone2")],
                }.items()
            )
        )

        actual_surface_projects_by_zone = OrderedDict(
            sorted(
                {
                    z: [
                        (s, p, prm_z)
                        for (s, p, prm_z) in instance.ELCC_SURFACE_PROJECTS_BY_PRM_ZONE[z]
                    ]
                    for z in instance.PRM_ZONES
                }.items()
            )
        )

        self.assertDictEqual(
            expected_surface_projects_by_zone, actual_surface_projects_by_zone
        )

        # Set: ELCC_SURFACE_PROJECT_PERIOD_FACETS
        expected_s_prj_p_f = sorted(
            [
                ("Nuclear", "Nuclear", "PRM_Zone1", 2020, 1),
                ("Nuclear", "Nuclear", "PRM_Zone1", 2020, 2),
                ("Nuclear", "Nuclear", "PRM_Zone1", 2030, 1),
                ("Nuclear", "Nuclear", "PRM_Zone1", 2030, 2),
                ("Wind_Solar", "Wind", "PRM_Zone1", 2020, 1),
                ("Wind_Solar", "Wind", "PRM_Zone1", 2020, 2),
                ("Wind_Solar", "Wind", "PRM_Zone1", 2030, 1),
                ("Wind_Solar", "Wind", "PRM_Zone1", 2030, 2),
                ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2020, 1),
                ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2020, 2),
                ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2030, 1),
                ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2030, 2),
            ]
        )

        actual_s_prj_p_f = sorted(
            [
                (s, prj, prm_z, p, f)
                for (s, prj, prm_z, p, f) in instance.ELCC_SURFACE_PROJECT_PERIOD_FACETS
            ]
        )

        self.assertListEqual(expected_s_prj_p_f, actual_s_prj_p_f)

        # Param: elcc_surface_coefficient
        expected_coeff = OrderedDict(
            sorted(
                {
                    ("Nuclear", "Nuclear", "PRM_Zone1", 2020, 1): 0.9,
                    ("Nuclear", "Nuclear", "PRM_Zone1", 2020, 2): 0.9,
                    ("Nuclear", "Nuclear", "PRM_Zone1", 2030, 1): 0.9,
                    ("Nuclear", "Nuclear", "PRM_Zone1", 2030, 2): 0.9,
                    ("Wind_Solar", "Wind", "PRM_Zone1", 2020, 1): 0.3,
                    ("Wind_Solar", "Wind", "PRM_Zone1", 2020, 2): 0.2,
                    ("Wind_Solar", "Wind", "PRM_Zone1", 2030, 1): 0.25,
                    ("Wind_Solar", "Wind", "PRM_Zone1", 2030, 2): 0.2,
                    ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2020, 1): 0.3,
                    ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2020, 2): 0.25,
                    ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2030, 1): 0.3,
                    ("Wind_Solar", "Wind_z2", "PRM_Zone2", 2030, 2): 0.25,
                }.items()
            )
        )

        actual_coeff = OrderedDict(
            sorted(
                {
                    (s, prj, prm_z, p, f): instance.elcc_surface_coefficient[s, prj, prm_z, p, f]
                    for (s, prj, prm_z, p, f) in instance.ELCC_SURFACE_PROJECT_PERIOD_FACETS
                }.items()
            )
        )
        self.assertDictEqual(expected_coeff, actual_coeff)
