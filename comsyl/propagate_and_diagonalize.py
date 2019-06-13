import pickle
from comsyl.waveoptics.ComsylWofryBeamline import ComsylWofryBeamline
from comsyl.waveoptics.SRWAdapter import ComsylSRWBeamline
from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction
from comsyl.autocorrelation.CompactAFReader import CompactAFReader

comsyl_beamline  = pickle.load(open("id16a.p","rb"))

#filename = "/users/srio/OASYS1.1e/paper-hierarchical-resources/comsyl/propagation_wofry_EBS/propagated_beamline.npz"
filename = "/scisoft/data/srio/COMSYL/ID16/id16s_ebs_u18_1400mm_1h_new_s1.0.npy"
#af_comsyl = AutocorrelationFunction.load(filename)
af_oasys = CompactAFReader.initialize_from_file(filename)
af_comsyl = af_oasys.get_af()

# **source position correction**
source_position=af_comsyl.info().sourcePosition()
if source_position == "entrance":
    source_offset = af_comsyl._undulator.length() * 0.5
elif source_position == "center":
    source_offset = 0.0
else:
    raise Exception("Unhandled source position")
print("Using source position entrance z=%f" % source_offset)
comsyl_beamline.add_undulator_offset(source_offset)


af_propagated = comsyl_beamline.propagate_af(af_comsyl,
             directory_name="tmp_comsyl_propagation",
             af_output_file_root="tmp_comsyl_propagation/propagated_beamline",
             maximum_mode=5,
             python_to_be_used="/users/srio/OASYS1.1e/oasys1env/bin/python")
af_propagated.save("propagated")

#rediagonalization
af_propagated.diagonalizeModes(5)
af_propagated.save("rediagonalized")
#
