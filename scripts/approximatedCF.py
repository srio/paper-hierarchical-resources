import numpy
import scipy.constants as codata
from tableElectron import get_sigmas

def get_sigmas_radiation(photon_energy,undulator_length):
    lambdan = 1e-10 * codata.h*codata.c/codata.e*1e10 / photon_energy # in m
    return 1e6*2.740/4/numpy.pi*numpy.sqrt(lambdan*undulator_length),1e6*0.69*numpy.sqrt(lambdan/undulator_length),




if __name__ == "__main__":

    photon_energy = 17000.0
    undulator_length = 1.4

    sr,srp = get_sigmas_radiation(photon_energy,undulator_length)

    print("sigmas: ",sr,srp)



    txt = ""
    for machine in ["ESRF","EBS"]:
        m = get_sigmas(machine)
        f2dot35 = 2*numpy.sqrt(2*numpy.log(2))
        sx,sz,sxp,szp = m['sigmaX'],m['sigmaZ'],m["sigmaX'"],m["sigmaZ'"]
        Sx = numpy.sqrt( sx**2 + sr**2)
        Sz = numpy.sqrt( sz**2 + sr**2)
        Sxp = numpy.sqrt( sxp**2 + srp**2)
        Szp = numpy.sqrt( szp**2 + srp**2)

        Wx = f2dot35 * Sx
        Wxp = f2dot35 * Sxp
        Wz = f2dot35 * Sz
        Wzp = f2dot35 * Szp

        print("\n\nSOURCE x,y,x',z' %g  %g  %g  %g  \n"%(Wx,Wz,Wxp,Wzp))
        CF_h = sr * srp / (Sx * Sxp)
        CF_v = sr * srp / (Sz * Szp)
        print("%s CF x = %f"%(machine, CF_h))
        print("%s CF z = %f"%(machine, CF_v))
        print("%s CF = %f percent" % (machine, 1e2 * CF_h * CF_v))






