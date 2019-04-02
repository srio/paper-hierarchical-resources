import numpy
from srxraylib.plot.gol import plot_image,plot_surface, plot
import matplotlib.pylab as plt
from comsyl.autocorrelation.CompactAFReader import CompactAFReader


def plot_spectral_density(afp,mode=None,spectral_density=True,do_plot=False,
                          xrange=None,yrange=None,figsize=[9,5],
                          show_profiles=False,filename="",aspect="equal"):

    if spectral_density:
        if mode is None:
            sd = af.spectral_density()
        else:
            sd = af.intensity_from_modes(max_mode_index=mode)
    else:
        sd =  numpy.abs(af.eigenvalue(mode) * af.mode(mode))


    x = afp.x_coordinates()
    y = afp.y_coordinates()


    fig,ax = plot_image(sd,1e6*x,1e6*y,cmap='jet',figsize=figsize,add_colorbar=False,show=0,
                     xtitle="X [$\mu$m]",ytitle="Y [$\mu$m]",title="",aspect=aspect,
                     xrange=xrange,yrange=yrange,)



    # if is_propagated:
    #     ax.xaxis.label.set_size(15)
    #     ax.yaxis.label.set_size(20)
    #     plt.xticks(fontsize=15)
    #     plt.yticks(fontsize=15)
    # else:
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(20)
    plt.yticks([-15,-10,-5,0,5,10,15],fontsize=20)
    plt.xticks(fontsize=20)

    if filename != "":
        plt.savefig(filename) #,dpi=600)
        print("File written to disk: %s"%filename)

    plt.show()

if __name__ == "__main__":


    if True:
        filename_ebs="/scisoft/data/srio/COMSYL/ID16/id16s_ebs_u18_1400mm_1h_new_s1.0.npy"
        af = CompactAFReader.initialize_from_file(filename_ebs)
        plot_spectral_density(af, mode=None, spectral_density=True, do_plot=True, xrange=[-75,75],yrange=[-20,20],figsize=(12,4),      filename="ebs_spectral_density.png")
        plot_spectral_density(af, mode=0,    spectral_density=False, do_plot=True, xrange=[-75./2,75./2],yrange=[-20,20],figsize=(6,4),filename="ebs_mode0.png")
        plot_spectral_density(af, mode=1,    spectral_density=False, do_plot=True, xrange=[-75./2,75./2],yrange=[-20,20],figsize=(6,4),filename="ebs_mode1.png")
        plot_spectral_density(af, mode=2,    spectral_density=False, do_plot=True, xrange=[-75./2,75./2],yrange=[-20,20],figsize=(6,4),filename="ebs_mode2.png")
        plot_spectral_density(af, mode=3,    spectral_density=False, do_plot=True, xrange=[-75./2,75./2],yrange=[-20,20],figsize=(6,4),filename="ebs_mode3.png")


    if False:
        filename_hb ="/scisoft/data/srio/COMSYL/ID16/id16s_hb_u18_1400mm_1h_s1.0.npy"
        af = CompactAFReader.initialize_from_file(filename_hb)
        plot_spectral_density(af, mode=None, spectral_density=True, do_plot=True, xrange=[-1000,1000],yrange=[-20,20],
                              figsize=(12,4),filename="ebs_spectral_density.png",aspect="auto")

        plot_spectral_density(af, mode=0, spectral_density=False, do_plot=True, xrange=[-75. / 2, 75. / 2], yrange=[-20, 20],
                              figsize=(6, 4), filename="ebs_mode0.png")


