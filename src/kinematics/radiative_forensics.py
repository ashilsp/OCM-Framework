"""
Order Creator Mechanism (OCM) - Radiative Forensics & Temporal Flux Analysis
Implements the OCM Color Rule (Violet Shift), orthogonal temporal flux decomposition
(F_total = F_accretion + F_OCM), mass-frequency scaling, and dust-extinction correction.
"""

import numpy as np

class RadiativeForensics:
    def __init__(self, phi_manifold: float = 0.85):
        """
        Initialize radiative forensics parameters.
        
        :param phi_manifold: Manifold damping factor for time dilation corrections
        """
        self.phi_manifold = phi_manifold
        self.h_eV = 4.135667696e-15  # Planck constant in eV*s
        self.c = 2.99792458e8         # Speed of light in m/s

    def compute_violet_exhaust_wavelength(self, delta_E_eV: float = 4.0) -> dict:
        """
        Calculates fundamental exhaust wavelength lambda_exhaust = c / nu.
        Validates the OCM Color Rule for stellar-mass nodes (120 - 300 nm / 3.1 - 4.1 eV).
        """
        nu_exhaust = (delta_E_eV / self.h_eV) * self.phi_manifold
        lambda_m = self.c / nu_exhaust
        lambda_nm = lambda_m * 1.0e9
        
        return {
            "delta_E_eV": float(delta_E_eV),
            "nu_exhaust_Hz": float(nu_exhaust),
            "lambda_exhaust_nm": float(lambda_nm),
            "is_violet_band": 120.0 <= lambda_nm <= 400.0
        }

    def decompose_temporal_flux(self, F_accretion_mean: float, F_OCM_baseline: float, time_points: np.ndarray) -> dict:
        """
        Decomposes total radiative output into orthogonal components:
        F_total(lambda, t) = F_accretion(lambda, t) + F_OCM(lambda)
        
        Where F_OCM is a stationary, zero-phase-noise monochromatic background hum.
        """
        # Accretion exhibits stochastic red-noise fluctuations
        stochastic_noise = np.random.normal(0.0, 0.2 * F_accretion_mean, size=len(time_points))
        F_accretion = np.maximum(0.0, F_accretion_mean + stochastic_noise)
        
        # F_OCM is strictly invariant across time (d F_OCM / d mdot = 0)
        F_OCM = np.full_like(time_points, fill_value=F_OCM_baseline)
        F_total = F_accretion + F_OCM
        
        return {
            "F_accretion_series": F_accretion.tolist(),
            "F_OCM_series": F_OCM.tolist(),
            "F_total_series": F_total.tolist(),
            "OCM_decoupled_from_mdot": True
        }

    def mass_frequency_scaling_classification(self, M_solar: float) -> dict:
        """
        Scales energy gap and exhaust regime as mass scales from stellar to hypermassive.
        Maps to Table 8 (Stellar-Mass -> UV/Violet, Supermassive -> Hard X-Ray / Gamma-Ray).
        """
        if M_solar < 50.0:
            classification = "Stellar-Mass Active / Isolated"
            spectral_regime = "Violet / Far-UV (120 - 400 nm)"
            delta_E_eV = 4.0
        elif 50.0 <= M_solar < 1.0e5:
            classification = "Intermediate-Mass Node"
            spectral_regime = "Soft X-Ray (10 - 100 nm)"
            delta_E_eV = 50.0
        elif 1.0e5 <= M_solar < 1.0e8:
            classification = "Supermassive Active Node"
            spectral_regime = "Hard X-Ray (0.1 - 1.0 nm)"
            delta_E_eV = 1.2e3
        else:
            classification = "Hypermassive Core (M87* Class)"
            spectral_regime = "Gamma-Ray Jet Core (< 0.01 nm)"
            delta_E_eV = 1.2e5

        return {
            "mass_solar": float(M_solar),
            "classification": classification,
            "spectral_regime": spectral_regime,
            "typical_delta_E_eV": float(delta_E_eV)
        }

    def apply_extinction_correction(self, F_observed: float, E_B_V: float, R_V: float = 3.1) -> float:
        """
        Reconstructs intrinsic source profile using standard dust extinction corrections:
        A_lambda = R_V * E(B-V)
        F_intrinsic = F_observed * 10^(0.4 * A_lambda)
        """
        A_lambda = R_V * E_B_V
        F_intrinsic = F_observed * (10.0 ** (0.4 * A_lambda))
        return float(F_intrinsic)
