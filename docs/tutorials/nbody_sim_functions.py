import numpy as np
import rebound
import astropy.constants as constants


def exomoon_simulation(params):
    """Run a hierarchical N-body simulation with one planet and one moon around the planet. 
    
    Args:
        params (tuple): eccentricity of planet and semi-major axis of moon (in fraction of Hill Radius)
    
    """
    
    # unpack params
    ecc_planet, a_moon = params
    
    # constants
    MEARTH_TO_MSUN = constants.M_earth.value / constants.M_sun.value
    DAY_TO_YEAR = 1. / 365.25
    MIN_DIST = 0.00039   # AU (planet radius)
    MAX_DIST = 0.030     # AU (Hill radius)
    
    # fixed params
    m_star = 1.16                                   # stellar mass
    mass_moon = 0.148 * MEARTH_TO_MSUN              # moon mass 
    mass_planet = 12. * MEARTH_TO_MSUN              # planet mass
    period_planet = 542.08 * DAY_TO_YEAR * 2*np.pi  # planet orbital period
    
    # hyperparams
    sim_time = 1e2  # run for 100 years
    N_outputs = 50
    
    # random mean anomaly for moon
    ma_moon = np.random.uniform(0, 2*np.pi)
    
    # set up simulation
    sim = rebound.Simulation()
    sim.integrator = "ias15"
    
    sim.add(m=m_star, hash="star")  # add star
    sim.add(m=mass_planet, P=period_planet, e=ecc_planet, M=0., inc=np.pi/2, hash="planet")  # add planet around star
    sim.add(m=mass_moon, a=a_moon*MAX_DIST, e=0., M=ma_moon, inc=np.pi/2,
            primary=sim.particles[-1], hash="moon")  # add moon around planet
    
    sim.dt = 0.05 * sim.particles[-1].P  # first timestep is 5% of moon's orbital period
    sim.move_to_com()
    
    sim.exit_min_distance = MIN_DIST  # catch encounters

    # run simulation
    timescale = sim_time * (2 * np.pi)  # units where G=1
    ps = sim.particles  # an array of pointers that will update as the simulation runs
    times = np.linspace(0, timescale, N_outputs)

    try:
        for time in times:
            sim.integrate(time)
            dp_moon = ps["planet"] - ps["moon"]  # calculate the component-wise difference between moon and planet
            dist_sq_moon = dp_moon.x*dp_moon.x + dp_moon.y*dp_moon.y + dp_moon.z*dp_moon.z
            if dist_sq_moon > MAX_DIST**2:
                return 0.  # moon escaped Hill sphere: unstable
            
    except rebound.Encounter:
        return 0.  # close encounter: unstable
    
    return 1.  # stable