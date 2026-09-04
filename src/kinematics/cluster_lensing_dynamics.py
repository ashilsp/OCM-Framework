"""
Order Creator Mechanism (OCM) - Cluster Gravitational Lensing & Collision Dynamics
Implements the analytical light deflection angle alpha_hat(xi) = (4*G*M_b)/(c^2*xi) + (2*pi*sqrt(G*M_b*a_0))/c^2,
topological lensing potential gradient Phi_kappa, and Bullet Cluster (1E 0657-558) spatial separation
kinematics between gas cores (ram pressure) and topological node centers.
"""

import numpy as np

class ClusterLensingDynamics:
    def __init__(self, a_0: float = 1.2e-10, G: float = 6.67430e-11, c: float = 299792458.0):
        """
        Initialize universal cosmological constants.
        
        :param a_0: Universal cosmic acceleration threshold (m/s^2)
        """
        self.a_0 = a_0
        self.G = G
        self.c = c

    def compute_cluster_deflection_angle(self, xi_impact_parameter_m: float, M_baryonic_kg: float) -> dict:
        """
        Calculates the total analytical cluster deflection angle alpha_hat(xi):
        alpha_hat = alpha_N + alpha_kappa
        alpha_N = (4 * G * M_b) / (c^2 * xi)
        alpha_kappa = (2 * pi * sqrt(G * M_b * a_0)) / c^2
        """
        if xi_impact_parameter_m <= 0.0 or M_baryonic_kg <= 0.0:
            raise ValueError("Impact parameter xi and baryonic mass M_baryonic_kg must be strictly positive.")

        # Classical Newtonian Lensing Angle Component (radians)
        alpha_N = (4.0 * self.G * M_baryonic_kg) / ((self.c ** 2) * xi_impact_parameter_m)
        
        # Scale-Invariant Topological Lensing Deflection Plateau (radians)
        alpha_kappa = (2.0 * np.pi * np.sqrt(self.G * M_baryonic_kg * self.a_0)) / (self.c ** 2)
        
        alpha_total = alpha_N + alpha_kappa
        
        # Convert radians to arcseconds
        rad_to_arcsec = (180.0 / np.pi) * 3600.0

        return {
            "xi_kpc": float(xi_impact_parameter_m / 3.085677581e19),
            "alpha_Newtonian_arcsec": float(alpha_N * rad_to_arcsec),
            "alpha_topological_plateau_arcsec": float(alpha_kappa * rad_to_arcsec),
            "alpha_total_arcsec": float(alpha_total * rad_to_arcsec),
            "topological_boost_ratio": float(alpha_total / alpha_N)
        }

    def evaluate_bullet_cluster_offset(self, 
                                       v_rel_km_s: float = 4500.0, 
                                       tau_coll_yr: float = 1.0e8, 
                                       C_D: float = 1.0, 
                                       A_gas_m2: float = 3.0e42, 
                                       m_gas_kg: float = 1.0e44, 
                                       rho_ext_kg_m3: float = 1.0e-23, 
                                       gamma_kappa: float = 1.0e-16) -> dict:
        """
        Models the Bullet Cluster (1E 0657-558) spatial offset separation delta_x(t) between
        dissipative gas cores (ram pressure) and non-dissipative topological nodes.
        
        delta_x_peak = (C_D * A_gas * rho_ext / (2 * m_gas)) * v_rel^2 * tau_coll^2 * (1 - exp(-gamma_kappa * tau_coll))
        """
        v_rel = v_rel_km_s * 1000.0  # Convert km/s to m/s
        tau_coll = tau_coll_yr * 365.25 * 86400.0  # Convert years to seconds
        
        # Ram-pressure deceleration prefactor
        prefactor = (C_D * A_gas_m2 * rho_ext_kg_m3) / (2.0 * m_gas_kg)
        
        damping_term = 1.0 - np.exp(-gamma_kappa * tau_coll)
        delta_x_peak_meters = prefactor * (v_rel ** 2) * (tau_coll ** 2) * damping_term
        delta_x_peak_kpc = delta_x_peak_meters / 3.085677581e19

        return {
            "relative_velocity_km_s": float(v_rel_km_s),
            "collision_timescale_Myr": float(tau_coll_yr / 1.0e6),
            "delta_x_peak_meters": float(delta_x_peak_meters),
            "delta_x_peak_kpc": float(delta_x_peak_kpc),
            "matches_observed_bullet_offset": bool(np.isclose(delta_x_peak_kpc, 215.0, atol=35.0)),
            "mechanism": "Node core lensing peak decouples from ram-pressure gas core without particle dark matter"
        }
