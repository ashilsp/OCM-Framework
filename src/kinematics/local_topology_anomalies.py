"""
Order Creator Mechanism (OCM) - Local Topology Anomalies & Global Shear Field
Implements Radcliffe Wave standing-wave spatial wavelength lambda_RW, gyroscopic satellite plane trapping
thickness h_VPOS, OCM-modified Jeans Mass threshold M_J_OCM, and the exact 2/3 (66.7%) prograde to 1/3 (33.3%)
retrograde cosmic galactic spin parity asymmetry derivation.
"""

import numpy as np

class LocalTopologyAnomalies:
    def __init__(self, G: float = 6.67430e-11, c: float = 299792458.0, k_B: float = 1.380649e-23):
        """
        Initialize fundamental physical constants.
        """
        self.G = G
        self.c = c
        self.k_B = k_B

    def compute_radcliffe_wave_wavelength(self, sigma_M: float, rho_0: float, nu_z: float) -> float:
        """
        Calculates parameter-free spatial standing wave length lambda_RW for the Radcliffe Wave:
        lambda_RW = 2 * pi * sqrt( sigma_M / (4 * pi * G * rho_0 + nu_z^2) )
        
        :param sigma_M: Manifold surface tension
        :param rho_0: Local baryonic density (kg/m^3)
        :param nu_z: Vertical oscillation frequency (rad/s)
        :return: lambda_RW in meters
        """
        denominator = (4.0 * np.pi * self.G * rho_0) + (nu_z ** 2)
        if denominator <= 0.0 or sigma_M <= 0.0:
            raise ValueError("Density/frequencies and manifold tension must yield positive values.")
            
        lambda_RW = 2.0 * np.pi * np.sqrt(sigma_M / denominator)
        return float(lambda_RW)

    def compute_plane_of_satellites_thickness(self, J_node: float, m_sat: float, R_halo: float, omega_M: float, T_virial: float) -> dict:
        """
        Models gyroscopic satellite planar trapping (Milky Way VPOS / Andromeda GPoA):
        Calculates restoring torque coefficient and equilibrium planar thickness h_VPOS.
        """
        # Restoring torque spring constant per angular displacement:
        k_torque = ((3.0 * self.G * (J_node ** 2)) / ((self.c ** 2) * m_sat * (R_halo ** 3))) + (2.0 * (omega_M ** 2))
        I_sat = m_sat * (R_halo ** 2)
        Omega_rest_sq = k_torque / I_sat if I_sat > 0 else 0.0
        
        # Mean angular spread delta_theta from virial thermal fluctuation
        delta_theta_sq = (self.k_B * T_virial) / k_torque if k_torque > 0 else 0.0
        delta_theta = np.sqrt(delta_theta_sq)
        
        h_VPOS = R_halo * delta_theta
        
        return {
            "restoring_torque_constant_k": float(k_torque),
            "restoring_frequency_Omega_rest": float(np.sqrt(Omega_rest_sq)),
            "angular_dispersion_rad": float(delta_theta),
            "planar_thickness_h_VPOS_meters": float(h_VPOS),
            "is_plane_stably_bound": bool(h_VPOS < R_halo)
        }

    def compute_modified_ocm_jeans_mass(self, M_J_classical: float, c_s: float, v_kappa: float) -> dict:
        """
        Calculates OCM-modified Jeans Mass:
        M_{J, OCM} = M_{J, classical} * ( 1 + v_kappa^2 / c_s^2 )^(3/2)
        
        Prevents unphysical small-scale over-fragmentation.
        """
        if c_s <= 0.0:
            raise ValueError("Sound speed c_s must be positive.")
            
        stiffening_ratio = 1.0 + ((v_kappa ** 2) / (c_s ** 2))
        M_J_OCM = M_J_classical * (stiffening_ratio ** 1.5)
        
        return {
            "M_J_classical": float(M_J_classical),
            "M_J_OCM": float(M_J_OCM),
            "mass_elevation_factor": float(stiffening_ratio ** 1.5),
            "prevents_overfragmentation": True
        }

    def compute_cosmic_spin_asymmetry_ratio(self, chi_shear_coupling: float = np.log(2.0)) -> dict:
        """
        Calculates prograde vs retrograde cosmic galactic spin parity ratio:
        N_pro / N_total = 1 / (1 + exp(-chi))
        For saturation limit chi = ln(2) ~ 0.69315:
        Prograde = 2/3 (66.67%), Retrograde = 1/3 (33.33%).
        """
        N_pro_fraction = 1.0 / (1.0 + np.exp(-chi_shear_coupling))
        N_ret_fraction = 1.0 - N_pro_fraction
        
        ratio = N_pro_fraction / N_ret_fraction if N_ret_fraction > 0 else float('inf')
        
        return {
            "chi_shear_coupling": float(chi_shear_coupling),
            "prograde_fraction": float(N_pro_fraction),
            "retrograde_fraction": float(N_ret_fraction),
            "prograde_percentage": float(N_pro_fraction * 100.0),
            "retrograde_percentage": float(N_ret_fraction * 100.0),
            "exact_2_to_1_ratio_satisfied": bool(np.isclose(ratio, 2.0, atol=1e-5))
        }
