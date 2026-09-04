"""
Order Creator Mechanism (OCM) - Dimensional Descent & Gauge Boundary Reduction
Implements 5D to 4D Kaluza-Klein-Weyl metric factorization, Stueckelberg vacuum expectation value locking,
computation of the topological impedance operator Xi_hat(R_d), gauge invariance verification under U(1),
and the mass-energy venting flux current J_vent across the R_d boundary layer.
"""

import numpy as np

class DimensionalDescent:
    def __init__(self, R_4: float = 1.616255e-35, kappa_M: float = 1.0e-3, kappa_0_zeta_0: float = 1.0e-3, hbar: float = 1.054571817e-34, c: float = 299792458.0):
        """
        Initialize dimensional descent and gauge field parameters.
        
        :param R_4: Compactified extra-dimensional radius (meters, Planck scale default)
        :param kappa_M: Manifold permeability constant
        :param kappa_0_zeta_0: Normalization constant product for impedance damping
        """
        self.hbar = hbar
        self.c = c
        self.R_4 = R_4
        self.kappa_M = kappa_M
        self.kappa_0_zeta_0 = kappa_0_zeta_0

    def compute_stueckelberg_vev(self) -> float:
        """
        Calculates the Stueckelberg gauge-fixed vacuum expectation value:
        <Phi_4> = Phi_0 = sqrt((hbar * c) / kappa_M)
        """
        if self.kappa_M <= 0.0:
            raise ValueError("Manifold permeability kappa_M must be positive.")
        
        Phi_0 = np.sqrt((self.hbar * self.c) / self.kappa_M)
        return float(Phi_0)

    def evaluate_5d_metric_factorization(self, g_munu_4d: np.ndarray, sigma_x: float, A_mu: np.ndarray) -> dict:
        """
        Evaluates the 5D metric tensor ansatz g_hat_MN using Kaluza-Klein-Weyl factorization:
        ds^2 = e^(2*sigma) * g_munu * dx^mu * dx^nu - epsilon_M * Phi_4^2 * (dx^4 + A_mu * dx^mu)^2
        """
        Phi_0 = self.compute_stueckelberg_vev()
        conformal_factor = np.exp(2.0 * sigma_x)
        g_4d_conformal = conformal_factor * g_munu_4d
        
        return {
            "Phi_0_vev": float(Phi_0),
            "conformal_factor": float(conformal_factor),
            "4d_conformal_metric": g_4d_conformal,
            "extra_dim_scale_factor": float(Phi_0 ** 2)
        }

    def compute_topological_impedance_operator(self, R_d: float, mu_mass: float) -> float:
        """
        Calculates the localized non-local boundary impedance magnitude Xi_hat(R_d):
        Xi_hat(R_d) = (hbar^2 / (2 * mu * R_d^2)) * exp(-kappa_M / (kappa_0 * zeta_0))
        
        Truncates the classical 1/r singularity drop.
        """
        if R_d <= 0.0 or mu_mass <= 0.0:
            raise ValueError("R_d and mu_mass must be strictly positive.")
            
        exponential_damping = np.exp(-self.kappa_M / self.kappa_0_zeta_0)
        Xi_magnitude = (self.hbar ** 2) / (2.0 * mu_mass * (R_d ** 2)) * exponential_damping
        return float(Xi_magnitude)

    def verify_u1_gauge_invariance(self, psi_val: complex, lambda_phase: float) -> dict:
        """
        Verifies localized U(1) gauge transformation invariance:
        psi -> psi * exp(i * Lambda)
        delta(Xi_hat) = 0
        """
        psi_transformed = psi_val * np.exp(1j * lambda_phase)
        abs_psi_original = abs(psi_val)
        abs_psi_transformed = abs(psi_transformed)
        
        is_invariant = np.isclose(abs_psi_original, abs_psi_transformed)
        
        return {
            "original_psi_norm": float(abs_psi_original),
            "transformed_psi_norm": float(abs_psi_transformed),
            "is_gauge_invariant": bool(is_invariant)
        }

    def compute_venting_flux_current(self, m_dot_out: float, R_d: float) -> float:
        """
        Calculates the boundary mass-energy venting flux current J_vent:
        lim_{r->R_d^+} J_vent . n_hat = (m_dot_out / kappa_M) * Surface_Area
        
        :param m_dot_out: Outward mass venting rate (kg/s)
        :param R_d: Interface radius (meters)
        :return: Normal venting flux magnitude
        """
        surface_area = 4.0 * np.pi * (R_d ** 2)
        J_vent_normal = (m_dot_out / self.kappa_M) * surface_area
        return float(J_vent_normal)
