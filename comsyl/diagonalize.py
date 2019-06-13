

import numpy

# from srwlib import *
import sys


import comsyl
print(">>>>>>>",comsyl.__file__)
from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction
from comsyl.autocorrelation.AutocorrelationFunctionPropagator import AutocorrelationFunctionPropagator
from comsyl.parallel.utils import isMaster, barrier
from comsyl.utils.Logger import log


from comsyl.waveoptics.Wavefront import NumpyWavefront, SRWWavefront

if __name__ == "__main__":

    filename =     "/users/srio/OASYS1.1e/paper-hierarchical-resources/comsyl/propagation_wofry_EBS/propagated_beamline.npz"
    filename_out = "/users/srio/OASYS1.1e/paper-hierarchical-resources/comsyl/propagation_wofry_EBS/rediagonalized.npz"

    af_name = filename.split("/")[-1].replace(".npz", "")

    autocorrelation_function = AutocorrelationFunction.load(filename)

    print(autocorrelation_function.eigenvalues())

    autocorrelation_function.diagonalizeModes()

    print(autocorrelation_function.eigenvalues())

    autocorrelation_function.save(filename_out)


