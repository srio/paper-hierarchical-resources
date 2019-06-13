import numpy
from srxraylib.plot.gol import plot
from srxraylib.metrology.dabam import dabam
import matplotlib.pylab as plt

def first_version():
    dir = "../Oasys/"
    files = ["ID16A_ML_W-B4C_120Strp","ID16A_KB1_VF","ID16A_KB1_HF"]
    fontsize = 12

    plt.figure(figsize=(10,20))

    plt_counter = 0
    for file in files:
        plt_counter += 1
        plt.subplot(3, 2, plt_counter)
        a = numpy.loadtxt(dir+file+".dat")
        d = dabam()
        d.load_external_profile(a[:,0],a[:,1])


        # plot(1e3*d.y,1e9*d.zHeights,xtitle="X [mm]",ytitle="Height error [nm]",
        #      title=file,
        #      legend="Slope Error RMS = %4.3f urad"%(1e6*d.stdev_profile_slopes()),
        #      show=False)

        plt.plot(1e3*d.y,1e9*d.zHeights)
        plt.xlabel("X [mm]",fontsize=fontsize)
        plt.ylabel("Height error [nm]",fontsize=fontsize)
        # plt.title("Slope Error RMS = %4.3f urad"%(1e6*d.stdev_profile_slopes()))

        # filename = file+"_heights.png"
        # plt.savefig(filename)
        # print("File written to disk: ",filename)
        # plt.show()


        plt_counter += 1
        plt.subplot(3, 2, plt_counter)
        # f3 = plt.figure(3)
        plt.loglog(d.f, d.psdHeights)
        # y = d.f ** (d.powerlaw["hgt_pendent"]) * 10 ** d.powerlaw["hgt_shift"]
        # i0 = d.powerlaw["index_from"]
        # i1 = d.powerlaw["index_to"]
        # plt.loglog(d.f, y)
        # plt.loglog(d.f[i0:i1], y[i0:i1])
        # beta = -d.powerlaw["hgt_pendent"]
        # plt.title("PSD of heights profile (beta=%.2f,Df=%.2f)" % (beta, (5 - beta) / 2))
        plt.xlabel("f [m^-1]",fontsize=fontsize)
        plt.ylabel("PSD [m^3]",fontsize=fontsize)
        # filename = file+"_psd.png"
        # plt.savefig(filename)
        # print("File written to disk: ",filename)
        # plt.show()

    filename = "metrology.eps"
    plt.savefig(filename)
    print("File written to disk: ",filename)
    plt.show()

def second_version(root=""):
    from srxraylib.metrology.dabam import dabam
    import matplotlib.pylab as plt
    entry = 900
    dm = dabam()
    dm.set_input_outputFileRoot("")  # avoid output files
    dm.set_input_silent(1)
    dm.set_entry(entry)
    dm.load()

    dm.inputs["setDetrending"] = -1

    # dm.inputs["plot"] = "heights"
    # dm.plot()
    # plt.show()


    f1 = plt.figure(1)
    plt.plot(1e3 * dm.y, 1e6 * dm.zHeights)
    plt.title('Slope Error RMS: %.3f urad\n'%( 1e6*dm.stdev_profile_slopes() ))
    plt.xlabel("Y [mm]")
    plt.ylabel("Z [um]")
    if root != "":
        filename = "%s_%s.png"%(root,entry)
        plt.savefig(filename)
        print("File written to disk: %s"%filename)
    plt.show()

    print(dm.info_profiles())

if __name__ == "__main__":

    first_version()
    # second_version(root="tmp")

