# coding: utf8
"""
implémentation d'une superellipse
"""

import math

from ..linspace import linspace
from ..utils import spe_cos, spe_sin

class Superellipse(object):
    """
    définit une superellipse.

    x = rx c(theta, 2/m)
    y = ry s(theta, 2/m)

    où

    c(theta, m) = sign(cos(theta))|cos(theta)|**m
    s(theta, m) = sign(sin(theta))|sin(theta)|**m

    Paramètres
    ==========

    n : nombre de points de discrétisation en theta

    rx : rayon suivant x

    ry : rayon suivant y

    m : puissance dans l'expression de la superellipse.

    Attributs
    =========
    n : nombre de points de discrétisation en theta

    rx : rayon suivant x

    ry : rayon suivant y

    m : puissance dans l'expression de la superellipse.

    Méthodes
    ========

    surface: renvoie les points de la surface.

    area: renvoie l'aire.

    """

    def __init__(self, n, rx, ry, m):
        self.n = n
        self.rx = rx
        self.ry = ry
        self.m = m

    def surface(self):
        """
        retourne les points à la surface de la superellipse
        """
        phi_list = linspace(0., 2.*math.pi, self.n)
        x = []
        y = []
        for phi in phi_list:
            x.append(self.rx*spe_cos(phi, 2./self.m))
            y.append(self.ry*spe_sin(phi, 2./self.m))
        return x, y

    @property
    def area(self):
        """
        retourne l'aire de la superellipse
        """
        r = 1./self.m
        return 4**(1-r)*self.rx*self.ry*math.sqrt(math.pi)*math.gamma(1+r)/math.gamma(.5+r)

class Circle(Superellipse):
    """
    définit un cercle à partir d'une superellipse
    """
    def __init__(self, n, r):
        super(Circle, self).__init__(n, r, r, 2)

    @property
    def perimeter(self):
        """
        retourne le préimètre d'un cercle
        """
        return 2*math.pi*self.rx
