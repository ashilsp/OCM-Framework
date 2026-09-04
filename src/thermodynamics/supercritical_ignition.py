"""
Order Creator Mechanism (OCM) - Super-Critical Ignitions & Primordial Nodes
Models ground-state E_0 topological transitions, GRB polar jet collimation,
and early-universe direct-collapse seed node formation (JWST z > 10 anomaly).
"""

import numpy as np

class SuperCriticalIgnition:
    def __init__(self, ground_state_energy_E0: float = 1.0e44):
        """
        Initialize the ground state energy capacity.
        :param ground_state_energy_E0: Base energy scale of the E_0 ground state (Joules)
        """
        self.E0 = ground_state_energy_E0

    def compute_latent_phase_exhaust(self, S_M: float) -> dict:
        """
        Calculates the latent phase release energy during transition to the 4D bridge.
        
        :param S_M: Manifold Saturation Index (S_M > 1 for ignition)
        :return: Dictionary containing latent exhaust energy and spectral regime
        """
        if S_M <= 1.0:
            return {"latent_energy": 0.0, "regime": "Sub-critical (No Puncture)"}
        
        # Energy release scales with degree of super-criticality
        latent_energy = self.E0 * (S_M - 1.0)
        
        if S_M < 2.0:
            regime = "Violet Shift (Standard OCM Birth Cry)"
        elif 2.0 <= S_M < 5.0:
            regime = "Kilonova Splicing (Heavy Element Ejection)"
        else:
            regime = "Gamma-Ray Burst (Super-Critical Hypernova)"
            
        return {"latent_energy": latent_energy, "regime": regime}

    def compute_grb_jet_collimation(self, S_M: float, angular_momentum_J: float) -> float:
        """
        Calculates the opening half-angle (theta) of polar exhaust jets in hyper-critical regimes.
        Extreme centrifugal tension (high J) forces kappa-flux into collimated polar channels.
        
        :param S_M: Saturation index (S_M >> 1)
        :param angular_momentum_J: Dimensionless angular momentum (spin) parameter
        :return: Jet opening angle in degrees (smaller angle = tighter collimation)
        """
        if S_M > 1.0 and angular_momentum_J > 0.8:
            # High spin + high S_M tightens the jet angle
            collimation_factor = 1.0 / (S_M * angular_momentum_J)
            opening_angle_deg = np.rad2deg(np.arcsin(min(1.0, collimation_factor)))
            return float(opening_angle_deg)
        return 90.0  # Isotropic emission for low spin / standard ignition

    def primordial_seed_growth(self, S_M_primordial: float, redshift_z: float) -> float:
        """
        Evaluates immediate direct-collapse supermassive node formation at z > 10.
        Bypasses standard accretion limits via instant super-critical 4D bridge ignition.
        
        :param S_M_primordial: High-density fluctuations in early universe
        :param redshift_z: Cosmological redshift (e.g., z > 10)
        :return: Seed mass multiplier relative to solar mass
        """
        if S_M_primordial > 1.0 and redshift_z >= 10.0:
            # Direct topological puncture yields immediate 10^6 - 10^9 solar mass nodes
            base_mass_multiplier = 1.0e6
            return base_mass_multiplier * (S_M_primordial ** 2)
        return 10.0  # Standard stellar-mass seed fallback
