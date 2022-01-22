import skrf
import ns2mdif

amp_data = skrf.read_all("LEE-39+")
ns = skrf.NetworkSet(amp_data)


# Export a NetworkSet with filenames as the GMDIF parameter
# by default, the network name is used as the VAR parameter

# ns2mdif.networkset2gmdif(ns, "LEE-39+.mdf")

# here is a better example

current_mA = []
temp_C = []

# parse the network names containing temperature and current into floats

for ntwk in ns:
    _, current_str, temp_str = ntwk.name.split("___")
    current_mA.append(float(current_str.replace("mA", "")))
    temp_C.append(float(temp_str.replace("Plus", "").replace("Minus", "-").replace("degC", "")))

values = {"current_mA": current_mA, "temp_C": temp_C}
datatypes = {"current_mA": "double", "temp_C": "double"}
comments = ["scikit-rf NetworkSet converted to GMDIF file", "Awesome!"]

ns2mdif.networkset2gmdif(ns, "LEE-39+.mdf", values, datatypes, comments)
