
import numpy
from syned.beamline.element_coordinates import ElementCoordinates

from wofry.propagator.propagator import PropagationManager, PropagationElements, PropagationParameters
from wofry.propagator.propagators2D.fresnel_zoom_xy import FresnelZoomXY2D
from srxraylib.plot.gol import plot_image

from comsyl_wofry_beamline import ComsylWofryBeamline
from comsyl_wofry_beamline_element import ComsylWofryBeamlineElement
import pickle


def get_wofry_beamline_elements():

    ELEMENTS = []
    COORDINATES = []
    HANDLERS = []
    SPECIFIC = []

    #
    # info on current oe 0
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.0,q=28.30,angle_radial=0.0,angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel':1,'magnification_x':8.0,'magnification_y':10.0})


    #
    # info on current oe 1
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


    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.0, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel':1,'magnification_x':1.0,'magnification_y':1.0})


    #
    # info on current oe 2
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.0, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})


    #
    # info on current oe 3
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=11.70, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 0.01, 'magnification_y': 1.0})


    #
    #
    # #########################   KB  #########################################
    #
    #

    #
    # info on current oe 4
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=144.9, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 440.0, 'magnification_y': 5.0})


    #
    # info on current oe 5
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.0, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})



    #
    # info on current oe 6
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
    from syned.beamline.shape import Rectangle
    boundary_shape = Rectangle(x_left=-0.000195, x_right=0.000195, y_bottom=-0.0065, y_top=0.0065)

    from wofry.beamline.optical_elements.absorbers.slit import WOSlit
    optical_element = WOSlit(boundary_shape=boundary_shape)

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.05, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 0.5})



    #
    # info on current oe 7
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.0, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 1.0, 'magnification_y': 1.0})


    #
    # info on current oe 8
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

    ELEMENTS.append(optical_element)
    COORDINATES.append(ElementCoordinates(p=0.05, q=0.0, angle_radial=0.0, angle_azimuthal=0.0))
    HANDLERS.append('FRESNEL_ZOOM_XY_2D')
    SPECIFIC.append({'shift_half_pixel': 1, 'magnification_x': 0.000070, 'magnification_y': 0.000090})

    return ELEMENTS,COORDINATES,HANDLERS,SPECIFIC



if __name__ == "__main__":

    do_generate = 0 # 0=generate, 1=read json, 2=read pickle

    if do_generate == 0:
        ELEMENTS, COORDINATES, HANDLERS, SPECIFIC = get_wofry_beamline_elements()
        bl = ComsylWofryBeamline.initialize_from_lists(ELEMENTS,
                                                       COORDINATES,
                                                       HANDLERS,
                                                       SPECIFIC)
        bl.write_file_json("id16a.json")
        bl.write_file_pickle("id16a.p")
    elif do_generate == 1:
        from json_tools import load_from_json_file
        bl = load_from_json_file("id16a.json")
    elif do_generate == 2:
        bl = pickle.load(open("id16a.p","rb"))


    print(bl.info())
    for i in range(bl.get_beamline_elements_number()):
        print(">>>>>>>")
        print(">>>>",i,
              bl.get_beamline_element_at(i).get_optical_element(),
              bl.get_beamline_element_at(i).get_coordinates(),
              bl.get_propagator_handler(i),
              bl.get_propagator_specific_parameters(i))

