"""
Order Creator Mechanism (OCM) - Manifold Saturation Principle (S_M)
Implements the local scalar field computation of S_M = (D * Phi_curvature) / epsilon_M,
volumetric manifold elasticity threshold epsilon_M, non-linear stability potential Psi(S_M),
TOV limit mapping, and variational classification across sub-critical, critical, and super-critical regimes.
"""

import numpy as np

class ManifoldSaturation:
    def __init__(self, xi_elastic: float = 1.0, hbar: float = 1.054571817e-34, c: float = 299792458.0, G: float = 6.67430e-11):
        """
        Initialize fundamental physical constants and manifold elasticity parameter.
        
        :param xi_elastic: Dimensionless structural coupling constant (default xi_elastic ~ 1.0)
        """
        self.xi_elastic = xi_elastic
        self.hbar = hbar
        self.c = c
        self.G = G
        
        # Volumetric Manifold Elasticity Threshold epsilon_M (J/m^3)
        # epsilon_M = (c^7 / (G^2 * hbar)) * xi_elastic
        self.epsilon_M = ((self.c ** 7) / ((self.G ** 2) * self.hbar)) * self.xi_elastic

    def compute_manifold_elasticity(self) -> float:
        """
        Returns the volumetric energy density threshold of the 3D space fabric (epsilon_M in J/m^3).
        """
        return float(self.epsilon_M)

    def compute_local_saturation_parameter(self, mass_density_rho: float, phi_curvature: float) -> float:
        """
        Calculates local dimensionless saturation metric:
        S_M = (D * Phi_curvature) / epsilon_M
        where D = rho * c^2 (energy density).
        
        :param mass_density_rho: Mass density in kg/m^3
        :param phi_curvature: Local 3D spatial Ricci scalar / potential curvature in m^2/s^2
        """
        D = mass_density_rho * (self.c ** 2)  # Energy density J/m^3
        S_M = (D * phi_curvature) / self.epsilon_M
        return float(S_M)

    def evaluate_non_linear_potential_psi(self, S_M: float) -> float:
        """
        Evaluates the non-linear potential function Psi(S_M):
        Psi(S_M) = 0.5 * (S_M - 1.0)^2 * Theta(S_M - 1.0)
        where Theta is the Heaviside step function.
        """
        if S_M < 1.0:
            return 0.0
        return float(0.5 * ((S_M - 1.0) ** 2))

    def evaluate_supernova_snapback_energy(self, S_M_peak: float, integration_volume_m3: float) -> float:
        """
        Calculates reflected kinetic rebound wave energy E_kinetic for core-collapse supernovae:
        E_kinetic = Integral(epsilon_M * (S_M - 1) dV)
        """
        if S_M_peak <= 1.0:
            return 0.0
        
        E_kinetic = self.epsilon_M * (S_M_peak - 1.0) * integration_volume_m3
        return float(E_kinetic)

    def compute_magnetar_torsional_b_field(self, torsional_shear_tensor_sq: float) -> float:
        """
        Calculates magnetic flux density B_magnetar generated via metric torsional deformation:
        B_magnetar = sqrt(4 * pi * epsilon_M * tau_ijk * tau^ijk)
        """
        B_tesla = np.sqrt(4.0 * np.pi * self.epsilon_M * torsional_shear_tensor_sq)
        B_gauss = B_tesla * 10000.0  # Convert Tesla to Gauss
        return float(B_gauss)

    def classify_astrophysical_state(self, S_M: float, angular_velocity_omega: float = 0.0, is_binary_merger: bool = False) -> dict:
        """
        Classifies compact objects based on S_M regime, rotational shear, and topological changing boundary conditions.
        """
        psi_val = self.evaluate_non_linear_potential_psi(S_M)
        
        if S_M < 1.0:
            regime = "Sub-Critical (Static Retention)"
            topology = "Standard 3D Metric Continuity (R^3)"
            object_type = "White Dwarf" if S_M < 0.3 else "Stable Low-Mass Neutron Star"
        elif np.isclose(S_M, 1.0, atol=0.05):
            regime = "Critical & Torsional Crisis (Structural Failure)"
            topology = "Boundary Saturation Limit (TOV Equivalence)"
            if angular_velocity_omega > 1000.0:
                object_type = "Magnetar (Torsional Knotting B ~ 10^15 G)"
            elif angular_velocity_omega > 0.0:
                object_type = "Pulsar (Topological Friction Spin-Down)"
            else:
                object_type = "Type II Supernova Snap-Back Rebound"
        else:  # S_M > 1.0
            regime = "Super-Critical (Topological Ignition)"
            topology = "Punctured Metric (R^3 -> R^3 x S^1 / Z_2 Bridge)"
            if is_binary_merger:
                object_type = "Binary Merger Topological Splicing (Kilonova r-process)"
            elif angular_velocity_omega > 2000.0:
                object_type = "Hyper-Critical Ignition (Collimated GRB Outflow)"
            else:
                object_type = "Active OCM Primary Node / Primordial High-z Seed"
                
        return {
            "S_M_value": float(S_M),
            "regime": regime,
            "topology": topology,
            "object_classification": object_type,
            "Psi_potential_value": float(psi_val),
            "has_4D_bridge_ignited": bool(S_M >= 1.0)
        }
