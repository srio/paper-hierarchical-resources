
import pickle
import numpy

from comsyl.waveoptics.ComsylWofryBeamline import ComsylWofryBeamline
from comsyl.waveoptics.SRWAdapter import ComsylSRWBeamline

from comsyl.autocorrelation.AutocorrelationFunction import AutocorrelationFunction


def create_beamline_srw_new(load_from_file=None,slit_width=5e-6,slit_height=5e-6,source_offset=0.0,dumpfile=None):

    from srwlib import srwl_uti_proc_is_master, SRWLOptD, SRWLOptL, SRWLOptA, SRWLOptC
    import pickle

    if load_from_file is not None:
        return pickle.load(open(load_from_file,"rb"))

    if not srwl_uti_proc_is_master(): exit()

    ####################################################
    # BEAMLINE

    srw_oe_array = []
    srw_pp_array = []
    drift_before_oe_0 = SRWLOptD(36.0+source_offset)
    pp_drift_before_oe_0 = [0,0,1.0,0,0,8.0,0.5,10.0,0.5,0,0.0,0.0]

    srw_oe_array.append(drift_before_oe_0)
    srw_pp_array.append(pp_drift_before_oe_0)


    oe_1=SRWLOptL(_Fx=18.0, _Fy=18.0, _x=0.0, _y=0.0)
    pp_oe_1 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

    srw_oe_array.append(oe_1)
    srw_pp_array.append(pp_oe_1)

    drift_before_oe_2 = SRWLOptD(32.0)
    pp_drift_before_oe_2 = [0,0,1.0,0,0,0.4,1.0,0.25,1.0,0,0.0,0.0]

    srw_oe_array.append(drift_before_oe_2)
    srw_pp_array.append(pp_drift_before_oe_2)

    oe_2=SRWLOptA(_shape='r',
                   _ap_or_ob='a',
                   _Dx=slit_width,
                   _Dy=slit_height,
                   _x=0.0,
                   _y=0.0)
    pp_oe_2 = [0,0,1.0,0,0,1.0,1.0,1.0,1.0,0,0.0,0.0]

    srw_oe_array.append(oe_2)
    srw_pp_array.append(pp_oe_2)

    drift_before_oe_3 = SRWLOptD(2.0)
    pp_drift_before_oe_3 = [0,0,1.0,0,0,0.3,5.0,0.25,2.0,0,0.0,0.0]

    srw_oe_array.append(drift_before_oe_3)
    srw_pp_array.append(pp_drift_before_oe_3)


    optBL = SRWLOptC(srw_oe_array, srw_pp_array)


    if dumpfile is not None:
        pickle.dump(ComsylSRWBeamline(optBL), open(dumpfile,"wb"))
        print("File written to disk: ",dumpfile)


    return ComsylSRWBeamline(optBL)

def create_beamline_wofry():

    from id16a_create_beamline import get_wofry_beamline_elements
    ELEMENTS, COORDINATES, HANDLERS, SPECIFIC = get_wofry_beamline_elements()
    bl = ComsylWofryBeamline.initialize_from_lists(ELEMENTS,
                                                   COORDINATES,
                                                   HANDLERS,
                                                   SPECIFIC)
    return bl

def propagate_single_mode(af,i,beamline):


    from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters
    from syned.beamline.beamline_element import BeamlineElement
    from syned.beamline.element_coordinates import ElementCoordinates
    from wofry.propagator.propagators2D.fresnel_zoom_xy import FresnelZoomXY2D

    from wofry.propagator.wavefront2D.generic_wavefront import GenericWavefront2D
    from wofry.beamline.optical_elements.ideal_elements.screen import WOScreen

    mi = af.coherentMode(i)
    evi = af.eigenvalue(i)

    print("propagating mode index",i,evi,mi.shape)


    input_wavefront = GenericWavefront2D.initialize_wavefront_from_arrays(x_array=af.xCoordinates(),
                                                                          y_array=af.yCoordinates(),
                                                                          z_array=mi*numpy.sqrt(evi),
                                                                          )
    i0 = input_wavefront.get_integrated_intensity()

    input_wavefront.set_photon_energy(17226.0)

    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoomXY2D())
    except:
        pass

    wfp = beamline.propagate(input_wavefront,propagator)

    i1 = wfp[-1].get_integrated_intensity()

    return wfp,i1/i0



if __name__ == "__main__":


    method = 'WOFRY'
    lattice = "EBS"

    if lattice == "EBS":
        python_to_be_used = "/users/srio/OASYS1.1d/miniconda3/bin/python"
        filename = "/scisoft/data/srio/COMSYL/ID16/id16s_ebs_u18_1400mm_1h_new_s1.0.npz"
    else:
        python_to_be_used = "/scisoft/users/srio/COMSYL_CONDA/miniconda3/bin/python"
        filename = "/scisoft/data/srio/COMSYL/ID16/id16s_hb_u18_1400mm_1h_s1.0.npz"

    python_to_be_used = "/scisoft/users/srio/COMSYL_CONDA/miniconda3/bin/python"


    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++ method =     %s   lattice: %s"%(method,lattice))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


    autocorrelation_function = AutocorrelationFunction.load(filename)

    #
    # source offfset
    #
    source_position=autocorrelation_function.info().sourcePosition()
    if source_position == "entrance":
        source_offset = autocorrelation_function._undulator.length() * 0.5 #+ 2 * comparer.undulator().periodLength()
        print("Using source position entrance z=%f" % source_offset)
    elif source_position == "center":
        source_offset = 0.0
        print("Using source position center z=%f" % source_offset)
    else:
        raise Exception("Unhandled source position")

    print(">>>>> Using source position center z=%f" % source_offset)



    if method == 'SRW':
        #
        # SRW
        #

        comsyl_beamline = create_beamline_srw_new(slit_width=25e-6,slit_height=25e-6,source_offset=0,
                                              dumpfile="bl.p")

        comsyl_beamline.add_undulator_offset(offset=source_offset,p_or_q="q")
        # print(">>>>>>>>>***************",source_offset,comsyl_beamline.get_native_beamline().arOpt[0].L)

        # comsyl_beamline = create_beamline_srw_new(load_from_file="bl.p")

        # directory_name = "propagation_EBS_25x25"
    elif method == 'WOFRY':
        #
        # WOFRY
        #
        comsyl_beamline = create_beamline_wofry()
        print("????OFFSET: ",source_offset)
        print("\n\n????BEFORE: ")
        print(comsyl_beamline.info())

        comsyl_beamline.add_undulator_offset(source_offset)
        print("\n\n????AFTER: ")
        print(comsyl_beamline.info())

        directory_name = "propagation_wofry_%s"%lattice


    #
    # propagate single mode
    #

    if False:
        from srxraylib.plot.gol import plot_image
        nmodes = 5
        mode_transmission = numpy.zeros(nmodes)
        for i in range(5):
            wfp, itrans = propagate_single_mode(autocorrelation_function,i,comsyl_beamline)
            plot_image(wfp[-1].get_intensity())
            mode_transmission[i] = itrans

        for i in range(5):
            print("Mode index: %d, transmission: %f"%(i,mode_transmission[i]))

    #
    # propagate all modes
    #

    if True:
        # Mode
        # index: 0, transmission: 0.232206
        # Mode
        # index: 1, transmission: 0.020266
        # Mode
        # index: 2, transmission: 0.098194
        # Mode
        # index: 3, transmission: 0.026601
        # Mode
        # index: 4, transmission: 0.062042
        number_of_modes = 10
        af_propagated = comsyl_beamline.propagate_af(autocorrelation_function,
                                                     directory_name=directory_name,
                                                     af_output_file_root="%s/propagated_beamline"%(directory_name),
                                                     maximum_mode=number_of_modes, python_to_be_used=python_to_be_used)


        # for i in range(number_of_modes):
        #     print("Mode index: %d, transmission: %g, %g" % (i,
        #                                                     (numpy.abs(autocorrelation_function.coherentMode(i))**2).sum(),
        #                                                     (numpy.abs(af_propagated.coherentMode(i))**2).sum(),
        #     ))
        # for i in range(number_of_modes):
        #     print("Mode index: %d, eigenvalue: %g, %g" % (i, autocorrelation_function.eigenvalue(i).sum().real,af_propagated.eigenvalue(i).sum().real)) #/autocorrelation_function.coherentMode(i).sum()))
