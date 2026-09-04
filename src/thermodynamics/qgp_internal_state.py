"""
Order Creator Mechanism (OCM) - QGP Internal State & Luminosity Floor
Implements Wien's displacement law vs. Topological Hardening at the R_d boundary,
and calculates the total observable luminosity including the invariant OCM floor (Lambda_OCM).
"""

import numpy as np

class QGPInternalState:
    def __init__(self, lambda_ocm_floor: float = 1.0e23):
        """
        Initialize the thermodynamic metabolic parameters.
        
        :param lambda_ocm_floor: Baseline invariant OCM luminosity floor Lambda_OCM (in Watts, ~1.0e30 erg/s)
        """
        self.lambda_ocm = lambda_ocm_floor
        self.wien_b = 2.8977719e-3  # Wien's displacement constant in m*K
        self.c = 2.99792e8

    def compute_wien_vs_topological_hardening(self, temperature_K: float, kappa_flux_density: float) -> dict:
        """
        Calculates peak blackbody emission wavelength via Wien's Law and compares
        it against the non-thermal Topological Hardening shift forced by kappa-flux.
        
        :param temperature_K: QGP thermal temperature at R_d (Kelvin)
        :param kappa_flux_density: Localized kappa-flux density
        :return: Dictionary containing thermal and topologically hardened wavelengths
        """
        if temperature_K <= 0:
            raise ValueError("Temperature must be greater than absolute zero.")
            
        lambda_thermal = self.wien_b / temperature_K
        
        # Non-thermal hardening decouples from pure temperature via kappa-flux
        hardening_factor = 1.0 + np.log10(1.0 + kappa_flux_density)
        lambda_hardened = lambda_thermal / hardening_factor
        
        return {
            "thermal_peak_lambda_m": float(lambda_thermal),
            "topologically_hardened_lambda_m": float(lambda_hardened),
            "spectral_regime": "Violet / UV-Hardened Non-Thermal"
        }

    def compute_observable_luminosity(self, mdot_kg_per_sec: float, radiative_efficiency: float = 0.1) -> dict:
        """
        Calculates total observable luminosity:
        L_obs = eta * mdot * c^2 + Lambda_OCM
        
        Resolves JWST Little Red Dots (LRDs) and enforces the 'White-ish Hole' plateau as mdot -> 0.
        
        :param mdot_kg_per_sec: Accretion mass inflow rate (kg/s)
        :param radiative_efficiency: Standard accretion efficiency eta
        :return: Dictionary containing accretion luminosity, baseline floor, and total L_obs
        """
        l_accretion = radiative_efficiency * mdot_kg_per_sec * (self.c ** 2)
        l_obs = l_accretion + self.lambda_ocm
        
        is_whiteish_hole_regime = l_accretion < self.lambda_ocm
        
        return {
            "L_accretion_Watts": float(l_accretion),
            "Lambda_OCM_floor_Watts": float(self.lambda_ocm),
            "L_total_obs_Watts": float(l_obs),
            "is_whiteish_hole_regime": is_whiteish_hole_regime,
            "status": "White-ish Hole Stability Plateau Active" if is_whiteish_hole_regime else "Accretion Dominated"
        }
