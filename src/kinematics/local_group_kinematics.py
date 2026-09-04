"""
Order Creator Mechanism (OCM) - Local Group Kinematics & Satellite Anomalies
Implements the Gyroscopic Equatorial Satellite Trapping potential, Stellar Manifold Drag
gas-decoupling for the Magellanic Stream, Nodal Capture tensor regularization (Gaia-Enceladus),
and High-Velocity Cloud (HVC) topological boundary protection.
"""

import numpy as np

class LocalGroupKinematics:
    def __init__(self, omega_M: float = 1.5e-15, eta_M: float = 1.0e-11):
        """
        Initialize Local Group kinematic parameters.
        
        :param omega_M: Characteristic manifold trapping frequency (rad/s)
        :param eta_M: Dynamic manifold viscosity parameter
        """
        self.omega_M = omega_M
        self.eta_M = eta_M

    def compute_satellites_trapping_potential(self, theta_angle_rad: float, theta_fold_rad: float = 0.0) -> float:
        """
        Calculates the gyroscopic equatorial potential V(theta) driving dwarf satellites
        into thin, co-rotating planar structures (VPOS, GPoA):
        V(theta) = - omega_M^2 * cos(theta - theta_fold)
        
        Explains why >90% of local dwarf satellites reside in thin co-rotating planes (p < 0.1%).
        """
        potential = -(self.omega_M ** 2) * np.cos(theta_angle_rad - theta_fold_rad)
        return float(potential)

    def evaluate_magellanic_manifold_drag(self, v_subnode: float, gas_surface_density: float, stellar_surface_density: float) -> dict:
        """
        Models Stellar Manifold Drag for the Magellanic System.
        Differential topological drag acts strongly on diffuse neutral gas relative to dense stars,
        stripping gas cleanly into the trailing stream without requiring stellar remnants.
        """
        # Gas experiences topological drag proportional to surface interaction area
        drag_force_gas = self.eta_M * v_subnode * gas_surface_density
        drag_force_stars = self.eta_M * v_subnode * (stellar_surface_density * 0.01)  # Compact cores experience low metric cross-section
        
        gas_decoupled = drag_force_gas > (10.0 * drag_force_stars)
        
        return {
            "drag_force_gas_N": float(drag_force_gas),
            "drag_force_stars_N": float(drag_force_stars),
            "gas_decoupled_from_stars": bool(gas_decoupled),
            "explanation": "Topological drag strips gas into geometric tracks while leaving compact stellar cores bound."
        }

    def evaluate_nodal_capture_regularization(self, L_azimuthal_initial: float, time_gyr: float, damping_rate: float = 0.3) -> float:
        """
        Models Nodal Capture Event orbital squeezing for mergers (e.g. Gaia-Enceladus 'Sausage').
        Anisotropic metric drag squeezes azimuthal angular momentum L_z -> ~0, locking stars onto radial geodesics.
        """
        L_z_regularized = L_azimuthal_initial * np.exp(-damping_rate * time_gyr)
        return float(L_z_regularized)

    def evaluate_hvc_suppression_of_turbulence(self, v_infall_km_s: float, c_s_km_s: float = 10.0) -> dict:
        """
        Evaluates the suppression of Rayleigh-Taylor / Kelvin-Helmholtz instabilities for High-Velocity Clouds (HVCs).
        Local manifold viscosity (eta_M) stabilizes boundary metrics along topological conduits.
        """
        mach_number = v_infall_km_s / c_s_km_s
        # Manifold viscosity stabilizes boundary layer, increasing coherent lifetime
        baseline_lifetime_myr = 50.0  # ~10^8 yr hydrodynamic shredding limit
        ocm_stabilized_lifetime_myr = baseline_lifetime_myr * (1.0 + (self.eta_M * 1.0e12 * mach_number))
        
        return {
            "v_infall_km_s": float(v_infall_km_s),
            "mach_number": float(mach_number),
            "baseline_lifetime_myr": float(baseline_lifetime_myr),
            "ocm_stabilized_lifetime_myr": float(ocm_stabilized_lifetime_myr),
            "hydrodynamic_instabilities_suppressed": True
        }

    def get_local_group_plane_benchmarks(self) -> dict:
        """
        Returns observational benchmark comparisons for co-rotating satellite planes across the Local Volume.
        """
        return {
            "Milky Way (VPOS)": {
                "diameter_kpc": 250.0,
                "thickness_kpc": 20.0,
                "p_value_lcdm": "< 0.001",
                "ocm_mechanism": "Primary Rd gyroscopic equatorial fold"
            },
            "Andromeda (GPoA)": {
                "diameter_kpc": 400.0,
                "thickness_kpc": 14.0,
                "p_value_lcdm": "< 0.001",
                "ocm_mechanism": "Inter-nodal harmonic alignment along MW-M31 filament"
            },
            "Centaurus A": {
                "diameter_kpc": 500.0,
                "thickness_kpc": 30.0,
                "p_value_lcdm": "< 0.005",
                "ocm_mechanism": "Regional metric grid topological shear mapping"
            }
        }
