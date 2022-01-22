from itertools import product
import numpy as np
import skrf
import sys


def networkset2gmdif(networkset: skrf.NetworkSet, output_file: str, values=None, datatypes=None, comments=[]):
    """Convert a scikit-rf NetworkSet object to an Generated MDIF file


    if values==None then use networkset names
    comments is a list (each element is separate comment line)

    """

    if values == None:
        v = list()
        for ns in networkset:
            v.append(ns.name)

        values = {"name": v}
        datatypes = {"name": "string"}

    # VAR datatypes
    dict_types = dict({"int": "0", "double": "1", "string": "2"})

    try:
        mdif = open(output_file, "w")
    except:
        print("Error:", sys.exc_info()[0])

    # write comments
    for c in comments:
        mdif.write(f"! {c}\n")

    nports = networkset[0].nports

    optionstring = __create_optionstring(nports)

    for filenumber, ntwk in enumerate(networkset):
        # print("[INFO]: Processing {} Port file: {}".format(nports, ntwk.name))

        mdif.write("!" + "-" * 79 + "\n! network name: " + ntwk.name + "\n\n")

        for p in values:
            # assign double as the datatype if none is specified
            if p not in datatypes:
                datatypes[p] = "double"

            if datatypes[p] == "string":
                var_def_str = 'VAR {}({}) = "{}"'.format(p, dict_types[datatypes[p]], values[p][filenumber])
            else:
                var_def_str = "VAR {}({}) = {}".format(p, dict_types[datatypes[p]], values[p][filenumber])

            mdif.write(var_def_str + "\n")

        mdif.write("\nBEGIN ACDATA\n")
        mdif.write(optionstring + "\n")
        data = ntwk.write_touchstone(return_string=True)
        mdif.write(data)
        mdif.write("END\n\n")

    mdif.close()

    # print("[INFO]: Saved Generalized MDIF: {}".format(output_file))


def __create_optionstring(nports):
    if nports > 9:
        corestring = "n{}_{}x n{}_{}y "
    else:
        corestring = "n{}{}x n{}{}y "

    optionstring = "%F "

    if nports == 2:
        optionstring += "n11x n11y n21x n21y n12x n12y n22x n22y"

    else:
        # parse the option string for nports not equal to 2

        for i in product(list(range(1, nports + 1)), list(range(1, nports + 1))):

            optionstring += corestring.format(i[0], i[1], i[0], i[1])

            # special case for nports = 3
            if nports == 3:
                # 3 ports
                if not (np.remainder(i[1], 3)):
                    optionstring += "\n"

            # touchstone spec allows only 4 data pairs per line
            if nports >= 4:
                if np.remainder(i[1], 4) == 0:
                    optionstring += "\n"
                # NOTE: not sure if this is needed. Doesn't seem to be
                # required by Microwave Office
                if i[1] == nports:
                    optionstring += "\n"
    return optionstring
