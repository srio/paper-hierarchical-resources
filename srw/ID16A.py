#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# Wave propagation through ID16A - U18.3 - 17.225keV mode
# Author: Rafael Celestre
# Rafael.Celestre@esrf.fr
# 13.11.2017
#############################################################################
#from __future__ import print_function #Python 2.7 compatibility
from srwlib import *
# from uti_plot import *
# from math import *
# import os
# import copy
from srw_aux_tools import tic,toc,plot_wfr,dump_open,dump_wfr,dump_close, srwl_wfr_emit_prop_multi_e_NEW
# import scipy.constants as codata
# import numpy


#
# main code
#
Plots    = "oasys"		# "off", "on" or "oasys" Generates graphical results only when MultiE is set to 'off'

if Plots == "on": #SRW plots
	from uti_plots import *
elif Plots == "oasys": # other plots
	try:
		import matplotlib.pylab as plt
		plt.switch_backend("Qt5Agg")
	except:
		raise Exception("Failed to set matplotlib backend to Qt5Agg")


def main():

	tic()

	print('\nWave propagation through ID16A - U18.3 - 17.225keV mode\n')

	#############################################################################
	# Program variables
	defocus  = 0		# (-) before focus, (+) after focus
	MultiE   = "off"	# Multi -e calculation when set to 'on' ('off')
	Debug    = "off"	# Debug mode disables saving data and speeds simulation

	Errors   = "off"	# loads (or not - off) errors for the optics
	ThnElmnt = "on"	# ThnElmnt = "on" uses Thin Lenses for all optical elements
	Source	 = "ebs"
	nMacroElec = 3 # 50000	# total number of macro-electrons
	directory  = '/ID16A'
	DumpH5File = "on"
	#############################################################################



	# Files and folders names
	if (Errors.lower() == 'on'):
		oeErr = "_Err"
	else:
		oeErr = "_noErr"

	if (ThnElmnt.lower() == 'on'):
		Prfx = "_TE"	#Thin Element
	else:
		Prfx = "_OE"	#Optical Element

	strDataFolderName = 'simulations'+directory
	strIntPropOutFileName  = Source+Prfx+"_d"+str(defocus)+'_AP_intensity'+oeErr+'.dat'
	strPhPropOutFileName   = Source+Prfx+"_d"+str(defocus)+'_AP_phase'+oeErr+'.dat'
	strIntPrtlChrnc 	   = Source+Prfx+"_"+str(nMacroElec/1000)+"k_d"+str(defocus)+'_ME_AP_intensity'+oeErr+'.dat'

	print(Source + ' lattice, ' + Prfx +' optics, ' + oeErr + ' optics errors\n')
	#############################################################################
	# Beamline assembly
	print("\nSetting up beamline\n")
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
	Drft5  = SRWLOptD(-defocus)

	#============= MULTILAYER(H) ==========================================#
	"""Side bounce multi layer horizontal focusing mirror generating a
	secondary source on a slit upstream the beamline. Here, the mirror is
	represented as a ideal thin lens + an aperture to limit the beam
	footprint"""
	W_MltLr = 13*1E-3
	L_MltLr = 120*1E-3
	grzAngl = 31.42*1E-3
	oeAptrMltLr = SRWLOptA('r','a',L_MltLr*sin(grzAngl),W_MltLr)
	print(">>>> Dimensions ML: ",L_MltLr*sin(grzAngl),W_MltLr)

	if (ThnElmnt.lower() == 'on'):
		fMltLrh = 1/((1/pMltLr)+(1/(pSlt-pMltLr)))
		fMltLrv = 1E23
		oeMltLr = SRWLOptL(_Fx=fMltLrh, _Fy=fMltLrv)
	else:
		oeMltLr = SRWLOptMirEl(_p = pMltLr,_q=(pSlt-pMltLr) ,_ang_graz=grzAngl,_r_sag=1E23,	_size_tang=L_MltLr, _size_sag=W_MltLr, _nvx=cos(grzAngl), _nvy=0, _nvz=-sin(grzAngl), _tvx=-sin(grzAngl), _tvy=0)

	if (Errors.lower() == 'on'):
		# Loading 1D mirror slope error from .dat file
		heightProfData = srwl_uti_read_data_cols(os.path.join(os.getcwd(), strDataFolderName, 'optics', 'ID16A_ML_W-B4C_120Strp.dat'), _str_sep='\t', _i_col_start=0, _i_col_end=1)
		oeMLerr = srwl_opt_setup_surf_height_1d(heightProfData, _dim='x', _ang=grzAngl, _amp_coef=1) # _dim='x' for side bounce
	#============= VIRTUAL SOURCE SLIT ====================================#
	VSS_h = 50*1E-6
	VSS_v = 3*1E-3
	oeVSS = SRWLOptA('r','a',VSS_h,VSS_v)
	print(">>>> Dimensions ML exit slit: ",VSS_h,VSS_v)
	#============= KB(V) ==================================================#
	"""The fisrt mirror of the KB system has a vertical focusing function.
	It takes the beam from the source and focuses if onto the sample. In our
	convention, bounce down for for vertical focusing elements."""
	W_KBv = 20*1E-3
	L_KBv = 60*1E-3
	grzAngl = 14.99*1E-3
	oeAptrKBv = SRWLOptA('r','a',W_KBv,L_KBv*sin(grzAngl))
	print(">>>> Dimensions KBv: ",W_KBv,L_KBv*sin(grzAngl))

	if (ThnElmnt.lower() == 'on'):
		fKBv_v = 1/((1/pKBV)+(1/(pGBE-pKBV)))
		fKBv_h =1E23
		oeKBv = SRWLOptL(_Fx=fKBv_h, _Fy=fKBv_v)
	else:
		oeKBv = SRWLOptMirEl(_p = pKBV,_q=(pGBE-pKBV) ,_ang_graz=grzAngl,_r_sag=1E23,_size_tang=L_KBv, _size_sag=W_KBv, _nvx=0, _nvy=cos(grzAngl), _nvz=-sin(grzAngl), _tvx=0, _tvy=-sin(grzAngl))

	if (Errors.lower() == 'on'):
		#Loading 1D mirror slope error from .dat file
		heightProfData = srwl_uti_read_data_cols(os.path.join(os.getcwd(), strDataFolderName, 'optics', 'ID16A_KB1_VF.dat'), _str_sep='\t', _i_col_start=0, _i_col_end=1)
		oeKBverr = srwl_opt_setup_surf_height_1d(heightProfData, _dim='y', _ang=grzAngl, _amp_coef=1)
	#============= KB(H) ==================================================#
	"""The second mirror of the KB system has a horizontal focusing function.
	It takes the beam from the virtual source (VSS) and focuses if onto the
	sample. In our convention, side bounce for for horizontal focusing
	elements."""
	W_KBh = 20*1E-3
	L_KBh  = 26*1E-3
	grzAngl = 14.99*1E-3
	oeAptrKBh = SRWLOptA('r','a',L_KBh*sin(grzAngl),W_KBh)
	print(">>>> Dimensions KBh: ",L_KBh*sin(grzAngl),W_KBh)

	if (ThnElmnt.lower() == 'on'):
		fKBh_v = 1E23
		fKBh_h = 1/((1/(pKBH-pSlt))+(1/(pGBE-pKBH)))
		oeKBh = SRWLOptL(_Fx=fKBh_h, _Fy=fKBh_v)
	else:
		oeKBh = SRWLOptMirEl(_p=(pKBH-pSlt),_q=(pGBE-pKBH),_ang_graz=grzAngl,_r_sag=1E23,_size_tang=L_KBh, _size_sag=W_KBh, _nvx=cos(grzAngl), _nvy=0, _nvz=-sin(grzAngl), _tvx=-sin(grzAngl), _tvy=0)

	if (Errors.lower() == 'on'):
		#Loading 1D mirror slope error from .dat file
		heightProfData = srwl_uti_read_data_cols(os.path.join(os.getcwd(), strDataFolderName, 'optics', 'ID16A_KB1_HF.dat'), _str_sep='\t', _i_col_start=0, _i_col_end=1)
		oeKBherr = srwl_opt_setup_surf_height_1d(heightProfData, _dim='x', _ang=grzAngl, _amp_coef=1)

	if (ThnElmnt.lower() == "on"):
		#============= Wavefront Propagation Parameters =======================#
		#                [ 0] [1] [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9] [10] [11]
		ppAptrMltLr		=[ 0,  0, 1.,   0,   0,  1.,  8.,  1.,  8.,   0,   0,   0]
		ppMltLr			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppMLerr			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft1 		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0] #Par[3] = (1),(2)
		ppVSS			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft2			=[ 0,  0, 1.,   1,   0,  1.,  1,   1.,  1.,   0,   0,   0] #Par[3] = (1,1),(1,3),(2,3)
		ppAptrKBv		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBv			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBverr		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft3			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppAptrKBh		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBh			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBherr		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft4			=[ 0,  0, 1.,   4,   0,  1.,  1.,  1.,  1.,   0,   0,   0] #Par[3] = (1,1,4)*,(1,3,4),(2,3,4)=>bad
		ppFinal			=[ 0,  0, 1.,   0,   0,  1.,  1., 0.5,  2.,   0,   0,   0]
	else:
		#============= Wavefront Propagation Parameters =======================#
		#                [ 0] [1] [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9] [10] [11]
		ppAptrMltLr		=[ 0,  0, 1.,   0,   0,  1.,  8.,  1.,  8.,   0,   0,   0]
		ppMltLr			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppMLerr			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft1 		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0] #Par[3] = (1),(2)
		ppVSS			=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft2			=[ 0,  0, 1.,   1,   0,  1.,  1,   1.,  1.,   0,   0,   0] #Par[3] = (1,1),(1,3),(2,3)
		ppAptrKBv		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBv			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBverr		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft3			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppAptrKBh		=[ 0,  0, 1.,   0,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBh			=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppKBherr		=[ 0,  0, 1.,   1,   0,  1.,  1.,  1.,  1.,   0,   0,   0]
		ppDrft4			=[ 0,  0, 1.,   4,   0,  1.,  1.,  1.,  1.,   0,   0,   0] #Par[3] = (1,1,4)*,(1,3,4),(2,3,4)=>bad
		ppFinal			=[ 0,  0, 1.,   0,   0,  1.,  1., 0.5,  2.,   0,   0,   0]


	if (Errors.lower() == 'on'):
		optBL = SRWLOptC([oeAptrMltLr,], # oeMltLr,oeMLerr,  Drft1, oeVSS,  Drft2,oeAptrKBv,oeKBv,oeKBverr,  Drft3,oeAptrKBh,oeKBh,oeKBherr,  Drft4],
						 [ppAptrMltLr,], # ppMltLr,ppMLerr,ppDrft1, ppVSS,ppDrft2,ppAptrKBv,ppKBv,ppKBverr,ppDrft3,ppAptrKBh,ppKBh,ppKBherr,ppDrft4,ppFinal]
						 )
	else:
		optBL = SRWLOptC([oeAptrMltLr,], #oeMltLr,  Drft1, oeVSS,  Drft2,oeAptrKBv,oeKBv,  Drft3,oeAptrKBh,oeKBh,  Drft4],
						 [ppAptrMltLr,], #ppMltLr,ppDrft1, ppVSS,ppDrft2,ppAptrKBv,ppKBv,ppDrft3,ppAptrKBh,ppKBh,ppDrft4,ppFinal]
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
	if (Source.lower() == 'ebs'):
		# e- beam paramters (RMS) EBS
		sigEperE = 9.3E-4 			# relative RMS energy spread
		sigX  = 30.3E-06			# horizontal RMS size of e-beam [m]
		sigXp = 4.4E-06				# horizontal RMS angular divergence [rad]
		sigY  = 3.6E-06				# vertical RMS size of e-beam [m]
		sigYp = 1.46E-06			# vertical RMS angular divergence [rad]
		eBeam.partStatMom1.gamma = 6.00/0.51099890221e-03 # Relative Energy
		n = 1
		K = sqrt(2*(2*n*Wavelength*eBeam.partStatMom1.gamma**2 /undPer -1))
		B = K/(undPer*93.3728962)	# Peak Horizontal field [T] (undulator)
	else:
		# e- beam paramters (RMS) ESRF @ high beta
		sigEperE = 1.1E-3 			# relative RMS energy spread
		sigX  = 410.3E-06			# horizontal RMS size of e-beam [m]
		sigXp = 10.3E-06			# horizontal RMS angular divergence [rad]
		sigY  = 3.4E-06				# vertical RMS size of e-beam [m]
		sigYp = 1.2E-06			# vertical RMS angular divergence [rad]
		eBeam.partStatMom1.gamma = 6.04/0.51099890221e-03 # Relative Energy
		n = 1
		K = sqrt(2*(2*n*Wavelength*eBeam.partStatMom1.gamma**2 /undPer -1))
		B = K/(undPer*93.3728962)	# Peak Horizontal field [T] (undulator)

	print(">>>> K:",K)
	print(">>>> undPer:",undPer)
	print(">>>> numPer:",numPer)
	print(">>>> L:",numPer*undPer)
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
	arPrecSR[6] = 0		# sampling factor for adjusting nx, ny (effective if > 0)	# -1 @Petra

	sampFactNxNyForProp = 0 # sampling factor for adjusting nx, ny (effective if > 0)

	und = SRWLMagFldU([SRWLMagFldH(n, 'v', B, phB, sB, 1)], undPer, numPer)

	magFldCnt = SRWLMagFldC([und], array('d', [xcID]), array('d', [ycID]), array('d', [zcID]))

	#********************************Wavefronts
	# Monochromatic wavefront
	wfr = SRWLWfr()
	wfr.allocate(1, 256, 256)  # Photon Energy, Horizontal and Vertical Positions
	wfr.mesh.zStart = pMltLr
	wfr.mesh.eStart = beamE*1E3
	wfr.mesh.eFin = wfr.mesh.eStart
	wfr.mesh.xStart = -2.0*1E-3
	wfr.mesh.xFin = - wfr.mesh.xStart
	wfr.mesh.yStart = -1*1E-3
	wfr.mesh.yFin = - wfr.mesh.yStart
	wfr.partBeam = eBeam

	meshPartCoh = deepcopy(wfr.mesh)

	#############################################################################
	# Wavefront generation and beam propagation
	if(srwl_uti_proc_is_master()):

		#********************************Calculating Initial Wavefront and extracting Intensity:
		print('- Performing Initial Electric Field calculation ... ')
		srwl.CalcElecFieldSR(wfr, eTraj, magFldCnt, arPrecSR)

		#############################################################################
		# Graphical representation of results
		if Plots.lower() == 'on':
		#********************************Electrical field intensity and phase after propagation
			plotMesh1x = [1E6*wfr.mesh.xStart, 1E6*wfr.mesh.xFin, wfr.mesh.nx]
			plotMesh1y = [1E6*wfr.mesh.yStart, 1E6*wfr.mesh.yFin, wfr.mesh.ny]
			uti_plot2d(arI1, plotMesh1x, plotMesh1y, ['Horizontal Position [um]', 'Vertical Position [um]', 'Intensity After Propagation'])
			uti_plot2d(arP1, plotMesh1x, plotMesh1y, ['Horizontal Position [um]', 'Vertical Position [um]', 'Phase After Propagation'])

			uti_plot_show() # show all graphs (blocks script execution; close all graph windows to proceed)

		if Plots.lower() == 'oasys':
			arI1,x,y = plot_wfr(wfr,kind='intensity',title='Source Intensity at ' + str(wfr.mesh.eStart) + ' eV',
					 xtitle='Horizontal Position [um]',
					 ytitle='Vertical Position [um]',show=True)



		if DumpH5File == "on":
			filename = "tmp.h5"
			f = dump_open(filename)
			dump_wfr(f,wfr,prefix="source")

		#********************************Electrical field propagation
		print('- Simulating Electric Field Wavefront Propagation ... ')

		srwl.PropagElecField(wfr, optBL)
		arI1 = array('f', [0]*wfr.mesh.nx*wfr.mesh.ny) # "flat" 2D array to take intensity data
		srwl.CalcIntFromElecField(arI1, wfr, 6, 0, 3, wfr.mesh.eStart, 0, 0)


		if Debug.lower() == 'off':
			srwl_uti_save_intens_ascii(arI1, wfr.mesh, os.path.join(os.getcwd(), strDataFolderName, strIntPropOutFileName), 0)

		arP1 = array('d', [0]*wfr.mesh.nx*wfr.mesh.ny) # "flat" array to take 2D phase data (note it should be 'd')
		srwl.CalcIntFromElecField(arP1, wfr, 0, 4, 3, wfr.mesh.eStart, 0, 0)

		if Debug.lower() == 'off':
			srwl_uti_save_intens_ascii(arP1, wfr.mesh, os.path.join(os.getcwd(), strDataFolderName, strPhPropOutFileName), 0)

		if DumpH5File == "on":
			dump_wfr(f,wfr,prefix="focus")
			dump_close(f)
			print("File written to disk: %s"%(filename))
			f.close()

		print('   done')

	if MultiE.lower() == 'on':
		print('- Simulating Partially-Coherent Wavefront Propagation by summing-up contributions of SR from individual electrons (takes time)... ')
		nMacroElecAvgPerProc = 1 # 10	# number of macro-electrons / wavefront to average on worker processes before sending data to master (for parallel calculation only)
		nMacroElecSavePer = 1 # 100		# intermediate data saving periodicity (in macro-electrons)
		srCalcMeth = 1				# SR calculation method
		srCalcPrec = 0.01			# SR calculation rel. accuracy
		radStokesProp = srwl_wfr_emit_prop_multi_e_NEW(eBeam, magFldCnt, meshPartCoh, srCalcMeth, srCalcPrec,
													   nMacroElec, nMacroElecAvgPerProc, nMacroElecSavePer,
													   os.path.join(os.getcwd(), strDataFolderName, strIntPrtlChrnc),
													   sampFactNxNyForProp, optBL,_char=0,
													   filename="tmp_e.h5",save_individual_electrons=True)
		print('   done')

	toc()

	#############################################################################
	# Graphical representation of results
	if (MultiE.lower() == 'off') and (Plots.lower() == 'on'):
	#********************************Electrical field intensity and phase after propagation
		plotMesh1x = [1E6*wfr.mesh.xStart, 1E6*wfr.mesh.xFin, wfr.mesh.nx]
		plotMesh1y = [1E6*wfr.mesh.yStart, 1E6*wfr.mesh.yFin, wfr.mesh.ny]
		uti_plot2d(arI1, plotMesh1x, plotMesh1y, ['Horizontal Position [um]', 'Vertical Position [um]', 'Intensity After Propagation'])
		uti_plot2d(arP1, plotMesh1x, plotMesh1y, ['Horizontal Position [um]', 'Vertical Position [um]', 'Phase After Propagation'])

		uti_plot_show() # show all graphs (blocks script execution; close all graph windows to proceed)

	if (MultiE.lower() == 'off') and (Plots.lower() == 'oasys'):
		arI1,x,y = plot_wfr(wfr,kind='intensity',title='Focal Intensity at ' + str(wfr.mesh.eStart) + ' eV',
				 xtitle='Horizontal Position [um]',
				 ytitle='Vertical Position [um]',show=True)


	print('\ncalculation finished\n')


if __name__ == "__main__":
	main()