

def u18_ebs(K,SLIT):
    #
    # script to make the calculations (created by XOPPY:undulator_spectrum)
    #
    from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_spectrum
    energy, flux, spectral_power, cumulated_power = xoppy_calc_undulator_spectrum(
        ELECTRONENERGY=6.0,
        ELECTRONENERGYSPREAD=0.00093339,
        ELECTRONCURRENT=0.2,
        ELECTRONBEAMSIZEH=3.01836e-05,
        ELECTRONBEAMSIZEV=3.63641e-06,
        ELECTRONBEAMDIVERGENCEH=4.36821e-06,
        ELECTRONBEAMDIVERGENCEV=1.37498e-06,
        PERIODID=0.0183,
        NPERIODS=77,
        KV=K,
        DISTANCE=27.1,
        GAPH=SLIT,
        GAPV=SLIT,
        PHOTONENERGYMIN=3000.0,
        PHOTONENERGYMAX=55000.0,
        PHOTONENERGYPOINTS=2000,
        METHOD=2,
        USEEMITTANCES=1)

    return energy, flux #, spectral_power, cumulated_power

def u18_esrf(K,SLIT):
    #
    # script to make the calculations (created by XOPPY:undulator_spectrum)
    #
    from orangecontrib.xoppy.util.xoppy_undulators import xoppy_calc_undulator_spectrum
    energy, flux, spectral_power, cumulated_power = xoppy_calc_undulator_spectrum(
        ELECTRONENERGY=6.037,
        ELECTRONENERGYSPREAD=0.0011,
        ELECTRONCURRENT=0.2,
        ELECTRONBEAMSIZEH=0.000414971,
        ELECTRONBEAMSIZEV=3.43353e-06,
        ELECTRONBEAMDIVERGENCEH=1.03149e-05,
        ELECTRONBEAMDIVERGENCEV=1.16498e-06,
        PERIODID=0.0183,
        NPERIODS=77,
        KV=K,
        DISTANCE=27.1,
        GAPH=SLIT,
        GAPV=SLIT,
        PHOTONENERGYMIN=3000.0,
        PHOTONENERGYMAX=55000.0,
        PHOTONENERGYPOINTS=2000,
        METHOD=2,
        USEEMITTANCES=1)

    return energy, flux  # , spectral_power, cumulated_power
    #
    # end script
    #



if __name__ == "__main__":

    import matplotlib.pylab as plt

    e_ebs_1, f_ebs_1 = u18_ebs(K=0.411, SLIT=0.001)
    e_esrf_1, f_esrf_1 = u18_esrf(K=0.411, SLIT=0.001)

    print("maximum flux EBS (slit=1mm) : %g"%f_ebs_1.max())
    print("maximum flux ESRF (slit=1mm) : %g"%f_esrf_1.max())


    # example plot
    from srxraylib.plot.gol import plot
    plot(e_ebs_1, f_ebs_1,
         e_esrf_1, f_esrf_1,
         legend=["EBS","ESRF",],
         ytitle="Flux [photons/s/0.1%bw]", xtitle="Photon energy [eV]", title="",
         xlog=False, ylog=False, show=False)

    plt.savefig("/tmp/fluxU18.png",dpi=300)
    print("File /tmp/fluxU18.png written to disk.")
    plt.show()
