
import numpy
from wofry.propagator.wavefront1D.generic_wavefront import GenericWavefront1D
from syned.beamline.shape import Rectangle
from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates
from wofry.propagator.propagators1D.fresnel_zoom import FresnelZoom1D
from wofry.propagator.propagators1D.integral import Integral1D
from wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens

from srxraylib.plot.gol import plot
import matplotlib.pylab as plt


def get_fwhm_in_microns(wf,string=False):
    import numpy
    x = 1e6 * wf.get_abscissas()
    h = wf.get_intensity()

    #CALCULATE fwhm
    tt = numpy.where(h>=max(h)*0.5)
    if h[tt].size > 1:
        binSize = x[1]-x[0]
        fwhm =binSize*(tt[0][-1]-tt[0][0])
    print("fwhm = ",fwhm)

    if string:
        return "%8.3f"%fwhm
    else:
        return fwhm

def apply_gaussian(in_object_1,shift):
    import numpy
    wf = in_object_1.duplicate()
    # print(dir(wf))
    A = wf.get_complex_amplitude()
    und_length = 1.40
    p = 28.3
    wavelength = wf.get_wavelength()
    print("wavelength = ", wavelength)

    sigma_photons = .69 * numpy.sqrt(wavelength / und_length)
    print(A.shape)
    X = wf.get_abscissas()
    print(X.shape)
    print(X[-1])
    sigma = p * sigma_photons
    # sigmax = 2 * X[-1,-1] / 10
    # sigmay = 2 * Y[-1,-1] / 10
    # print("Sigmas: ",sigmax,sigmay)
    print("sigma_photons (intensity): ", sigma)
    print("sigma (intensity): ", sigma)
    sigma *= numpy.sqrt(2)
    print("sigma (amplitude): ", sigma)
    Gx = numpy.exp(-(X-shift)**2 / 2 / sigma ** 2)
    wf.set_complex_amplitude(A * Gx)
    out_object = wf

    return out_object


def gaussian_wavefront(center,angle):
    #
    # create input_wavefront
    #
    #
    input_wavefront = GenericWavefront1D.initialize_wavefront_from_range(x_min=-0.0028, x_max=0.0028,
                                                                         number_of_points=8192)
    input_wavefront.set_photon_energy(17225)
    input_wavefront.set_spherical_wave(radius=28.3, center=center, complex_amplitude=complex(1, 0))

    #
    # apply Gaussian amplitude
    #
    input_wavefront = apply_gaussian(input_wavefront,shift=28.3*angle)


    return input_wavefront

def ML_size(input_wavefront):
    # note that wavefront 1d will be clipped using the first two coordinates!
    boundary_shape = Rectangle(x_left=-0.0018849, x_right=0.0018849, y_bottom=-0.0018849, y_top=0.0018849)

    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #

    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)

    propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')

    return output_wavefront


#
####################################################
#
# HORIZONTAL BEAMLINE
#
####################################################

def ML_28p3(input_wavefront):
    #
    # define current oe
    #


    optical_element = WOIdealLens(name='', focal_x=8.277750, focal_y=None)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront


def Aperture_40m(input_wavefront):
    # from syned.beamline.shape import Rectangle
    # note that wavefront 1d will be clipped using the first two coordinates!
    boundary_shape = Rectangle(x_left=-2.5e-05, x_right=2.5e-05, y_bottom=-2.5e-05, y_top=2.5e-05)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=11.700000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 0.010000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())

    except:
        pass

    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')

    return output_wavefront


def KBv_Plane(input_wavefront):
    # note that wavefront 1d will be clipped using the first two coordinates!
    boundary_shape = Rectangle(x_left=-0.025, x_right=0.025, y_bottom=-0.025, y_top=0.025)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=144.900000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 220.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront

def KBh_Size(input_wavefront):
    # note that wavefront 1d will be clipped using the first two coordinates!
    boundary_shape = Rectangle(x_left=-0.000195, x_right=0.000195, y_bottom=-0.000195, y_top=0.000195)

    # from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront

def KBh(input_wavefront):
    optical_element = WOIdealLens(name='', focal_x=0.049983, focal_y=None)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront


def Screen_h(input_wavefront,fresnel=True):
    # note that wavefront 1d will be clipped using the first two coordinates!
    boundary_shape = Rectangle(x_left=-0.5, x_right=0.5, y_bottom=-0.5, y_top=0.5)

    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 0.000020)
    #
    propagator = PropagationManager.Instance()
    try:
        if fresnel:
            propagator.add_propagator(FresnelZoom1D())
        else:
            propagator.add_propagator(Integral1D())
    except:
        pass
    if fresnel:
        output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    else:
        output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                     handler_name='INTEGRAL_1D')

    return output_wavefront


#
####################################################
#
# VERTICAL BEAMLINE
#
####################################################
#

def Aperture_40m_V_open(input_wavefront):
    boundary_shape = Rectangle(x_left=-0.5, x_right=0.5, y_bottom=-0.5, y_top=0.5)

    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=11.700000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 0.640000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')

    return output_wavefront




def KBv_Size(input_wavefront):
    boundary_shape = Rectangle(x_left=-0.00045, x_right=0.00045, y_bottom=-0.00045, y_top=0.00045)

    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=144.900000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 5.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')

    return output_wavefront


def KBv(input_wavefront):
    optical_element = WOIdealLens(name='', focal_x=0.099946, focal_y=None)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront


def KBh_Plane(input_wavefront):
    boundary_shape = Rectangle(x_left=-0.0065, x_right=0.0065, y_bottom=-0.0065, y_top=0.0065)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 0.500000)
    #
    propagator = PropagationManager.Instance()
    try:
        propagator.add_propagator(FresnelZoom1D())
    except:
        pass
    output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    return output_wavefront



def Screen_v(input_wavefront,fresnel=True):
    boundary_shape = Rectangle(x_left=-0.5, x_right=0.5, y_bottom=-0.5, y_top=0.5)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit1D
    optical_element = WOSlit1D(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    propagation_elements.add_beamline_element(beamline_element)
    propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
                                                   propagation_elements=propagation_elements)
    # self.set_additional_parameters(propagation_parameters)
    #
    propagation_parameters.set_additional_parameters('magnification_x', 0.000020)
    #
    propagator = PropagationManager.Instance()
    try:
        if fresnel:
            propagator.add_propagator(FresnelZoom1D())
        else:
            propagator.add_propagator(Integral1D())
    except:
        pass

    if fresnel:
        output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                 handler_name='FRESNEL_ZOOM_1D')
    else:
        output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
                                                     handler_name='INTEGRAL_1D')

    return output_wavefront



#
####################################################
#
#
#
####################################################
#


def run_beamline_horizontal(center=0.0,angle=0.0,fresnel=True):

    wf0 = gaussian_wavefront(center=center,angle=angle)
    wf1 = ML_size(wf0)
    wf2 = ML_28p3(wf1)
    wf3 = Aperture_40m(wf2)
    wf4 = KBv_Plane(wf3)
    wf5 = KBh_Size(wf4)
    wf6 = KBh(wf5)
    wf7 = Screen_h(wf6,fresnel=fresnel)

    return wf7


def run_beamline_vertical(center=0.0,angle=0.0,fresnel=True):

    wf0 = gaussian_wavefront(center=center,angle=angle)
    wf1 = ML_size(wf0)
    wf2 = Aperture_40m_V_open(wf1)
    wf3 = KBv_Size(wf2)
    wf4 = KBv(wf3)
    wf5 = KBh_Plane(wf4)
    wf6 = Screen_v(wf5,fresnel=fresnel)

    return wf6

def run_limits():


    wf_h = run_beamline_horizontal( center=0,angle=0)
    # wf_hl = run_beamline_horizontal(center=-35e-6,angle=0)
    # wf_hr = run_beamline_horizontal(center=+35e-6,angle=0)
    wf_hl = run_beamline_horizontal(center=0,angle=-8e-6)
    wf_hr = run_beamline_horizontal(center=0,angle=+8e-6)



    plot(1e6 * wf_h.get_abscissas(), wf_h.get_intensity(),
         1e6 * wf_hl.get_abscissas(), wf_hl.get_intensity(),
         1e6 * wf_hr.get_abscissas(), wf_hr.get_intensity(),
         title="wf_h "+get_fwhm_in_microns(wf_h,string=True),legend=["center","left","right"],show=False)


    plot(1e6 * wf_h.get_abscissas(), wf_h.get_intensity()+wf_hl.get_intensity()+wf_hr.get_intensity(),
         1e6 * wf_h.get_abscissas(), wf_h.get_intensity(),
         title="wf_h "+get_fwhm_in_microns(wf_h,string=True),legend=["sum","center"],show=True)


def run_h():

    wf_h = run_beamline_horizontal( center=0,angle=0,fresnel=False)


    plot(1e9 * wf_h.get_abscissas(), wf_h.get_intensity(),
         xtitle="H [nm]",ytitle="V [nm]",xrange=[-50,50],show=False)

    print(">>>> FWHM V [um]: ",get_fwhm_in_microns(wf_h))
    plt.savefig("/tmp/wofry1Dh.png")
    print("File written to disk: /tmp/wofry1Dh.png")
    plt.show()


def run_v():

    wf_v = run_beamline_vertical( center=0,angle=0,fresnel=False)


    plot(1e9 * wf_v.get_abscissas(), wf_v.get_intensity(),
         xtitle="H [nm]",ytitle="V [nm]",xrange=[-50,50],show=False)

    print(">>>> FWHM V [um]: ",get_fwhm_in_microns(wf_v))
    plt.savefig("/tmp/wofry1Dv.png")
    print("File written to disk: /tmp/wofry1Dv.png")
    plt.show()

if __name__ == "__main__":

    run_h()
    run_v()

    # run_limits()

