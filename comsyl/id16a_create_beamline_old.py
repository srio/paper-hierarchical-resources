






#
# ===== Example of python code to create propagate current element =====
#

#
# Import section
#
import numpy
from syned.beamline.beamline_element import BeamlineElement
from syned.beamline.element_coordinates import ElementCoordinates
from syned.beamline.beamline import Beamline

from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters
from wofry.propagator.propagators2D.fresnel_zoom_xy import FresnelZoomXY2D
from srxraylib.plot.gol import plot_image

from comsyl.waveoptics.WOFRYAdapter import ComsylWofryBeamline
import pickle


def get_wofry_beamline_elements():

    BEAMLINE_ELEMENTS = []
    HANDLERS = []
    SPECIFIC = []

    #
    # info on current oe
    #
    #
    #    -------WOScreen---------
    #        -------BoundaryShape---------
    #

    #
    # define current oe
    #
    from wofry.beamline.optical_elements.ideal_elements.screen import WOScreen

    optical_element = WOScreen()




    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=0.000000,    q=28.300000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),    propagation_elements = propagation_elements)
    # #self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 8.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 10.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='FRESNEL_ZOOM_XY_2D')

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel':1,'magnification_x':8.0,'magnification_y':8.0})


    # input_wavefront = output_wavefront

    #
    # info on current oe
    #
    #
    #    -------WOSlit---------
    #        -------Rectangle---------
    #        x_left: -0.0018849 m # x (width) minimum (signed)
    #        x_right: 0.0018849 m # x (width) maximum (signed)
    #        y_bottom: -0.0018849 m # y (length) minimum (signed)
    #        y_top: 0.0018849 m # y (length) maximum (signed)
    #

    #
    # define current oe
    #
    from syned.beamline.shape import Rectangle
    boundary_shape = Rectangle(x_left=-0.0018849,x_right=0.0018849,y_bottom=-0.0018849,y_top=0.0018849)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    optical_element = WOSlit(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=0.000000,    q=0.000000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),    propagation_elements = propagation_elements)
    # #self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 1.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    #
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel':1,'magnification_x':1.0,'magnification_y':1.0})


    #
    # info on current oe
    #
    #
    #    -------WOIdealLens---------
    #        focal_x: 8.319 m # Focal length in x [horizontal]
    #        focal_y: 99999999999999.0 m # Focal length in y [vertical]
    #

    #
    # define current oe
    #
    from wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens

    optical_element = WOIdealLens(name='',focal_x=8.319000,focal_y=99999999999999.000000)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=0.000000,    q=0.000000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),    propagation_elements = propagation_elements)
    # #self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 1.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    #
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})


    #
    # info on current oe
    #
    #
    #    -------WOSlit---------
    #        -------Rectangle---------
    #        x_left: -2.5e-05 m # x (width) minimum (signed)
    #        x_right: 2.5e-05 m # x (width) maximum (signed)
    #        y_bottom: -0.5 m # y (length) minimum (signed)
    #        y_top: 0.5 m # y (length) maximum (signed)
    #

    #
    # define current oe
    #
    from syned.beamline.shape import Rectangle
    boundary_shape = Rectangle(x_left=-2.5e-05,x_right=2.5e-05,y_bottom=-0.5,y_top=0.5)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    optical_element = WOSlit(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,    coordinates=ElementCoordinates(p=11.700000,    q=0.000000,    angle_radial=numpy.radians(0.000000),    angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),    propagation_elements = propagation_elements)
    # #self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 0.010000)
    # propagation_parameters.set_additional_parameters('magnification_y', 1.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,    handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 0.01, 'magnification_y': 1.0})


    #
    #
    # #########################   KB  #########################################
    #
    #

    #
    # info on current oe
    #
    #
    #    -------WOSlit---------
    #        -------Rectangle---------
    #        x_left: -0.025 m # x (width) minimum (signed)
    #        x_right: 0.025 m # x (width) maximum (signed)
    #        y_bottom: -0.00045 m # y (length) minimum (signed)
    #        y_top: 0.00045 m # y (length) maximum (signed)
    #

    #
    # define current oe
    #
    from syned.beamline.shape import Rectangle
    boundary_shape = Rectangle(x_left=-0.025, x_right=0.025, y_bottom=-0.00045, y_top=0.00045)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    optical_element = WOSlit(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=144.900000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
    #                                                propagation_elements=propagation_elements)
    # # self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 440.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 5.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
    #                                              handler_name='FRESNEL_ZOOM_XY_2D')
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 440.0, 'magnification_y': 5.0})


    #
    # info on current oe
    #
    #
    #    -------WOIdealLens---------
    #        focal_x: 100000000.0 m # Focal length in x [horizontal]
    #        focal_y: 0.09994594594594594 m # Focal length in y [vertical]
    #

    #
    # define current oe
    #
    from wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens

    optical_element = WOIdealLens(name='', focal_x=100000000.000000, focal_y=0.099946)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
    #                                                propagation_elements=propagation_elements)
    # # self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 1.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
    #                                              handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})



    #
    # info on current oe
    #
    #
    #    -------WOSlit---------
    #        -------Rectangle---------
    #        x_left: -0.000195 m # x (width) minimum (signed)
    #        x_right: 0.000195 m # x (width) maximum (signed)
    #        y_bottom: -0.0065 m # y (length) minimum (signed)
    #        y_top: 0.0065 m # y (length) maximum (signed)
    #

    #
    # define current oe
    #
    # from syned.beamline.shape import Rectangle
    # boundary_shape = Rectangle(x_left=-0.000195, x_right=0.000195, y_bottom=-0.0065, y_top=0.0065)
    #
    # from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    # optical_element = WOSlit(boundary_shape=boundary_shape)
    #
    # #
    # # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    # #
    # #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
    #                                                propagation_elements=propagation_elements)
    # # self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 0.500000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
    #                                              handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 0.05})



    #
    # info on current oe
    #
    #
    #    -------WOIdealLens---------
    #        focal_x: 0.049982758620701014 m # Focal length in x [horizontal]
    #        focal_y: 100000000.0 m # Focal length in y [vertical]
    #

    #
    # define current oe
    #
    from wofry.beamline.optical_elements.ideal_elements.lens import WOIdealLens

    optical_element = WOIdealLens(name='', focal_x=0.049983, focal_y=100000000.000000)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.000000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
    #                                                propagation_elements=propagation_elements)
    # # self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 1.000000)
    # propagation_parameters.set_additional_parameters('magnification_y', 1.000000)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
    #                                              handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})


    #
    # info on current oe
    #
    #
    #    -------WOSlit---------
    #        -------Rectangle---------
    #        x_left: -0.5 m # x (width) minimum (signed)
    #        x_right: 0.5 m # x (width) maximum (signed)
    #        y_bottom: -0.5 m # y (length) minimum (signed)
    #        y_top: 0.5 m # y (length) maximum (signed)
    #

    #
    # define current oe
    #
    from syned.beamline.shape import Rectangle
    boundary_shape = Rectangle(x_left=-0.5, x_right=0.5, y_bottom=-0.5, y_top=0.5)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    optical_element = WOSlit(boundary_shape=boundary_shape)

    #
    # propagating (***  ONLY THE ZOOM PROPAGATOR IS IMPLEMENTED ***)
    #
    #
    # propagation_elements = PropagationElements()
    beamline_element = BeamlineElement(optical_element=optical_element,
                                       coordinates=ElementCoordinates(p=0.050000, q=0.000000,
                                                                      angle_radial=numpy.radians(0.000000),
                                                                      angle_azimuthal=numpy.radians(0.000000)))
    # propagation_elements.add_beamline_element(beamline_element)
    # propagation_parameters = PropagationParameters(wavefront=input_wavefront.duplicate(),
    #                                                propagation_elements=propagation_elements)
    # # self.set_additional_parameters(propagation_parameters)
    # #
    # propagation_parameters.set_additional_parameters('shift_half_pixel', 1)
    # propagation_parameters.set_additional_parameters('magnification_x', 0.000070)
    # propagation_parameters.set_additional_parameters('magnification_y', 0.000090)
    # #
    # propagator = PropagationManager.Instance()
    # try:
    #     propagator.add_propagator(FresnelZoomXY2D())
    # except:
    #     pass
    # output_wavefront = propagator.do_propagation(propagation_parameters=propagation_parameters,
    #                                              handler_name='FRESNEL_ZOOM_XY_2D')
    #
    #
    # input_wavefront = output_wavefront

    BEAMLINE_ELEMENTS.append(beamline_element)
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 0.000070, 'magnification_y': 0.000090})


    return BEAMLINE_ELEMENTS,HANDLERS,SPECIFIC


def get_wofry_beamline(ELEMENTS,HANDLERS,SPECIFIC,dumpfile=""):

    propagation_elements = PropagationElements()

    for k in range(len(ELEMENTS)):
        propagation_elements.add_beamline_element(beamline_element=ELEMENTS[k], element_parameters=SPECIFIC[k])

    bl = ComsylWofryBeamline.initialize_from_propagator_elements_object(propagation_elements)


    if dumpfile != "":
        pickle.dump(bl, open(dumpfile, "wb"))
        print("File written to disk: ", dumpfile)

def get_syned_beamline(BEAMLINE_ELEMENTS,dumpfile=""):

    beamline = Beamline()


    for ble in BEAMLINE_ELEMENTS:

        beamline.append_beamline_element(ble)

    # print(beamline.to_dictionary())
    # print(beamline.to_full_dictionary())
    # print(beamline.to_json())

    if dumpfile != "":
        f = open(dumpfile,"w")
        f.write(beamline.to_json())
        f.close()
        print("File written to disk: ", dumpfile)

    return bl



if __name__ == "__main__":
    BL_ELEMENTS, HANDLERS, SPECIFIC = get_wofry_beamline_elements()

    bl = get_wofry_beamline(BL_ELEMENTS,HANDLERS,SPECIFIC,dumpfile="id16a.p")

    syned_bl = get_syned_beamline(BL_ELEMENTS,dumpfile="id16a.json")

    # print(bl.info())
    # plot_image(input_wavefront.get_intensity(),1e6*input_wavefront.get_coordinate_x(),1e6*input_wavefront.get_coordinate_y(),aspect="auto")
