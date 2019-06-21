import numpy
import scipy.constants as codata

def k_value(und_dict, photon_energy, electron_energy=6.0):

    gamma = electron_energy* 1e9 / (codata.m_e *  codata.c**2 / codata.e)
    lambdan = codata.h*codata.c/codata.e*1e10 / photon_energy # in A

    harm_number = -1
    KK = -1
    while KK < 0:
        harm_number += 2
        lambda1 = lambdan * harm_number
        KK = ( 2*( (1e-10*lambda1)/(1e-3*und_dict['period']) *2*gamma*gamma  - 1))

    return numpy.sqrt(KK),harm_number

if __name__ == "__main__":

    #u26 = {'name':"IVU26", 'period':26.0, 'length':2.5, 'number':1}
    u18 = {'name':"U18.3", 'period':18.3, 'length':1.4, 'number':2}
    u22 = {'name':"U22.4", 'period':22.4, 'length':1.4, 'number':2}

    undulators = [u18,u22]
    energies = [6.04,6.0]
    rings = ["ESRF","EBS"]

    txt = ""
    for ie,e in enumerate(energies):
        for u in undulators:
            k11, n11 = k_value(u,11200,e)
            k17, n17 = k_value(u,17050,e)
            k33, n33 = k_value(u,33600,e)
            txt += " %s-%s  & %4.2f  & %4.2f  & %d & %5.3f(n=%d) & %5.3f(n=%d) & %5.3f(n=%d)\\\\ \n"%(
                rings[ie],u['name'],u['period'],u['length'],u['number'],k11,n11,k17,n17,k33,n33)
        if ie ==0: txt += "\hline\n"

    print(txt)

    f = open("/tmp/tableUndulator.txt",'w')
    f.write(txt)
    f.close()
    print("File /tmp/tableUndulator.txt written to disk.")




