import numpy
from srxraylib.plot.gol import plot
from srxraylib.metrology.dabam import dabam
import matplotlib.pylab as plt


dir = "../Oasys/"
files = ["ID16A_ML_W-B4C_120Strp","ID16A_KB1_VF","ID16A_KB1_HF"]


for file in files:
    a = numpy.loadtxt(dir+file+".dat")
    d = dabam()
    d.load_external_profile(a[:,0],a[:,1])
    # d.inputs["plot"]="slopes"
    # d.plot()
    plot(1e3*d.y,1e9*d.zHeights,xtitle="X [mm]",ytitle="Height error [nm]",
         title=file,
         legend="Slope Error RMS = %4.3f urad"%(1e6*d.stdev_profile_slopes()),
         show=False)

    plt.savefig(file+".png")
    print("File written to disk: ",file+".png")
    plt.show()

    # print(">>",file,1e6*d.stdev_profile_slopes(),1e6*d.zSlopes.std())
    # d.inputs["plot"]="psd_s"
    # d.plot()
