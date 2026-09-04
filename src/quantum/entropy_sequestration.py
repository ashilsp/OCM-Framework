"""
Order Creator Mechanism (OCM) - Non-Singularity & Entropy Sequestration
Implements dimensional entropy compression (3D to 2D), the 4D mass flux conduit (Phi_mass),
and the Gravitational Hydrogen Atom potential with the Quantum Spring barrier.
"""

import numpy as np

class EntropySequestration:
    def __init__(self, R_d: float, Lambda_OCM: float = 1.0e-2, C_kappa: float = 1.0e-3):
        """
        Initialize topological sequestration parameters.
        
        :param R_d: Disruption radius boundary (meters)
        :param Lambda_OCM: Manifold repulsion coefficient
        :param C_kappa: Order Creator Flux (kappa) strength constant
        """
        self.R_d = R_d
        self.Lambda_OCM = Lambda_OCM
        self.C_kappa = C_kappa
        self.G = 6.67430e-11  # m^3 kg^-1 s^-2

    def compress_entropy(self, S_3D: float, efficiency: float = 0.95) -> dict:
        """
        Calculates 3D to 2D laminar entropy transition at R_d:
        S_3D -> S_2D(Laminar) + Delta E
        """
        S_2D = S_3D * (1.0 - efficiency)
        delta_E = S_3D * efficiency  # Rejected kinetic energy / exhaust
        
        return {
            "S_2D_laminar": S_2D,
            "delta_E_exhaust": delta_E,
            "information_preserved": True
        }

    def compute_4d_conduit_flux(self, viscosity_eta_M: float, grad_psi_4D: float, area_R_d: float) -> float:
        """
        Calculates mass-energy flux into the 4D conduit:
        Phi_mass = Surface_Integral(eta_M * grad(Psi_4D) dA)
        Mitigates 3D gravitational pressure without singular collapse.
        """
        phi_mass = viscosity_eta_M * grad_psi_4D * area_R_d
        return float(phi_mass)

    def gravitational_hydrogen_potential(self, r: float, mass_M: float, n_exponent: int = 2) -> float:
        """
        Evaluates V_top(r) = -GM/r + Lambda_OCM / (r - R_d)^n.
        Forms the Quantum Spring infinite barrier as r -> R_d from above.
        """
        if r <= self.R_d:
            return float('inf')  # Impenetrable Quantum Spring wall at R_d
            
        V_grav = -(self.G * mass_M) / r
        V_repulsion = self.Lambda_OCM / ((r - self.R_d) ** n_exponent)
        
        return V_grav + V_repulsion
