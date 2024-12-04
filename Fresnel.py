"""
FRESNEL EQUATIONS

This file contains Fresnel equations and supporting calculations.
Function summary:
	Fresnel amplitude equations (s and p polarized)
	Fresnel Irradiance equations (s and p polarized)
	Snell's law
	retardance and diattenuation calculations
	example code to test calculation speed
	test cases against known results and published literature

Decreasing phase convention assumed (n + i k)
Incident material assumed real-valued refractive index.
Transmitted irradiance defined immediately after interface.
Angles have units of radians.

"Inc" refers to incident material (assumed real-valued)
"Sub" refers to the transmitted (substrate) material (may be complex-valued)
"thetaInc" is the incident angle (assumed real-valued in range 0 <= thetaInc < pi/2) [units = radians]

This calculation only uses functions from standard library.
Test cases and time trial results can be evaluated with following command:
python3 Fresnel.py




© 2022 Arizona Board of Regents on behalf of the University Of Arizona 
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Arizona (USA) Required Clauses:
1.1. Arbitration. The Parties hereby acknowledge that this Agreement may be subject to arbitration in accordance with applicable law and court rules.
1.2. Applicable Law and Venue. This Agreement shall be interpreted pursuant to the laws of the State of Arizona. Any arbitration or litigation between the Parties shall be conducted in Pima County, Arizona, and LICENSEE hereby submits to venue and jurisdiction in Pima County, Arizona.
1.3. Non-Discrimination. The Parties agree to be bound by state and federal laws and regulations governing equal opportunity and non-discrimination and immigration.
1.4. Appropriation of Funds. The Parties recognize that performance by ARIZONA may depend upon appropriation of funds by the State Legislature of Arizona. If the Legislature fails to appropriate the necessary funds, or if ARIZONA’S appropriation is reduced during the fiscal year, ARIZONA may cancel this Agreement without further duty or obligation. ARIZONA will notify LICENSEE as soon as reasonably possible after it knows of the loss of funds.
1.5. Conflict of Interest. This Agreement is subject to the provisions of A.R.S. 38-511 and other conflict of interest regulations.  Within three years of the EFFECTIVE DATE, ARIZONA may cancel this Agreement if any person significantly involved in initiating, negotiating, drafting, securing, or creating this Agreement for or on behalf of ARIZONA becomes an employee or consultant in any capacity of LICENSEE with respect to the subject matter of this Agreement.
"""

# 2022-10-12 - fix: conservation of energy for transmission into metal - Greg Smith
# 2022-Sept - initial implementation - Greg Smith

from cmath import asin, sqrt, phase, sin, cos
from math import pi, atan

def SnellAngle(nInc, nSub, thetaInc):
	""" Transmitted (substrate) angle according to Snell's Law. Complex-valued. [radians]"""
	return asin(nInc*sin(thetaInc)/nSub)


# Fresnel amplitude equations
def rs(nInc, nSub, thetaInc):
	""" electric field amplitude, s-polarized, reflected"""
	nSq = nSub/nInc
	nSq *= nSq
	cosThetaInc = cos(thetaInc)
	sinThetaIncSq = sin(thetaInc)
	sinThetaIncSq *= sinThetaIncSq
	sqrtTerm = sqrt(nSq - sinThetaIncSq)
	return (cosThetaInc - sqrtTerm)/(cosThetaInc + sqrtTerm)

def rp(nInc, nSub, thetaInc):
	""" electric field amplitude, p-polarized, reflected"""
	nSq = nSub/nInc
	nSq *= nSq
	cosThetaInc = cos(thetaInc)
	sinThetaIncSq = sin(thetaInc)
	sinThetaIncSq *= sinThetaIncSq
	sqrtTerm = sqrt(nSq - sinThetaIncSq)
	return (nSq*cosThetaInc - sqrtTerm)/(nSq*cosThetaInc + sqrtTerm)

def ts(nInc, nSub, thetaInc):
	""" electric field amplitude, s-polarized, transmitted"""
	nSq = nSub/nInc
	nSq *= nSq
	cosThetaInc = cos(thetaInc)
	sinThetaIncSq = sin(thetaInc)
	sinThetaIncSq *= sinThetaIncSq
	return 2.0*cosThetaInc / (cosThetaInc + sqrt(nSq - sinThetaIncSq))

def tp(nInc, nSub, thetaInc):
	""" electric field amplitude, p-polarized, transmitted"""
	nRatio = nSub/nInc
	nRatioSq = nRatio*nRatio
	cosThetaInc = cos(thetaInc)
	sinThetaIncSq = sin(thetaInc)
	sinThetaIncSq *= sinThetaIncSq
	return (2.0*nRatio*cosThetaInc) / (nRatioSq*cosThetaInc + sqrt(nRatioSq - sinThetaIncSq))


# Fresnel irradiance equations
def Rs(nInc, nSub, thetaInc):
	""" irradiance, s-polarized, reflected"""
	rsVal = rs(nInc, nSub, thetaInc)
	return abs(rsVal*rsVal)

def Rp(nInc, nSub, thetaInc):
	""" irradiance, p-polarized, reflected"""
	rpVal = rp(nInc, nSub, thetaInc)
	return abs(rpVal*rpVal)

def Ts(nInc, nSub, thetaInc):
	""" irradiance, s-polarized, transmitted (absorbing materials require careful consideration of scale factor for energy conservation)"""
	thetaSub = SnellAngle(nInc, nSub, thetaInc)
	tsVal = ts(nInc, nSub, thetaInc)
	scale2 = nSub * cos(thetaSub)
	TsVal = abs(tsVal*tsVal) * scale2.real/(nInc.real*cos(thetaInc))
	return TsVal.real

def Tp(nInc, nSub, thetaInc):
	""" irradiance, p-polarized, transmitted (absorbing materials require careful consideration of scale factor for energy conservation)"""
	thetaSub = SnellAngle(nInc, nSub, thetaInc)
	cosThetaSub = cos(thetaSub)
	tpVal = tp(nInc, nSub, thetaInc)
	TpVal = abs(tpVal*tpVal) * (nSub.real*cosThetaSub.real + nSub.imag*cosThetaSub.imag) / (nInc.real * cos(thetaInc))
	return TpVal.real


# polarization calculations
def Diattenuation(irrad1, irrad2):
	""" diattenuation """
	return abs(irrad1-irrad2)/(irrad1+irrad2)

def Retardance(Efield1, Efield2):
	""" retardance [radians]"""
	return phase(Efield1)-phase(Efield2)





# test cases
testPrecision = 0.001	# some references have limited precision
def CompareComplex(var1, var2):
	"""helper function to compare two complex numbers"""
	return(abs(var1.real-var2.real) < testPrecision and \
		abs(var1.imag-var2.imag) < testPrecision
	)

def testFresnel():
	""" compute all test results and display to screen """
	if not testIdealGlassNormal():
		print('testIdealGlassNormal: failed')
	if not testBrewster():
		print('testBrewster: failed')
	if not testCritical():
		print('testCritical: failed')
	if not testFresnelRhomb():
		print('testFresnelRhomb: failed')
	if not testFresnelMetal1():
		print('testFresnelMetal1: failed')
	if not testFresnelMetal2():
		print('testFresnelMetal2: failed')
	combinedTest = \
		testIdealGlassNormal() and \
		testBrewster() and \
		testCritical() and \
		testFresnelRhomb() and \
		testFresnelMetal1() and \
		testFresnelMetal2()
	print('all FRESNEL TESTS passed? '+str(combinedTest))
        
# ideal glass n = 1.5 at normal incidence
# expected values for amplitude and irradiance known from theory
# see "Principles of Optics", Born and Wolf, 6th ed. sec. 1.5.2., eqn. 22-23, p.41
def testIdealGlassNormal():
	return(
		CompareComplex(ts(1,1.5,0), 0.8) and \
		CompareComplex(tp(1,1.5,0), 0.8) and \
		CompareComplex(rs(1,1.5,0), -0.2) and \
		CompareComplex(rp(1,1.5,0), 0.2) and \
		abs(Rs(1,1.5,0) - 0.04)<testPrecision and \
		abs(Rp(1,1.5,0) - 0.04)<testPrecision and \
		abs(Ts(1,1.5,0) - 0.96)<testPrecision and \
		abs(Tp(1,1.5,0) - 0.96)<testPrecision and \
		abs(Diattenuation(Rs(1,1.5,0), Rp(1,1.5,0)))<testPrecision and \
		abs(Diattenuation(Ts(1,1.5,0), Tp(1,1.5,0)))<testPrecision and \
		abs(Retardance(ts(1,1.5,0), tp(1,1.5,0)))<testPrecision and \
		abs(Retardance(rs(1,1.5,0), rp(1,1.5,0))-pi)<testPrecision)

# Brewster angle with semi-arbitrary (real-valued) refractive indices (high-to-low)
# p-polarized reflection should be zero and transmitted irradiance 100%
def testBrewster():
	n1 = 1.72
	n2 = 1.15
	thetaB = atan(n2.real/n1)
	return(
		CompareComplex(rp(n1,n2,thetaB), 0) and \
		abs(Rp(n1,n2,thetaB))<testPrecision and \
		abs(Tp(n1,n2,thetaB) - 1)<testPrecision and \
		abs(Diattenuation(Rs(n1,n2,thetaB), Rp(n1,n2,thetaB))-1)<testPrecision)

# Critical angle with semi-arbitrary (real-valued) refractive indices (high-to-low)
# both polarization irradiance should be 100% reflected and 0% transmitted
def testCritical():
	n1 = 1.72
	n2 = 1.15
	thetaC = asin(n2.real/n1)
	return(
		abs(Rs(n1,n2,thetaC) - 1)<testPrecision and \
		abs(Rp(n1,n2,thetaC) - 1)<testPrecision and \
		abs(Ts(n1,n2,thetaC))<testPrecision and \
		abs(Tp(n1,n2,thetaC))<testPrecision and \
		abs(Diattenuation(Rs(n1,n2,thetaC), Rp(n1,n2,thetaC)))<testPrecision)


# angles where Fresnel rhomb gives 1/8-wave retardance
# from text book: Born and Wolf, "Principles of Optics", 6th ed. section 1.5, below equation 63, p.50.
def testFresnelRhomb():
	n1 = 1.51
	n2 = 1.0
	theta1 = 0.84852090	# 48 degrees, 37 arc-min
	theta2 = 0.95324066	# 54 degrees, 37 arc-min
	return(
		abs(Retardance(rs(n1,n2,theta1), rp(n1,n2,theta1)) - pi/4)<testPrecision and \
		abs(Rs(n1,n2,theta1) + Ts(n1,n2,theta1) - 1.0)<testPrecision and \
		abs(Rp(n1,n2,theta1) + Tp(n1,n2,theta1) - 1.0)<testPrecision and \
		abs(Retardance(rs(n1,n2,theta2), rp(n1,n2,theta2)) - pi/4)<testPrecision and \
		abs(Rs(n1,n2,theta2) + Ts(n1,n2,theta2) - 1.0)<testPrecision and \
		abs(Rp(n1,n2,theta2) + Tp(n1,n2,theta2) - 1.0)<testPrecision)
				

# metal reflection: gold at 582 nm using data interpolated from https://RefractiveIndex.info
# theory results from P. B. Johnson and R. W. Christy. "Optical constants of the noble metals", Phys. Rev. B 6, 4370-4379 (1972). https://doi.org/10.1103/PhysRevB.6.4370
def testFresnelMetal1():
	n1 = 1.0
	n2 = complex(0.29006,2.8628)
	thetaInc = 0.87266463	# 50 degrees
	return(
		abs(Rs(n1,n2,thetaInc) - 0.92516)<testPrecision and \
		abs(Rp(n1,n2,thetaInc) - 0.83233)<testPrecision and \
		abs(Rs(n1,n2,thetaInc) + Ts(n1,n2,thetaInc) - 1.0)<testPrecision and \
		abs(Rp(n1,n2,thetaInc) + Tp(n1,n2,thetaInc) - 1.0)<testPrecision)

# metal reflection: nickel at 632.8 nm
# theory results from M. Chiu, J. Lee, and D. Su. "Complex refractive-index measurement based on Fresnel's equations and the uses of heterodyne interferometry," Appl.Opt. 38, 4047-4052 (1999). https://doi.org/10.1364/AO.38.004047
def testFresnelMetal2():
	n1 = 1.0
	n2 = complex(2.007, 3.781)
	thetaInc = 1.0471976	# 60 degrees
	return(
		CompareComplex(rs(n1,n2,thetaInc), complex(-0.882373, -0.183978)) and \
		CompareComplex(rp(n1,n2,thetaInc), complex(0.462133, 0.492465)) and \
		abs(Retardance(rp(n1,n2,thetaInc), rs(n1,n2,thetaInc)) - 3.7532)<testPrecision and \
		abs(Rs(n1,n2,thetaInc) + Ts(n1,n2,thetaInc) - 1.0)<testPrecision and \
		abs(Rp(n1,n2,thetaInc) + Tp(n1,n2,thetaInc) - 1.0)<testPrecision)






# Example
# Calculate transmitted s-polarized irradiance for nTrial random materials and angles
if __name__ == '__main__':
	from random import random
	from time import time

	# evaluate test cases
	testFresnel()


	# TIME TEST
	# create tuples of data with random incident angles and random refractive indices
	nTrials = 1000
	nInc = tuple(random()*2.0 for x in range(nTrials))							# real-valued
	nSub = tuple(complex(random()*2.0, random()*10.0) for x in range(nTrials))	# complex valued
	thetaInc = tuple(random()*1.570796326 for x in range(nTrials))				# any angle in range [0, pi/2]

	# compute transmitted irradiance values
	tic = time()
	TsVal = tuple(map(Ts,nInc,nSub,thetaInc))
	toc = time()

	# display statistics
	print("nTrials: %d    time: %.3f sec    TsMin: %.3f    TsMax: %.3f" % (nTrials, toc-tic, min(TsVal), max(TsVal)))
