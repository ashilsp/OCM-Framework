"""
Order Creator Mechanism (OCM) - Topological Failure Modes & Manifold Torsion
Simulates supernova snap-back energy and magnetar torsional crisis mechanics.
"""

import numpy as np

class ManifoldFailureDynamics:
    def __init__(self, manifold_tension_coefficient: float = 1.25e22):
        """
        Initialize manifold mechanical properties.
        :param manifold_tension_coefficient: Baseline spatial tension parameter
        """
        self.k_tension = manifold_tension_coefficient

    def calculate_snapback_energy(self, angular_turbulence: float, entropy_density: float) -> float:
        """
        Calculates kinetic energy reflected into 3D during a supernova (Manifold Rejection).
        Higher turbulence prevents laminar oloid boundary formation, leading to snap-back.
        
        :param angular_turbulence: Dimensionless non-laminar noise factor (0 = smooth, >1 = turbulent)
        :param entropy_density: Core entropic energy prior to collapse (Joules)
        :return: Reflected kinetic energy (Joules)
        """
        if angular_turbulence > 0.5:
            # Rejection regime: Manifold snaps back like an over-stretched elastic sheet
            rebound_efficiency = min(1.0, angular_turbulence * 0.85)
            return entropy_density * rebound_efficiency
        return 0.0

    def compute_torsional_magnetic_field(self, angular_momentum_J: float, saturation_S_M: float) -> float:
        """
        Calculates the effective 3D magnetic field strength B from Manifold Torsion (tau).
        B \propto \tau (Magnetar Crisis).
        
        :param angular_momentum_J: Angular momentum of the core
        :param saturation_S_M: Saturation parameter (S_M ~ 1)
        :return: Magnetic field strength B in Tesla
        """
        # Torsional knotting occurs when S_M ~ 1 under asymmetric spin
        torsion_tau = angular_momentum_J * np.abs(1.0 - saturation_S_M)
        
        # Proportional projection from 4D manifold strain into 3D B-field
        magnetic_field_B = self.k_tension * torsion_tau
        return magnetic_field_B
