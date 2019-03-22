import numpy
import scipy.constants as codata

def get_sigmas(name):

    if name == "ESRF":
        return get_sigmas("ESRF-AT")
    if name == "ESRF-AT":
        # return {'sigmaX':387.8,"sigmaZ":3.5,"sigmaX'":10.3,"sigmaZ'":1.2}
        return {'sigmaX':414.97,"sigmaZ":3.43,"sigmaX'":10.31,"sigmaZ'":1.16}
    if name == "ESRF-ORANGEBOOK":
        return {'sigmaX':387.8,"sigmaZ":3.5,"sigmaX'":10.3,"sigmaZ'":1.2}
    elif name == "EBS":
        # return {'sigmaX':27.2, "sigmaZ":3.4,"sigmaX'":5.2,"sigmaZ'":1.4}
        return get_sigmas("EBS-S28D")
    elif name == "EBS-S28A":
        return {'sigmaX':27.2, "sigmaZ":3.4,"sigmaX'":5.2,"sigmaZ'":1.4}
    elif name == "EBS-S28D":
        return {'sigmaX':30.18, "sigmaZ":3.64,"sigmaX'":4.37,"sigmaZ'":1.37}
    else:
        raise Exception("Unknown storage ring name")

if __name__ == "__main__":


    txt = ""
    for machine in ["ESRF-ORANGEBOOK","ESRF-AT","EBS-S28A","EBS-S28D"]:
        m = get_sigmas(machine)
        txt += "%s  & %4.2f  & %4.2f  & %4.2f & %4.2f \\\\ \n"%(
            machine,m['sigmaX'],m['sigmaZ'],m["sigmaX'"],m["sigmaZ'"])

    print(txt)
    
    f = open("../tableElectron.txt",'w')
    f.write(txt)
    f.close()
    print("File ../tableElectron.txt written to disk.")




