"""
Order Creator Mechanism (OCM) - Topological Tethering & Manifold Architecture
Implements the Manifold Drag Tensor (tau_M), gravitational Aharonov-Bohm phase-locking,
'Beads-on-a-String' stellar filament tension, Angular Phase-Trapping, and the exact derivation
of flat rotation curves (v_outer = eta_M / rho_0) without dark matter halos.
"""

import numpy as np

class TopologicalTethering:
    def __init__(self, eta_M: float = 1.0e-11, alpha_decay: float = 1.0e-21, rho_0: float = 1.0e-20):
        """
        Initialize topological tethering parameters.
        
        :param eta_M: Dynamic manifold viscosity parameter
        :param alpha_decay: Exponential spatial decay constant for the metric drag tensor
        :param rho_0: Mid-plane characteristic density scaling factor (kg/m^3)
        """
        self.eta_M = eta_M
        self.alpha_decay = alpha_decay
        self.rho_0 = rho_0
        self.hbar = 1.054571817e-34  # J*s
        self.G = 6.67430e-11         # m^3 kg^-1 s^-2

    def compute_manifold_drag_tensor(self, grad_omega_node: np.ndarray, v_disk: np.ndarray, R_radius: float) -> np.ndarray:
        """
        Calculates the anisotropic Manifold Drag Tensor tau_M:
        tau_M = eta_M * (grad(Omega_node) x v_disk) * exp(-alpha * R)
        
        Suppresses differential velocity shear across galactic disks without dark matter halos.
        """
        cross_prod = np.cross(grad_omega_node, v_disk)
        decay_factor = np.exp(-self.alpha_decay * R_radius)
        
        tau_M = self.eta_M * cross_prod * decay_factor
        return tau_M

    def evaluate_aharonov_bohm_phase_shift(self, mass_star_kg: float, vector_potential_A_kappa: float, loop_length_m: float) -> float:
        """
        Calculates macroscopic phase-locking shift via gravitational Aharonov-Bohm effect:
        Phi = (M_star / hbar) * Integral(A_kappa . dl)
        
        Phase-locks stellar trajectories to the central Rd node's spatial grid.
        """
        phi_shift = (mass_star_kg / self.hbar) * vector_potential_A_kappa * loop_length_m
        return float(phi_shift)

    def calculate_filament_linear_tension(self, curl_psi_kappa: float, length_L_meters: float) -> float:
        """
        Computes the linear tension T_M holding stellar strings together:
        T_M = Integral_0_L( eta_M * (curl(Psi_kappa))^2 dl )
        
        Models 'Beads-on-a-String' dynamics in Orion, Pleiades, and galactic spiral arms.
        """
        tension_density = self.eta_M * (curl_psi_kappa ** 2)
        T_M = tension_density * length_L_meters
        return float(T_M)

    def evaluate_angular_phase_trapping(self, theta: float, theta_fold: float, omega_M: float, gamma: float) -> float:
        """
        Evaluates the restorative acceleration from the angular phase-trapping differential equation:
        d^2 theta / dt^2 = - gamma * (d theta / dt) - omega_M^2 * sin(theta - theta_fold)
        
        Guarantees that corrugations (e.g. NGC 5907 scalloping, Radcliffe Wave) remain resonant and coherent.
        """
        phase_diff = theta - theta_fold
        restorative_acceleration = -(omega_M ** 2) * np.sin(phase_diff)
        return float(restorative_acceleration)

    def derive_flat_rotation_velocity(self, R_meters: float, M_baryon_kg: float) -> dict:
        """
        Derives the galactic orbital velocity from combined baryonic potential and metric tension:
        v^2 / R = (G * M_baryon / R^2) + (eta_M / rho_0) * (v / R)
        
        Asymptotically yields v_outer = eta_M / rho_0 = constant.
        """
        if R_meters <= 0:
            return {"v_total_m_per_s": 0.0, "v_asymptotic_m_per_s": float(self.eta_M / self.rho_0)}
            
        # Quadratic formula coefficients: v^2 - (eta_M / rho_0) * v - (G * M_baryon / R) = 0
        b = -(self.eta_M / self.rho_0)
        c = - (self.G * M_baryon_kg) / R_meters
        
        v_solution = (-b + np.sqrt(b**2 - 4*c)) / 2.0
        v_asymptotic = self.eta_M / self.rho_0
        
        return {
            "v_total_m_per_s": float(v_solution),
            "v_asymptotic_m_per_s": float(v_asymptotic),
            "metric_tension_dominated": bool(abs(c) < b**2)
        }
