"""
Definitions of handy particle PDGID literals
============================================

The PDGID literals provide aliases for most common particle PDGIDs, with easily recognisable names.
The aliases are instances of the PDGID class.

Typical use cases::

    >>> from particle.pdgid import literals as lid
    >>> lid.pi_plus
    <PDGID: 211>
    >>> lid.pi_plus.is_meson
    True
    >>> from particle.pdgid.literals import Lb0
    >>>> Lb0
    <PDGID: 5122>
    >>> Lb0.has_bottom
    True

List of available/defined particle PDGID literals:

{0}
"""
from ..shared_literals import common_particles
from .pdgid import PDGID

for item in common_particles:
    locals()[item] = PDGID(common_particles[item])

__doc = ""
for item in common_particles: __doc += "  {item!s} = PDGID({pdgid})\n".format(item=item, pdgid=common_particles[item])

__doc__ = __doc__.format(__doc)

del PDGID, common_particles