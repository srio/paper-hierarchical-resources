import numpy
import scipy.constants as codata
from tableElectron import get_sigmas

def get_sigmas_radiation(photon_energy,undulator_length):
    lambdan = 1e-10 * codata.h*codata.c/codata.e*1e10 / photon_energy # in m
    return 1e6*2.740/4/numpy.pi*numpy.sqrt(lambdan*undulator_length),1e6*0.69*numpy.sqrt(lambdan/undulator_length),




if __name__ == "__main__":

    photon_energy = 17225.0
    undulator_length = 1.4

    sr,srp = get_sigmas_radiation(photon_energy,undulator_length)

    print("electron sigmas: ",sr,srp)

    demagX = [2830.0/1170,14495.0/5.0]
    demagZ = 18490.0/10

    # N.A. by KB mirrors
    NAx = 390 / (184.95 - 40)
    NAz = 900 / 184.9

    txt = ""
    for machine in ["ESRF","EBS"]:
        txt += "\n\n %s WITH OPEN VSS =====================================================\n"%machine
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

        txt += "SOURCE x,z,x',z' %g  %g  %g  %g  \n"%(Wx,Wz,Wxp,Wzp)

        txt += "SLIT PLANE       %g  %g  %g  %g  \n"%(Wx/demagX[0],Wzp*40.0,Wxp*demagX[0],Wzp)

        txt += "FOCAL PLANE      %g  %g  %g  %g \n "%(
                        Wx/demagX[0]/demagX[1],
						Wz/demagZ,
                        NAx * demagX[1], # the same if: 390 / (0.05),
                        NAz * demagZ)    # the same if: 900 / (0.10))



        Tx = NAx / (Wxp*demagX[0])
        Tz = NAz / (Wzp)
        txt += "Demagnification H:%f x V:%f \n "%(demagX[0] * demagX[1], demagZ)
        txt += "N.A. [urad]  H:%g  V:%g \n"%(NAx,NAz)
        txt += "Transmission (percent) H: %f, V: %f, H*V: %f\n" % (1e2 * Tx, 1e2 * Tz, 1e2 * Tx * Tz)
        if machine == "ESRF":
            txt += "Flux: %g photons/s\n"%(1.9e15*Tx*Tz)
        else:
            txt += "Flux: %g photons/s\n" % (2.9e15 * Tx * Tz)
        txt += "\n\n\n"


    for machine in ["ESRF"]:
        txt += "\n\n %s WITH 50 um=====================================================\n" % machine
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

        txt += "FOCAL PLANE      %g  %g  %g  %g \n "%(
                        50.0/demagX[1],
						Wz/demagZ,
                        NAx * demagX[1],  # Wxp*demagX[0]*demagX[1],
                        NAz * demagZ)  # Wzp*demagZ)


        NAx = 390/(184.95-40)
        NAz = 900/184.9
        Tx = NAx / (Wxp*demagX[0]) * (1.0/8)
        Tz = NAz / (Wzp)
        txt += "Demagnification H:%f x V:%f \n "%(demagX[0] * demagX[1], demagZ)
        txt += "N.A. H:%f  V:%f \n"%(NAx,NAz)
        txt += "Transmission (percent) H: %f, V: %f, H*V: %f\n"% ( 1e2*Tx, 1e2*Tz, 1e2*Tx*Tz )
        txt += "Flux: %g photons/s\n"%(1.9e15*Tx*Tz)

        txt += "\n\n\n"




    print(txt)
    
    f = open("tableHandCalculations.txt",'w')
    f.write(txt)
    f.close()
    print("File tableHandCalculations.txt written to disk.")






