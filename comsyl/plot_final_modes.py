import matplotlib.pylab as plt



def plot1(z,x,y,xrange=[0,0],yrange=[0,0],xtitle="",ytitle="",title="",filename=""):

    cmap = plt.cm.jet # Greys #cm.coolwarm

    fx = 9
    fy = 9
    figure = plt.figure(figsize=(fx,fy))

    hfactor = 1.0
    vfactor = 1.0

    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    #
    #main plot
    #
    axScatter = figure.add_axes(rect_scatter)

    axScatter.set_xlabel(xtitle)
    axScatter.set_ylabel(ytitle)


    axScatter.axis(xmin=hfactor*xrange[0],xmax=xrange[1])
    axScatter.axis(ymin=vfactor*yrange[0],ymax=yrange[1])

    axScatter.set_aspect(1.0)


    axScatter.pcolormesh(x,y,z.T,cmap=cmap)


    #
    #histograms
    #
    axHistx = figure.add_axes(rect_histx, sharex=axScatter)
    axHisty = figure.add_axes(rect_histy, sharey=axScatter)

    # tmp_h_b = []
    # tmp_h_h = []
    # for s,t,v in zip(hfactor*tkt["bin_h_left"],hfactor*tkt["bin_h_right"],tkt["histogram_h"]):
    #     tmp_h_b.append(s)
    #     tmp_h_h.append(v)
    #     tmp_h_b.append(t)
    #     tmp_h_h.append(v)
    #     tmp_v_b = []
    #     tmp_v_h = []
    # for s,t,v in zip(vfactor*tkt["bin_v_left"],vfactor*tkt["bin_v_right"],tkt["histogram_v"]):
    #     tmp_v_b.append(s)
    #     tmp_v_h.append(v)
    #     tmp_v_b.append(t)
    #     tmp_v_h.append(v)

    hx = z.sum(axis=1)
    hy = z.sum(axis=0)
    axHistx.plot(x,hx)
    axHisty.plot(hy,y)

    tt = numpy.where(hx >= hx.max() * 0.5)
    if hx[tt].size > 1:
        binSize = x[1] - x[0]
        print("FWHM X: ",binSize * (tt[0][-1] - tt[0][0]))


    tt = numpy.where(hy >= hy.max() * 0.5)
    if hx[tt].size > 1:
        binSize = y[1] - y[0]
        print("FWHM Y: ",binSize * (tt[0][-1] - tt[0][0]))



    # supress ordinates labels ans ticks
    axHistx.get_yaxis().set_visible(False)
    axHisty.get_xaxis().set_visible(False)

    # supress abscissas labels (keep ticks)
    for tl in axHistx.get_xticklabels(): tl.set_visible(False)
    for tl in axHisty.get_yticklabels(): tl.set_visible(False)

    if title != None:
        axHistx.set_title(title)

    if filename != "":
        plt.savefig(filename)
        print("File written to disk: %s"%filename)

    plt.show()



if __name__ == "__main__":
    from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction
    from srxraylib.plot.gol import plot_image
    import numpy

    filename = "/users/srio/Oasys/paper-hierarchical-resources/comsyl/propagation_wofry_EBS/rediagonalized.npz"

    af_name = filename.split("/")[-1].replace(".npz", "")

    af = AutocorrelationFunction.load(filename)

    print(af.eigenvalues())


    x = af.xCoordinates()
    y = af.yCoordinates()

    for mode in [0,1]:

        sd0 =  numpy.abs(af.coherentMode(mode))**2

        plot1(sd0,1e9*x,1e9*y,xrange=[-50, 50],yrange=[-50, 50],xtitle="H [nm]",ytitle="V [nm]",filename="/tmp/final_mode%d.png"%mode)



    # spectral density

    sd0 = numpy.abs(af.coherentMode(0))**2
    sd1 = numpy.abs(af.coherentMode(1))**2

    sd = af.eigenvalue(0) * sd0 + af.eigenvalue(1) * sd1
    plot1(sd0,1e9*x,1e9*y,xrange=[-50, 50],yrange=[-50, 50],xtitle="H [nm]",ytitle="V [nm]",filename="/tmp/final_spectral_density.png")


    # fig,ax = plot_image(sd0,1e6*x,1e6*y,cmap='jet',figsize=(6,4),add_colorbar=False,show=1,
    #                  xtitle="X [$\mu$m]",ytitle="Y [$\mu$m]",title="",aspect="equal",
    #                     xrange=[-0.030, 0.030],
    #                     yrange=[-0.030, 0.030],)
