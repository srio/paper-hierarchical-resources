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

    demagX = [2830.0/1170,14495.0/5.0]
    demagZ = 18490.0/10



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

        txt += "SOURCE x,y,x',z' %g  %g  %g  %g  \n"%(Wx,Wz,Wxp,Wzp)

        txt += "SLIT PLANE       %g  %g  %g  %g  \n"%(Wx/demagX[0],Wzp*40.0,Wxp*demagX[0],Wzp)

        txt += "FOCAL PLANE      %g  %g  %g  %g \n "%(Wx/demagX[0]/demagX[1],
						Wz/demagZ,
						Wxp*demagX[0]*demagX[1],
						Wzp*demagZ)


    txt += "\n\n WITH 50 um\n"
    for machine in ["ESRF"]:
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

        txt += "SOURCE x,y,x',z' %g  %g  %g  %g  \n"%(Wx,Wz,Wxp,Wzp)

        txt += "SLIT PLANE       %g  %g  %g  %g  \n"%(50.0,Wzp*40.0,Wxp*demagX[0],Wzp)

        txt += "FOCAL PLANE      %g  %g  %g  %g \n "%(50.0/demagX[1],
						Wz/demagZ,
						Wxp*demagX[0]*demagX[1],
						Wzp*demagZ)




    print(txt)
    
    f = open("../tableHandCalculations.txt",'w')
    f.write(txt)
    f.close()
    print("File ../tableHandCalculations.txt written to disk.")

    print("Demagnification H x V: ",demagX[0]*demagX[1],demagZ)




