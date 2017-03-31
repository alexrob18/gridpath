#!/usr/bin/env python
# Copyright 2017 Blue Marble Analytics LLC. All rights reserved.
import os
import unittest

import run_scenario

# Change directory to base directory, as that"s what run_scenario.py expects
os.chdir(os.path.join(os.path.dirname(__file__), ".."))


class TestExamples(unittest.TestCase):
    """

    """
    def test_example_test(self):
        """
        Check objective function value of "test" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "test",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objective = 65494.41333

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_build_storage(self):
        """
        Check objective function value of "test_new_build_storage" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "test_new_build_storage",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objective = 102403.6400000600

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_build_storage_cumulative_min_max(self):
        """
        Check objective function value of
        "test_new_build_storage_cumulative_min_max" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario",
                               "test_new_build_storage_cumulative_min_max",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objective = 105922.15516955667

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_no_reserves(self):
        """
        Check objective function value of "test_no_reserves" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "test_no_reserves", "--quiet",
                               "--scenario_location", "examples",
                               "--mute_solver_output", "--testing"])

        expected_objective = 53362.74667

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_w_hydro(self):
        """
        Check objective function value of "test_w_hydro" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "test_w_hydro", "--quiet",
                               "--scenario_location", "examples",
                               "--mute_solver_output", "--testing"])

        expected_objective = 49049.58000

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_w_storage(self):
        """
        Check objective function value of "test_no_reserves" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "test_w_storage", "--quiet",
                               "--scenario_location", "examples",
                               "--mute_solver_output", "--testing"])

        expected_objective = 54702.61516952667

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2horizons(self):
        """
        Check objective function value of "2horizons" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "2horizons", "--quiet",
                               "--scenario_location", "examples",
                               "--mute_solver_output", "--testing"])

        expected_objective = 130988.82664

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2periods(self):
        """
        Check objective function value of "2periods" example
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "2periods", "--quiet",
                               "--scenario_location", "examples",
                               "--mute_solver_output", "--testing"])

        expected_objective = 1309888.26636

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2periods_new_build(self):
        """
        Check objective function value of "2periods_new_build" example;
        this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "2periods_new_build",
                               "--scenario_location", "examples",
                               "--solver", "ipopt", "--quiet",
                               "--mute_solver_output", "--testing"])

        expected_objective = 110443853.65676

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_2zones(self):
        """
        Check objective function value of "2periods_new_build_2zones" example;
        this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario", "2periods_new_build_2zones",
                               "--scenario_location", "examples",
                               "--solver", "ipopt", "--quiet",
                               "--mute_solver_output", "--testing"])

        expected_objective = 220087705.71354377

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_2zones_new_build_transmission(self
                                                                           ):
        """
        Check objective function value of
        "2periods_new_build_2zones_new_build_transmission" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_2zones_new_build_transmission",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 1941106539.6260998

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_2zones_singleBA(self):
        """
        Check objective function value of "2periods_new_build_2zones_singleBA"
        example; this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_2zones_singleBA",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 220044845.63243133

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_2zones_transmission(self):
        """
        Check objective function value of
        "2periods_new_build_2zones_transmission" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_2zones_transmission",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 50552825288.93714

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2periods_new_build_rps(self):
        """
        Check objective function value of "2periods_new_build_rps" example;
        this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_rps",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 972816048.46947

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_cumulative_min_max(self):
        """
        Check objective function value of
        "2periods_new_build_cumulative_min_max" example;
        this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(["--scenario",
                               "2periods_new_build_cumulative_min_max",
                               "--scenario_location", "examples",
                               "--solver", "ipopt", "--quiet",
                               "--mute_solver_output", "--testing"])

        expected_objective = 6295817377.201665

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_single_stage_prod_cost(self):
        """
        Check objective function values of "single_stage_prod_cost" example
        :return:
        """
        actual_objectives = \
            run_scenario.main(["--scenario", "single_stage_prod_cost",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objectives = {
            1: 65494.41332,
            2: 65494.41332,
            3: 65494.41332
        }

        for horizon in [1, 2, 3]:
            self.assertAlmostEqual(
                expected_objectives[horizon],
                actual_objectives[str(horizon)],
                places=1
            )

    def test_example_multi_stage_prod_cost(self):
        """
        Check objective function values of "multi_stage_prod_cost" example
        :return:
        """
        actual_objectives = \
            run_scenario.main(["--scenario", "multi_stage_prod_cost",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objectives = {
            1: {"da": 65494.41333,
                "ha": 65494.41333,
                "rt": 65494.41333},
            2: {"da": 65494.41333,
                "ha": 65494.41333,
                "rt": 65494.41333},
            3: {"da": 65494.41333,
                "ha": 65494.41333,
                "rt": 65494.41333}
        }

        for horizon in [1, 2, 3]:
            for stage in {"da", "ha", "rt"}:
                self.assertAlmostEqual(
                    expected_objectives[horizon][stage],
                    actual_objectives[str(horizon)][stage],
                    places=1
                )

    def test_example_multi_stage_prod_cost_w_hydro(self):
        """
        Check objective function values of "multi_stage_prod_cost_w_hydro"
        example
        :return:
        """
        actual_objectives = \
            run_scenario.main(["--scenario", "multi_stage_prod_cost_w_hydro",
                               "--scenario_location", "examples",
                               "--quiet", "--mute_solver_output", "--testing"])

        expected_objectives = {
            1: {"da": 60554.52439,
                "ha": 60554.52439,
                "rt": 60554.52439},
            2: {"da": 60554.52439,
                "ha": 60554.52439,
                "rt": 60554.52439},
            3: {"da": 60554.52439,
                "ha": 60554.52439,
                "rt": 60554.52439}
        }

        for horizon in [1, 2, 3]:
            for stage in {"da", "ha", "rt"}:
                self.assertAlmostEqual(
                    expected_objectives[horizon][stage],
                    actual_objectives[str(horizon)][stage],
                    places=1
                )

    def test_example_2periods_gen_lin_econ_retirement(self):
        """
        Check objective function value of "2periods_gen_lin_econ_retirement"
        example; this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_gen_lin_econ_retirement",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 1309888.2613

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_variable_gen_reserves(self):
        """
        Check objective function value of "variable_gen_reserves"
        example; this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_variable_gen_reserves",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 64739.3134351

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_rps_variable_reserves(self):
        """
        Check objective function value of
        "2periods_new_build_rps_variable_reserves" example; this example
        requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_rps_variable_reserves",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 844035398.4650549

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_2periods_new_build_rps_variable_reserves_subhourly_adj(
            self):
        """
        Check objective function value of
        "2periods_new_build_rps_variable_reserves_subhourly_adj" example;
        this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_rps_variable_reserves_subhourly_adj",
                 "--scenario_location", "examples",
                 "--solver", "ipopt", "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 845531663.851

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=0)

    def test_example_test_ramp_up_constraints(self):
        """
        Check objective function value of "test_ramp_up_constraints" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_ramp_up_constraints",
                 "--scenario_location", "examples",
                 "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 68087.36333333331

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_ramp_up_and_down_constraints(self):
        """
        Check objective function value of "test_ramp_up_and_down_constraints"
        example; this example requires a non-linear solver
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_ramp_up_and_down_constraints",
                 "--scenario_location", "examples",
                 "--quiet",
                 "--mute_solver_output", "--testing"]
            )

        expected_objective = 80071268.56333333

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2periods_new_build_rps_w_rps_ineligible_storage(self):
        """
        Check objective function value of
        "2periods_new_build_rps_w_rps_ineligible_storage" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_rps_w_rps_ineligible_storage",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 940371813.224

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_2periods_new_build_rps_w_rps_eligible_storage(self):
        """
        Check objective function value of
        "2periods_new_build_rps_w_rps_eligible_storage" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "2periods_new_build_rps_w_rps_eligible_storage",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 945001614.7954971

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_solar(self):
        """
        Check objective function value of "test_new_solar" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_new_solar",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 62127.27439170666

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_solar_carbon_cap(self):
        """
        Check objective function value of "test_new_solar_carbon_cap" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_new_solar_carbon_cap",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 271066533.40358055

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_solar_carbon_cap_2zones_tx(self):
        """
        Check objective function value of
        "test_new_solar_carbon_cap_2zones_tx" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_new_solar_carbon_cap_2zones_tx",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 159168636.89700875

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

    def test_example_test_new_solar_carbon_cap_2zones_dont_count_tx(self):
        """
        Check objective function value of
        "test_new_solar_carbon_cap_2zones_dont_count_tx" example
        :return:
        """
        actual_objective = \
            run_scenario.main(
                ["--scenario",
                 "test_new_solar_carbon_cap_2zones_dont_count_tx",
                 "--scenario_location", "examples",
                 "--quiet", "--mute_solver_output", "--testing"]
            )

        expected_objective = 142694316.98004726

        self.assertAlmostEqual(expected_objective, actual_objective,
                               places=1)

if __name__ == "__main__":
    unittest.main()
