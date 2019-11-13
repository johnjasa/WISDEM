#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import copy
from ruamel_yaml import YAML

from wisdem.rotorse.rotor_geometry_yaml import ReferenceBlade


if __name__ == '__main__':

    # --- INPUTS --- #
    fname_input = "turbine_inputs/BAR208_noRe.yaml"
    xfoil_path = "/Users/rfeil/work/4_Xfoil/Xfoil.app/Contents/Resources/xfoil"



    # --- Load input --- #
    with open(fname_input, 'r') as myfile:
        inputs = myfile.read()
    # ------------------ #


    yaml = YAML()
    wt = yaml.load(inputs)

    blade = copy.deepcopy(wt['components']['blade'])
    airfoils = copy.deepcopy(wt['airfoils'])

    # determine reference airfoils within blade components
    af_ref    = {}
    for afi in airfoils:
        if afi['name'] in blade['outer_shape_bem']['airfoil_position']['labels']:
            af_ref[afi['name']] = afi


    # Select airfoils for which new airfoil polars are to be determined

    init['NPTS_AfProfile'] = 50
    init = 50


    blade = ReferenceBlade.remap_profiles(self=init, blade=blade, AFref=af_ref, xfoil_path = xfoil_path)  # run XFoil at given flap angles
    blade = ReferenceBlade.remap_polars(blade, af_ref)



    print()



