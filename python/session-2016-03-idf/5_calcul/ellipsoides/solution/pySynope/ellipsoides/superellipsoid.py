# coding: utf8
"""
implémentation d'une superellipsoide
"""

import numpy as np

from ..utils import spe_cos, spe_sin
from .superellipse import Superellipse

def beta_func(r, t):
    """
    retourne la fonction beta.
    """  
    return math.gamma(r)*math.gamma(t)/math.gamma(r+t)

class Superellipsoid(object):
    """
    Définit une superellipsoid.

    x = rx c(theta, 2/m1) c(phi, 2/m2)
    y = ry s(theta, 2/m1) c(phi, 2/m2)
    y = rz s(phi, 2/m2)

    où
    c(theta, m) = sign(cos(theta))|cos(theta)|**m
    s(theta, m) = sign(sin(theta))|sin(theta)|**m

    Paramètres
    ==========

    n : nombre de points de discrétisation en theta et en phi

    rx : rayon suivant x

    ry : rayon suivant y

    rz : rayon suivant z

    m : puissance dans l'expression de la superellipse.

    Attributs
    =========

    n : nombre de points de discrétisation en theta et en phi

    rx : rayon suivant x

    ry : rayon suivant y

    rz : rayon suivant z

    m : puissance dans l'expression de la superellipse.

    Méthodes
    ========

    surface : renvoie le nuage de points de la surface.

    volume : renvoie le volume de la superellipsoide.
    """
    def __init__(self, n, rx, ry, rz, m1, m2):
        self.n = n
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.m1 = m1
        self.m2 = m2

    def surface(self):
        """
        retourne les points à la surface de la superellipsoide.
        """
        phi = np.linspace(-.5*np.pi, .5*np.pi, self.n)[:, np.newaxis]
        theta = np.linspace(-np.pi, np.pi, self.n)[np.newaxis, :]

        x = self.rx*spe_cos(phi, 2./self.m1)*spe_cos(theta, 2./self.m2)
        y = self.ry*spe_cos(phi, 2./self.m1)*spe_sin(theta, 2./self.m2)
        z = self.rz*spe_sin(phi, 2./self.m1)*np.ones(theta.shape)
        return x, y, z

    def surface_with_square(self):
        """
        retourne les points à la surface de la superellipsoid
        en projetant un carré sur  deux superellipses et en 
        faisant leur produit sphérique.
        """
        s1 = Superellipse(self.n, 1, 1, self.m1)
        s2 = Superellipse(self.n, 1, 1, self.m2)

        gx, gy = s1.surface_with_square()
        hx, hy = s2.surface_with_square()

        x = self.rx*gx[np.newaxis, :]*hx[:, np.newaxis]
        y = self.ry*gx[np.newaxis, :]*hy[:, np.newaxis]
        z = self.rz*gy[np.newaxis, :]*np.ones(hx.size)[:, np.newaxis]

        return x, y, z

    @property
    def volume(self):
        """
        retourne le volume de la superellipsoide.
        """
        r = 1./self.m1
        t = 1./self.m2
        return 8./3.*self.rx*self.ry*self.rz*r*t*beta_func(r, r)*beta_func(2*t, t)

class Sphere(Superellipsoid):
    """
    Définit une sphère à partir d'une superellipsoide.
    """
    def __init__(self, n, r):
        super(Sphere, self).__init__(n, r, r, r, 2, 2)

    @property
    def area(self):
        """
        retourne l'aire de la surface d'une sphère
        """
        return 4*np.pi*self.rx**2
