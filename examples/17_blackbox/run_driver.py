import os

import numpy as np

from wisdem import run_wisdem
from wisdem.inputs import load_yaml, write_yaml


def run_wisdem_tower_design(tower_height, base_thickness, top_thickness, top_diameter):
    """
    Lightly-wrapped version of WISDEM that takes in four tower design variables and outputs
    the full LCOE for the turbine, with blades and other subsystems fixed.

    Parameters
    ----------
    tower_height : float, [m]
        Tower height
    base_thickness : float, [m]
        Thickness of the tower wall at the base
    top_thickness : float, [m]
        Thickness of the tower wall at the top
    top_diameter : float, [m]
        Outer diameter at the top of the tower

    Returns
    -------
    LCOE : float, USD/MWh
        Levelized cost of energy for the entire turbine
    """

    ## File management
    mydir = os.path.dirname(os.path.realpath(__file__))  # get path to this file
    fname_wt_input = mydir + os.sep + "nrel5mw.yaml"
    fname_modeling_options = mydir + os.sep + "modeling_options.yaml"
    fname_analysis_options = mydir + os.sep + "analysis_options.yaml"

    n_height_tower = 11
    z_values = np.linspace(10.0, tower_height, n_height_tower)
    thicknesses = np.linspace(base_thickness, top_thickness, n_height_tower)
    outer_diameters = np.linspace(6.5, top_diameter, n_height_tower)

    # Load the base geometry yaml for the OC3 spar
    geom = load_yaml(fname_wt_input)

    # Loop through the tower z-values and assign them to the modified yaml dict
    for idx, z_value in enumerate(z_values):
        geom["components"]["tower"]["outer_shape_bem"]["reference_axis"]["z"]["values"][idx] = float(z_value)
    geom["assembly"]["hub_height"] = float(z_values[-1] + (90.0 - 87.6))

    # Replace the thickness values in the modified yaml
    for idx, thickness in enumerate(thicknesses):
        geom["components"]["tower"]["internal_structure_2d_fem"]["layers"][0]["thickness"]["values"][idx] = float(
            thickness
        )

    # Replace the outer diameter values
    for idx, outer_diameter in enumerate(outer_diameters):
        geom["components"]["tower"]["outer_shape_bem"]["outer_diameter"]["values"][idx] = float(outer_diameter)

    # Save the modified yaml options into a new geometry yaml
    new_fname_wt_input = f"{fname_wt_input.split('/')[-1].split('.')[0]}_mod.yaml"
    write_yaml(geom, new_fname_wt_input)

    # Run a WISDEM analysis with the modified geometry
    wt, analysis_options, opt_options = run_wisdem(new_fname_wt_input, fname_modeling_options, fname_analysis_options)

    # Grab and return the LCOE
    LCOE = wt.get_val("financese.lcoe", units="USD/(MW*h)")[0]

    return LCOE


# Nominal values for the OC3 spar
tower_height = 87.6  # meters
top_thickness = 0.019  # meters
base_thickness = 0.027  # meters
top_diameter = 3.87  # meters

LCOE = run_wisdem_tower_design(tower_height, base_thickness, top_thickness, top_diameter)
print("LCOE:", LCOE, "USD/MWh")

# Example: use less tower materials by decreasing the thicknesses and top diameter,
# leading to a lower LCOE.
tower_height = 87.6  # meters
top_thickness = 0.01  # meters
base_thickness = 0.02  # meters
top_diameter = 3.0  # meters

LCOE = run_wisdem_tower_design(tower_height, base_thickness, top_thickness, top_diameter)
print("LCOE:", LCOE, "USD/MWh")
