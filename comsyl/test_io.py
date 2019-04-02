from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction
from comsyl.autocorrelation.CompactAFReader import CompactAFReader

filename = "/scisoft/data/srio/COMSYL/ID16/id16s_ebs_u18_1400mm_1h_new_s1.0.npy"
# af0 = AutocorrelationFunction.load(filename)

af1 = CompactAFReader.initialize_from_file(filename)

af1.write_h5("tmp.h5",100)


af2 = CompactAFReader.initialize_from_file("tmp.h5")



