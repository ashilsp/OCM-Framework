"""
Order Creator Mechanism (OCM) - Quantum Foundation & OCM Hamiltonian
Implements the piecewise saturation potential V_top(r), quantized exhaust frequency,
and discrete quantum shell jumps (R_n) explaining empirical mass gaps.
"""

import numpy as np

class OCMHamiltonian:
    def __init__(self, M_solar: float, R_d: float, E_0: float = -1.0e52):
        """
        Initialize OCM Hamiltonian parameters for a compact node.
        
        :param M_solar: Mass of the compact object in solar masses (M_sun)
        :param R_d: Disruption boundary radius (meters)
        :param E_0: Saturation potential floor energy (Joules)
        """
        self.M_solar = M_solar
        self.M_kg = M_solar * 1.989e30
        self.R_d = R_d
        self.E_0 = E_0
        
        # Physical constants
        self.G = 6.67430e-11   # m^3 kg^-1 s^-2
        self.c = 2.99792e8     # m/s
        self.h = 6.62607e-34    # J*s

    def evaluate_topological_potential(self, r: float) -> float:
        """
        Calculates the piecewise topological potential V_top(r).
        Eliminates singular divergence by flattening to saturation floor E_0 at r <= R_d.
        """
        if r > self.R_d:
            return -(self.G * self.M_kg) / r
        else:
            return self.E_0

    def compute_exhaust_frequency(self, R_star: float, damping_omega: float = 1.0) -> float:
        """
        Calculates quantized exhaust frequency nu_exhaust from energy differential Delta E.
        Predicts Near-UV/Violet for stellar-mass nodes and Hard X-ray for supermassive nodes.
        """
        if R_star <= self.R_d:
            return 0.0
            
        delta_E = self.M_kg * (self.c ** 2) * (1.0 - np.sqrt(1.0 - (self.R_d / R_star)))
        curvature_term = np.sqrt((self.c ** 3) / (self.G * self.M_kg * damping_omega))
        
        nu_exhaust = (delta_E / self.h) * curvature_term
        return float(nu_exhaust)

    def calculate_quantized_shell_radius(self, n: int, M_min_solar: float = 2.5) -> float:
        """
        Calculates discrete shell expansions R_n = n^2 * (G * M_min / c^2).
        Provides geometric origin for lower mass gap (2.5 - 5 M_sun) and 
        pair-instability gap accommodation (e.g., GW190521).
        """
        M_min_kg = M_min_solar * 1.989e30
        R_1 = (self.G * M_min_kg) / (self.c ** 2)
        return float((n ** 2) * R_1)
