#!/usr/bin/python
# coding: utf-8
###################################################################################
# ID16A - OASYS School
# Authors/Contributors: Rafael Celestre, Manuel S. del Rio
# Rafael.Celestre@esrf.eu
# creation: 13.11.2017
# previously updated: 13.11.2017
# last update: 03.05.2019 (v0.2)
###################################################################################

import time
import copy
import numpy as np
import sys
sys.path.insert(0, './srw_python')
from srwlib import *
from uti_plot import *

startTime = time.time()
print('ID16-A simulation') if(srwl_uti_proc_is_master()) else 0
#############################################################################
# Program variables
wfr_resolution = (750, 140)  # nx, ny
screen_range = (-1.75E-3, 1.75e-3, -0.75E-3, 0.75E-3) # x_Start, x_Fin, y_Start, y_Fin
sampling_factor = 0.0  # sampling factor for adjusting nx, ny (effective if > 0)
defocus = 0            # (-) before focus, (+) after focus
MultiE = True          # partially coherent simulation
calculation =  0       # radiation characteristic to calculate (for MultiE):
                       #   0- Total Intensity (s0);
                       #   1- Four Stokes components;
                       #   2- Mutual Intensity Cut vs X;
                       #   3- Mutual Intensity Cut vs Y;
                       #   4- Mutual Intensity Cuts and Degree of Coherence vs X & Y;
                       #  10- Flux
                       #  20- Electric Field (sum of fields from all macro-electrons, assuming CSR)
                       #  40- Total Intensity, Mutual Intensity Cuts and Degree of Coherence vs X & Y;
save = True
plots = False
nMacroElec = 100000    # total number of macro-electrons
directory = 'simulations'

#############################################################################
# Files and folders names
strDataFolderName = directory

source = 'ebs'
prfx = '_idealTE'

strIntPropOutFileName = source + prfx + '_AP_wfr.dat'
strIntPrtlChrnc = source + prfx + '_' + str(nMacroElec/1000)+'k_ME'+'.dat'

#############################################################################
# Beamline assembly
print('\nSetting up beamline\n') if(srwl_uti_proc_is_master()) else 0

beamE = 17.225
Wavelength = srwl_uti_ph_en_conv(beamE, _in_u='keV', _out_u='m')

#============= ABSOLUTE POSITIONS =====================================#
pMltLr = 28.3
pSlt   = 40
pKBV   = 184.90
pKBH   = 184.95
pGBE   = 185

Drft1  = SRWLOptD((pSlt-pMltLr))
Drft2  = SRWLOptD(pKBV-pSlt)
Drft3  = SRWLOptD(pKBH-pKBV)
Drft4  = SRWLOptD(pGBE-pKBH+defocus)

# ============= MULTILAYER(H) ==========================================#
"""Side bounce multi layer horizontal focusing mirror generating a
secondary source on a slit upstream the beamline. Here, the mirror is
represented as a ideal thin lens + an aperture to limit the beam
footprint"""
W_MltLr = 13 * 1E-3
L_MltLr = 120 * 1E-3
grzAngl = 31.42 * 1E-3
oeAptrMltLr = SRWLOptA('r', 'a', L_MltLr * np.sin(grzAngl), W_MltLr)
print(">>>> Dimensions ML: ", L_MltLr * np.sin(grzAngl), W_MltLr) if(srwl_uti_proc_is_master()) else 0

fMltLrh = 1 / ((1 / pMltLr) + (1 / (pSlt - pMltLr)))
fMltLrv = 1E23
oeMltLr = SRWLOptL(_Fx=fMltLrh, _Fy=fMltLrv)

print(">>>> fx, fy: ",fMltLrh, fMltLrv) if(srwl_uti_proc_is_master()) else 0

# ============= VIRTUAL SOURCE SLIT ====================================#
VSS_h = 50 * 1E-6
VSS_v = 3 * 1E-3
oeVSS = SRWLOptA('r', 'a', VSS_h, VSS_v)
print(">>>> Dimensions ML exit slit: ", VSS_h, VSS_v) if(srwl_uti_proc_is_master()) else 0

# ============= KB(V) ==================================================#
"""The fisrt mirror of the KB system has a vertical focusing function.
It takes the beam from the source and focuses if onto the sample. In our
convention, bounce down for for vertical focusing elements."""
W_KBv = 20 * 1E-3
L_KBv = 60 * 1E-3
grzAngl = 14.99 * 1E-3
oeAptrKBv = SRWLOptA('r', 'a', W_KBv, L_KBv * np.sin(grzAngl))
print(">>>> Dimensions KBv: ", W_KBv, L_KBv * np.sin(grzAngl)) if(srwl_uti_proc_is_master()) else 0
fKBv_v = 1 / ((1 / pKBV) + (1 / (pGBE - pKBV)))
fKBv_h = 1E23
oeKBv = SRWLOptL(_Fx=fKBv_h, _Fy=fKBv_v)
print(">>>> fx, fy: ",fKBv_h, fKBv_v) if(srwl_uti_proc_is_master()) else 0

#============= KB(H) ==================================================#
"""The second mirror of the KB system has a horizontal focusing function.
It takes the beam from the virtual source (VSS) and focuses if onto the
sample. In our convention, side bounce for for horizontal focusing
elements."""
W_KBh = 20*1E-3
L_KBh  = 26*1E-3
grzAngl = 14.99*1E-3
oeAptrKBh = SRWLOptA('r','a',L_KBh * np.sin(grzAngl), W_KBh)
print(">>>> Dimensions KBh: ",L_KBh * np.sin(grzAngl), W_KBh) if(srwl_uti_proc_is_master()) else 0
fKBh_v = 1E23
fKBh_h = 1/((1/(pKBH-pSlt))+(1/(pGBE-pKBH)))
oeKBh = SRWLOptL(_Fx=fKBh_h, _Fy=fKBh_v)
print(">>>> fx, fy: ",fKBh_h, fKBh_v) if(srwl_uti_proc_is_master()) else 0

#============= Wavefront Propagation Parameters =======================#
#                [ 0] [1] [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9] [10] [11]
ppAptrMltLr		=[ 0,  0, 1.,   0,   0,  1.,  4.,  1.,  8.,   0,   0,   0]
ppMltLr			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppDrft1 		=[ 0,  0, 1.,   2,   0,  1.,  1.,  1.,  1.,   0,   0,   0] #Par[3] = (1),(2)
ppVSS			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppDrft2			=[ 0,  0, 1.,   2,   0,  1.,  1,   1.,  1.,   0,   0,   0] #Par[3] = (1,1),(1,3),(2,3)
ppAptrKBv		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppKBv			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppDrft3			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppAptrKBh		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppKBh			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
ppDrft4			=[ 0,  0, 1.,   4,   0,  1.,  1.,  3.,  1.,   0,   0,   0] #Par[3] = (1,1,4)*,(1,3,4),(2,3,4)=>bad #range x = 0.8265 um, range y = 1.1211 um
ppFinal			=[ 0,  0, 1.,   0,   0,  1.,0.4,0.25,  1.,   0,   0,   0]

# optBL = SRWLOptC([oeAptrMltLr,oeMltLr,  Drft1, oeVSS,  Drft2, oeAptrKBv, oeKBv,  Drft3,oeAptrKBh, oeKBh,  Drft4],
#                  [ppAptrMltLr,ppMltLr,ppDrft1, ppVSS,ppDrft2, ppAptrKBv, ppKBv,ppDrft3,ppAptrKBh, ppKBh,ppDrft4, ppFinal]
#                  )

optBL = SRWLOptC([oeAptrMltLr,oeMltLr,  Drft1, oeVSS,  Drft2, oeAptrKBv, oeKBv,  Drft3,oeAptrKBh,oeKBh,  Drft4],#],
                 [ppAptrMltLr,ppMltLr,ppDrft1, ppVSS,ppDrft2, ppAptrKBv, ppKBv,ppDrft3,ppAptrKBh,ppKBh,ppDrft4 , ppFinal]
                 )

"""
[ 0]: Auto-Resize (1) or not (0) Before propagation
[ 1]: Auto-Resize (1) or not (0) After propagation
[ 2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
[ 3]: Type of Free-Space Propagator:
       0- Standard Fresnel
       1- Fresnel with analytical treatment of the quadratic (leading) phase terms
       2- Similar to 1, yet with different processing near a waist
       3- For propagation from a waist over a ~large distance
       4- For propagation over some distance to a waist
[ 4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
[ 5]: Horizontal Range modification factor at Resizing (1. means no modification)
[ 6]: Horizontal Resolution modification factor at Resizing
[ 7]: Vertical Range modification factor at Resizing
[ 8]: Vertical Resolution modification factor at Resizing
[ 9]: Type of wavefront Shift before Resizing (not yet implemented)
[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
[11]: New Vertical wavefront Center position after Shift (not yet implemented)
"""
#############################################################################
# Photon source

#********************************Undulator parameters (U20.2)
numPer = 77			# Number of ID Periods
undPer = 0.0183		# Period Length [m]
phB = 0	        	# Initial Phase of the Horizontal field component
sB = 1		        # Symmetry of the Horizontal field component vs Longitudinal position
xcID = 0 			# Transverse Coordinates of Undulator Center [m]
ycID = 0
zcID = 0
n = 1
#********************************Storage ring parameters
eBeam = SRWLPartBeam()
eBeam.Iavg = 0.2             # average Current [A]
eBeam.partStatMom1.x = 0
eBeam.partStatMom1.y = 0
eBeam.partStatMom1.z = -0.5*undPer*(numPer + 4)    # initial Longitudinal Coordinate (set before the ID)
eBeam.partStatMom1.xp = 0  					       # initial Relative Transverse Velocities
eBeam.partStatMom1.yp = 0

# e- beam paramters (RMS) EBS
sigEperE = 9.3E-4  # relative RMS energy spread
sigX = 30.3E-06  # horizontal RMS size of e-beam [m]
sigXp = 4.4E-06  # horizontal RMS angular divergence [rad]
sigY = 3.6E-06  # vertical RMS size of e-beam [m]
sigYp = 1.46E-06  # vertical RMS angular divergence [rad]
eBeam.partStatMom1.gamma = 6.00 / 0.51099890221e-03  # Relative Energy
n = 1
K = np.sqrt(2 * (2 * n * Wavelength * eBeam.partStatMom1.gamma ** 2 / undPer - 1))
B = K / (undPer * 93.3728962)  # Peak Horizontal field [T] (undulator)
print(">>>> SOURCE") if(srwl_uti_proc_is_master()) else 0
print(">>>> K:",K) if(srwl_uti_proc_is_master()) else 0
print(">>>> undPer:",undPer) if(srwl_uti_proc_is_master()) else 0
print(">>>> numPer:",numPer) if(srwl_uti_proc_is_master()) else 0
print(">>>> L:",numPer*undPer) if(srwl_uti_proc_is_master()) else 0
# 2nd order stat. moments
eBeam.arStatMom2[0] = sigX*sigX			 # <(x-<x>)^2>
eBeam.arStatMom2[1] = 0					 # <(x-<x>)(x'-<x'>)>
eBeam.arStatMom2[2] = sigXp*sigXp		 # <(x'-<x'>)^2>
eBeam.arStatMom2[3] = sigY*sigY		     # <(y-<y>)^2>
eBeam.arStatMom2[4] = 0					 # <(y-<y>)(y'-<y'>)>
eBeam.arStatMom2[5] = sigYp*sigYp		 # <(y'-<y'>)^2>
eBeam.arStatMom2[10] = sigEperE*sigEperE # <(E-<E>)^2>/<E>^2

# Electron trajectory
eTraj = 0

# Precision parameters
arPrecSR = [0]*7
arPrecSR[0] = 1		# SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
arPrecSR[1] = 0.01	# relative precision
arPrecSR[2] = 0		# longitudinal position to start integration (effective if < zEndInteg)
arPrecSR[3] = 0		# longitudinal position to finish integration (effective if > zStartInteg)
arPrecSR[4] = 20000	# Number of points for trajectory calculation
arPrecSR[5] = 1		# Use "terminating terms"  or not (1 or 0 respectively)
arPrecSR[6] = sampling_factor # sampling factor for adjusting nx, ny (effective if > 0)	# -1 @Petra
sampFactNxNyForProp = arPrecSR[6] # sampling factor for adjusting nx, ny (effective if > 0)

und = SRWLMagFldU([SRWLMagFldH(n, 'v', B, phB, sB, 1)], undPer, numPer)

magFldCnt = SRWLMagFldC([und], array('d', [xcID]), array('d', [ycID]), array('d', [zcID]))

#********************************Wavefronts

# Monochromatic wavefront
wfr = SRWLWfr()
wfr.allocate(1, wfr_resolution[0], wfr_resolution[1])  # Photon Energy, Horizontal and Vertical Positions
wfr.mesh.zStart = pMltLr
wfr.mesh.eStart = beamE * 1E3
wfr.mesh.xStart = screen_range[0]
wfr.mesh.xFin = screen_range[1]
wfr.mesh.yStart = screen_range[2]
wfr.mesh.yFin = screen_range[3]
wfr.partBeam = eBeam
meshPartCoh = deepcopy(wfr.mesh)

#############################################################################
# Wavefront generation and beam propagation
if(srwl_uti_proc_is_master()):
    # ********************************Calculating Initial Wavefront and extracting Intensity:
    print('- Performing Initial Electric Field calculation ... ')
    srwl.CalcElecFieldSR(wfr, eTraj, magFldCnt, arPrecSR)
    print('Initial wavefront:')
    print('Nx = %d, Ny = %d' % (wfr.mesh.nx, wfr.mesh.ny))
    print('dx = %.4f um, dy = %.4f nm' % ((wfr.mesh.xFin-wfr.mesh.xStart)*1E6/wfr.mesh.nx,
                                          (wfr.mesh.yFin-wfr.mesh.yStart)*1E6/wfr.mesh.ny))
    print('range x = %.4f mm, range y = %.4f mm' % ((wfr.mesh.xFin-wfr.mesh.xStart)*1E3,
                                                    (wfr.mesh.yFin-wfr.mesh.yStart)*1E3))


    # ********************************Electrical field propagation
    print('- Simulating Electric Field Wavefront Propagation ... ')
    srwl.PropagElecField(wfr, optBL)
    print('Propagated wavefront:')
    print('Nx = %d, Ny = %d' % (wfr.mesh.nx, wfr.mesh.ny))
    print('dx = %.4f nm, dy = %.4f nm' % ((wfr.mesh.xFin-wfr.mesh.xStart)*1E9/wfr.mesh.nx,
                                          (wfr.mesh.yFin-wfr.mesh.yStart)*1E9/wfr.mesh.ny))
    print('range x = %.4f nm, range y = %.4f nm' % ((wfr.mesh.xFin-wfr.mesh.xStart)*1E9,
                                                    (wfr.mesh.yFin-wfr.mesh.yStart)*1E9))

    print('>> single electron calculations: done')
    arI1 = array('f', [0] * wfr.mesh.nx * wfr.mesh.ny)  # "flat" 2D array to take intensity data
    srwl.CalcIntFromElecField(arI1, wfr, 6, 0, 3, wfr.mesh.eStart, 0, 0)
    arP1 = array('d', [0] * wfr.mesh.nx * wfr.mesh.ny)  # "flat" array to take 2D phase data (note it should be 'd')
    srwl.CalcIntFromElecField(arP1, wfr, 0, 4, 3, wfr.mesh.eStart, 0, 0)
    srwl_uti_save_intens_ascii(arI1, wfr.mesh, os.path.join(os.getcwd(), strDataFolderName, strIntPropOutFileName), 0)

    # arI1 = array('f', [0] * wfr.mesh.nx * wfr.mesh.ny)  # "flat" 2D array to take intensity data
    # srwl.CalcIntFromElecField(arI1, wfr, 6, 0, 3, wfr.mesh.eStart, 0, 0)
    # arP1 = array('d', [0] * wfr.mesh.nx * wfr.mesh.ny)  # "flat" array to take 2D phase data (note it should be 'd')
    # srwl.CalcIntFromElecField(arP1, wfr, 0, 4, 3, wfr.mesh.eStart, 0, 0)
    # plotMesh1x = [1E6 * wfr.mesh.xStart, 1E6 * wfr.mesh.xFin, wfr.mesh.nx]
    # plotMesh1y = [1E6 * wfr.mesh.yStart, 1E6 * wfr.mesh.yFin, wfr.mesh.ny]
    # uti_plot2d(arI1, plotMesh1x, plotMesh1y,
    #            ['Horizontal Position [um]', 'Vertical Position [um]', 'Intensity After Propagation'])
    # uti_plot2d(arP1, plotMesh1x, plotMesh1y,
    #            ['Horizontal Position [um]', 'Vertical Position [um]', 'Phase After Propagation'])
    #
    # uti_plot_show()  # show all graphs (blocks script execution; close all graph windows to proceed)

print('\ncalculation finished') if (srwl_uti_proc_is_master()) else 0

if MultiE:
    print('- Simulating Partially-Coherent Wavefront Propagation... ') if(srwl_uti_proc_is_master()) else 0
    nMacroElecAvgPerProc = 10   # number of macro-electrons / wavefront to average on worker processes
    nMacroElecSavePer = 100     # intermediate data saving periodicity (in macro-electrons)
    srCalcMeth = 1              # SR calculation method
    srCalcPrec = 0.01           # SR calculation rel. accuracy
    radStokesProp = srwl_wfr_emit_prop_multi_e(eBeam, magFldCnt, meshPartCoh, srCalcMeth, srCalcPrec, nMacroElec,
                                               nMacroElecAvgPerProc, nMacroElecSavePer, os.path.join(os.getcwd(),
                                               strDataFolderName, strIntPrtlChrnc), sampFactNxNyForProp, optBL, _char=calculation)
    print('>> multi electron electron calculations: done') if(srwl_uti_proc_is_master()) else 0

deltaT = time.time() - startTime
hours, minutes = divmod(deltaT, 3600)
minutes, seconds = divmod(minutes, 60)
print("\n>>>> Elapsed time: " + str(int(hours)) + "h " + str(int(minutes)) + "min " + str(seconds) + "s ") if(srwl_uti_proc_is_master()) else 0