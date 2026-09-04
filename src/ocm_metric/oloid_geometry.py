"""
Order Creator Mechanism (OCM) - Oloid Interface & Metric Geometry
Implements the K=0 developable Oloid manifold core equations at R_d.
"""

import numpy as np

class OloidInterface:
    def __init__(self, radius_d: float, angular_momentum: float):
        """
        Initialize the Nodal Interface (R_d).
        :param radius_d: Schwarzschild-Planck boundary radius R_d (in meters)
        :param angular_momentum: Angular momentum J > 0
        """
        self.R_d = radius_d
        self.J = angular_momentum
        
    def gaussian_curvature(self) -> float:
        """
        The Oloid manifold surface exhibits identically zero Gaussian curvature (K = k1 * k2 = 0).
        Renders boundary locally isometric to a flat Euclidean plane (shear-free line-contact).
        """
        return 0.0

    def compute_laminar_flux(self, radial_mass_inflow: float) -> float:
        """
        Converts chaotic frame-dragged accretion into a laminar manifold flux stream (kappa)
        sequestered through the 4D nodal conduit.
        """
        if self.J > 0:
            # Laminar conversion factor under K=0 shear-free boundary
            kappa_flux = radial_mass_inflow * (1.0 - self.gaussian_curvature())
            return kappa_flux
        else:
            # Spherical collapse fallback
            return radial_mass_inflow
