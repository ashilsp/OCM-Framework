"""
Order Creator Mechanism (OCM) - Quantum-Geometric Regulation
Implements the kappa-Hamiltonian, topological repulsion potential V_top(r),
ground state wavefunction Psi_0(r), and exhaust energy transitions at R_d.
"""

import numpy as np

class KappaHamiltonian:
    def __init__(self, R_d: float, C_kappa: float = 1.0e-3, mass: float = 1.0):
        """
        Initialize the quantum boundary parameters for the R_d interface.
        
        :param R_d: Disruption radius boundary
        :param C_kappa: Repulsion strength constant for the kappa flux
        :param mass: Mass M of the compact object
        """
        self.R_d = R_d
        self.C_kappa = C_kappa
        self.M = mass
        self.G = 1.0  # Normalized gravitational constant
        self.hbar = 1.0

    def topological_potential(self, r: float, n: int = 2) -> float:
        """
        Calculates V_top(r) = V_grav(r) + V_kappa(r).
        Exhibits an impenetrable Quantum Wall as r -> R_d from above.
        """
        if r <= self.R_d:
            return float('inf')  # Infinite barrier wall inside R_d
        
        V_grav = -(self.G * self.M) / r
        V_kappa = self.C_kappa / ((r - self.R_d) ** n)
        return V_grav + V_kappa

    def ground_state_wavefunction(self, r: float, alpha: float = 1.5) -> float:
        """
        Evaluates the ground state Gaussian wavefunction Psi_0(r) localized at the R_d shell:
        Psi_0(r) ~ exp[-alpha * (r - R_d)^2]
        """
        if r < self.R_d:
            return 0.0
        return float(np.exp(-alpha * ((r - self.R_d) ** 2)))

    def compute_radiative_exhaust(self, E_chaos: float, E_0: float = 1.0) -> dict:
        """
        Calculates the energy gap Delta E = E_chaos - E_0 and determines
        the resulting Bremsstrahlung exhaust regime.
        """
        delta_E = max(0.0, E_chaos - E_0)
        
        # Determine operational regime based on mass scale curvature
        if self.M > 1.0e6:
            spectral_peak = "Hard X-ray (10 keV - 100 keV)"
        else:
            spectral_peak = "Violet / Extreme-UV (120 nm - 300 nm)"

        return {
            "energy_gap_delta_E": delta_E,
            "spectral_peak": spectral_peak,
            "information_preserved": True
        }
