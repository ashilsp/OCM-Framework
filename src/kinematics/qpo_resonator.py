"""
Order Creator Mechanism (OCM) - QPO Resonator & Nodal Vibration
Implements the 3:2 twin-peak resonance (Poloidal/Toroidal modes), parameter-free
mass-frequency scaling, and the quiescent "Ghost Pulse" topological hum prediction.
"""

import numpy as np

class QPOResonator:
    def __init__(self, manifold_tension_sigma: float = 1.0, manifold_density_rho: float = 1.0):
        """
        Initialize the nodal resonant cavity parameters.
        
        :param manifold_tension_sigma: Dimensionless manifold tension \sigma_M
        :param manifold_density_rho: Dimensionless \kappa-flux density \rho_manifold
        """
        self.sigma_M = manifold_tension_sigma
        self.rho_manifold = manifold_density_rho
        self.base_frequency_scale = 1.13e3  # Base constant in Hz for M = 1 M_sun

    def compute_twin_peak_frequencies(self, M_solar: float) -> dict:
        """
        Calculates parameter-free upper (Poloidal) and lower (Toroidal) QPO frequencies
        enforced by the 3:2 integer eigenvalue ratio of the Oloid interface:
        
        f_P = 3 * (1.13e3 Hz / (M / M_sun))
        f_T = 2 * (1.13e3 Hz / (M / M_sun))
        
        :param M_solar: Mass of the node in solar masses (M / M_sun)
        :return: Dictionary containing poloidal and toroidal frequencies in Hz
        """
        if M_solar <= 0:
            raise ValueError("Node mass must be strictly positive.")
            
        tension_factor = np.sqrt(self.sigma_M / self.rho_manifold)
        f_fundamental = (self.base_frequency_scale / M_solar) * tension_factor
        
        f_poloidal = 3.0 * f_fundamental
        f_toroidal = 2.0 * f_fundamental
        ratio = f_poloidal / f_toroidal
        
        return {
            "f_poloidal_upper_Hz": float(f_poloidal),
            "f_toroidal_lower_Hz": float(f_toroidal),
            "mode_ratio": float(ratio),
            "coupling_ratio_str": "3:2"
        }

    def evaluate_ghost_pulse(self, M_solar: float, accretion_rate_mdot: float) -> dict:
        """
        Predicts the persistent 'Ghost Pulse' topological hum during quiescence (mdot -> 0).
        Unlike accretion disk models, the R_d shell continues vibrating at ground state.
        
        :param M_solar: Node mass in solar masses
        :param accretion_rate_mdot: Accretion rate (0.0 = total quiescence)
        :return: Dictionary containing ghost pulse frequency and state status
        """
        freqs = self.compute_twin_peak_frequencies(M_solar)
        
        # Ground state hum persists regardless of accretion rate
        is_active_hum = True
        amplitude = 0.05 if accretion_rate_mdot == 0.0 else (0.05 + 0.95 * accretion_rate_mdot)
        
        return {
            "persistent_hum_frequency_Hz": freqs["f_poloidal_upper_Hz"],
            "relative_amplitude": float(amplitude),
            "is_quiescent_ghost_pulse": accretion_rate_mdot == 0.0,
            "status": "Ground-State Topological Clock Active"
        }
