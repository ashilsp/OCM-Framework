"""
Order Creator Mechanism (OCM) - Macro-Topology of the Cosmic Web & Global Shear Field
Implements Modified Jeans Stability with Manifold Viscosity (eta_M), Topological Torque (T_M),
Global Ignition Energy Gap (prograde vs retrograde), Filament Proximity Spin Scaling (80/20 to 50/50),
and CMB Quadrupole-Octopole (l=2, l=3) Axis Alignment.
"""

import numpy as np

class MacroTopologyShear:
    def __init__(self, eta_M: float = 1.0e-11, beta_coupling: float = 0.15, delta_E0: float = 1.0e45):
        """
        Initialize macro-topology shear and stability parameters.
        
        :param eta_M: Dynamic manifold viscosity coefficient
        :param beta_coupling: Structural coupling constant to the global 4D bulk spin vector
        :param delta_E0: Baseline ignition energy threshold for an active OCM node (Joules)
        """
        self.eta_M = eta_M
        self.beta_coupling = beta_coupling
        self.delta_E0 = delta_E0
        self.G = 6.67430e-11  # m^3 kg^-1 s^-2

    def evaluate_modified_jeans_balance(self, grad_P_gas: float, rho: float, grad_Phi_grav: float, 
                                       laplacian_v: float, grad_Psi_0: float) -> dict:
        """
        Evaluates the modified Jeans thermodynamic equilibrium equation:
        grad(P_gas) + rho * grad(Phi_grav) + eta_M * laplacian(v) = F_kappa
        where F_kappa = C * grad(Psi_0).
        
        Demonstrates how manifold viscosity pins stars along structural folds, preventing collapse/dissipation.
        """
        lhs_hydro_grav = grad_P_gas + (rho * grad_Phi_grav)
        viscous_stiffening = self.eta_M * laplacian_v
        
        # F_kappa provides the conservative topological restoring force
        F_kappa_required = lhs_hydro_grav + viscous_stiffening
        
        return {
            "lhs_hydro_grav_N_m3": float(lhs_hydro_grav),
            "viscous_stiffening_N_m3": float(viscous_stiffening),
            "F_kappa_restoring_force_N_m3": float(F_kappa_required),
            "is_topologically_stabilized": bool(abs(viscous_stiffening) > 0.0)
        }

    def compute_topological_torque(self, curl_psi_kappa: np.ndarray, area_vector: np.ndarray) -> np.ndarray:
        """
        Calculates the Topological Torque T_M exerted by the kappa-helicity at the Rd interface:
        T_M = eta_M * Integral_Rd ( (curl(Psi_kappa)) . dA )
        
        Acts as a macroscopic topological stirrer that imparts intrinsic spin chirality.
        """
        helicity_flux = np.dot(curl_psi_kappa, area_vector)
        torque_vector = self.eta_M * helicity_flux * area_vector
        return torque_vector

    def calculate_node_ignition_energy(self, omega_node: np.ndarray, S_global: np.ndarray) -> dict:
        """
        Calculates energy gap delta_E_ign = delta_E0 - beta * (omega_node . S_global).
        Prograde nodes (aligned with S_global) achieve ignition at lower entropy thresholds than retrograde nodes.
        """
        alignment_dot = np.dot(omega_node, S_global)
        delta_E_ign = self.delta_E0 - (self.beta_coupling * alignment_dot * self.delta_E0)
        
        is_prograde = alignment_dot > 0.0
        return {
            "alignment_dot_product": float(alignment_dot),
            "is_prograde": bool(is_prograde),
            "ignition_energy_J": float(delta_E_ign),
            "thermodynamic_advantage": "Lower threshold (Prograde)" if is_prograde else "Higher friction barrier (Retrograde)"
        }

    def compute_spin_asymmetry_by_filament_proximity(self, d_filament_mpc: float, d_char_mpc: float = 5.0) -> dict:
        """
        Calculates galactic spin-preference ratio based on proximity to high-tension cosmic filaments:
        Prograde fraction scales from ~80% (0.80) at filament cores (d=0) to ~50% (0.50) in deep voids (d >> d_char).
        """
        # Exponential transition from 0.80 at d=0 to 0.50 at large distances
        prograde_fraction = 0.50 + 0.30 * np.exp(-d_filament_mpc / d_char_mpc)
        retrograde_fraction = 1.0 - prograde_fraction
        
        return {
            "d_filament_mpc": float(d_filament_mpc),
            "prograde_ratio": float(prograde_fraction),
            "retrograde_ratio": float(retrograde_fraction),
            "spin_distribution_type": "Filament Core (80/20 regime)" if prograde_fraction > 0.70 else "Cosmic Void (50/50 isotropic limit)"
        }

    def evaluate_cmb_multipole_axis_alignment(self, quad_vector_l2: np.ndarray, oct_vector_l3: np.ndarray) -> dict:
        """
        Evaluates alignment between CMB quadrupole (l=2) and octopole (l=3) vectors along the Axis of Evil.
        Alignment indicates direct physical imprint of the global 4D manifold grain (S_global).
        """
        norm_l2 = quad_vector_l2 / np.linalg.norm(quad_vector_l2)
        norm_l3 = oct_vector_l3 / np.linalg.norm(oct_vector_l3)
        
        alignment_cosine = np.dot(norm_l2, norm_l3)
        alignment_angle_deg = np.degrees(np.arccos(np.clip(alignment_cosine, -1.0, 1.0)))
        
        return {
            "alignment_cosine": float(alignment_cosine),
            "alignment_angle_degrees": float(alignment_angle_deg),
            "is_axis_of_evil_aligned": bool(abs(alignment_cosine) > 0.90),
            "cosmological_implication": "Steady-state signature of primordial 4D manifold grain"
        }
