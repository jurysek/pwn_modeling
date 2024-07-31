import astropy.units as u
import numpy as np
from astropy.constants import astropyconst20 as const
import gappa as gp

def development(power_law_spectrum, age, t, snr, pwn, distance):

    # Setup gamera Particle object
    fp = gp.Particles()
    fp.SetCustomInjectionSpectrum(power_law_spectrum)

    # Adding IC photon fields
    # CMB
    u_cmb = 4.17 * 10**-13
    t_cmb = 2.726
    fp.AddThermalTargetPhotons(t_cmb, u_cmb) #in K, erg/cm^3.

    # FIR
    t_fir = 20; u_fir = 0.3 * gp.eV_to_erg
    fp.AddThermalTargetPhotons(t_fir,u_fir)

    # Adding lists of environmental variables for time development
    tim = t.to_value(u.yr)
    b_field = pwn.magnetic_field(t).to("G").value # this should be in Gauss
    radius = pwn.radius(t).to("pc").value # This should be in PC
    dt = t[1:]-t[:-1]
    #dt.append(dt[-1])
    v_pwn = pwn.radius(t[:-1]).to("cm").value / dt.to_value(u.s) # in cm/s
    v_pwn = np.append(v_pwn, v_pwn[-1])

    # Big question, is this a luminosity, i.e. dE/dt? Shouldn't it be integrated energy in dt?
    # Gamera tutorials suggest that this is the total energy at time t (in ergs), which does not make much sense to me...
    # It is called luminosity anyway, so I use psr luminosity at time t!
    lum = pwn.pulsar.luminosity_spindown(t).to("erg/s").value

    fp.SetLuminosityLookup(list(zip(tim, lum)))
    fp.SetBField(list(zip(tim, b_field)))
    fp.SetExpansionVelocity(list(zip(tim, v_pwn)))
    fp.SetRadius(list(zip(tim, radius)))

    fp.SetAge(age) # in yrs
    fp.CalculateElectronSpectrum()
    sp  = np.array(fp.GetParticleSpectrum()) # returns diff. spectrum: E(erg) vs dN/dE (1/erg)
    p_sed = np.array(np.array(fp.GetParticleSED()))

    # Radiation
    fr = gp.Radiation()
    fr.AddArbitraryTargetPhotons(fp.GetTargetPhotons()) # output from 'Particles' is in the right format to be used in 'Radiation'

    # Synchrotron
    #b = pwn.magnetic_field(tim[0]).to("G").value[0]
    b = np.interp(age, tim, b_field)
    fr.SetBField(b)

    #fr.SetAmbientDensity(density)
    if distance is not None:
        fr.SetDistance(distance)
    fr.SetElectrons(sp)
    # define energies at which gamma-ray emission should be calculated
    eg = np.logspace(3,16,1000) * gp.eV_to_erg
    fr.CalculateDifferentialPhotonSpectrum(eg)

    tot = np.array(fr.GetTotalSED())  # SED, E^2dNdE (erg/s/cm^2) vs E (TeV)
    ic = np.array(fr.GetICSED())
    #brems = np.array(fr.GetBremsstrahlungSED())
    synch = np.array(fr.GetSynchrotronSED())

    # integrated energy flux (int_e^inf dE E*dN/dE, units: erg / cm^2 / s) times area of the sphere erg/s
    total_radiated_energy = fr.GetIntegralTotalEnergyFlux(eg[0],eg[-1]) * 4 * np.pi * (distance * u.pc).to_value(u.cm)**2

    return sp, p_sed, tot, ic, synch, total_radiated_energy

def run_particle_developemnt(power_law_spectrum, age, t, snr, pwn, distance):
    return age, development(power_law_spectrum, age, t, snr, pwn, distance)
