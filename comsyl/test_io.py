


from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction
from comsyl.autocorrelation.CompactAFReader import CompactAFReader

# af0 = AutocorrelationFunction.load(filename)


#filename = "/scisoft/data/srio/COMSYL/ID16/id16s_ebs_u18_1400mm_1h_new_s1.0.npy"
#af1 = CompactAFReader.initialize_from_file(filename)
#af1.write_h5("tmp.h5",100)
#af2 = CompactAFReader.initialize_from_file("tmp.h5")


filename ="/scisoft/data/srio/COMSYL/ID16/id16s_hb_u18_1400mm_1h_s1.0.npz"
#af1 = CompactAFReader.initialize_from_file(filename)
#af1._af.saveh5("tmp_hb.h5",15)
#af2 = CompactAFReader.initialize_from_file("tmp_hb.h5")
#print(af1.info())


#filename = "/scisoft/data/srio/COMSYL/ID16/id16s_hb_u18_1400mm_1h_s1.0.h5"
#af1 = CompactAFReader.initialize_from_file(filename)

af1 = AutocorrelationFunction.load(filename)
#af1.write_h5("tmp.h5",20)
#af1._af.saveh5("tmp_hb.h5",15)
