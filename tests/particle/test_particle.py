# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import sys

import pytest
from pytest import approx

from particle.particle.enums import Charge, Parity, SpinType
from particle.particle import Particle
from particle.particle.particle import ParticleNotFound, InvalidParticle
from particle.pdgid import PDGID


def test_enums_Charge():
    assert Charge.p + Charge.m == Charge.o
    assert Charge.pp + Charge.mm == Charge.o


def test_enums_SpinType():
    assert SpinType.PseudoScalar == - SpinType.Scalar
    assert SpinType.Axial == - SpinType.Vector
    assert SpinType.PseudoTensor == - SpinType.Tensor


def test_from_search():
    # 1 match found
    assert repr(Particle.from_search(name_s='gamma')) ==  "<Particle: pdgid=22, fullname='gamma0', mass=0.0 MeV>"

    # No match found
    with pytest.raises(ParticleNotFound):
        p = Particle.from_search(name_s='NonExistent')

    # Multiple matches found
    with pytest.raises(RuntimeError):
        p = Particle.from_search(name_s='Upsilon')


def test_pdg():
    assert Particle.from_pdgid(211).pdgid == 211
    with pytest.raises(InvalidParticle):
        p = Particle.from_pdgid(0)


def test_pdg_convert():
    p = Particle.from_pdgid(211)
    assert isinstance(p.pdgid, PDGID)
    assert int(p) == 211
    assert PDGID(p) == 211


def test_sorting():
    assert Particle.from_pdgid(211) < Particle.from_pdgid(311)
    assert Particle.from_pdgid(211) < Particle.from_pdgid(-311)


def test_int_compare():
    assert Particle.from_pdgid(211) > 0
    assert Particle.from_pdgid(-211) < 0
    assert Particle.from_pdgid(211) >= 0
    assert Particle.from_pdgid(-211) <= 0

    assert 0 < Particle.from_pdgid(211)
    assert 0 > Particle.from_pdgid(-211)
    assert 0 <= Particle.from_pdgid(211)
    assert 0 >= Particle.from_pdgid(-211)


def test_str():
    pi = Particle.from_pdgid(211)
    assert str(pi) == 'pi+'


def test_rep():
    pi = Particle.from_pdgid(211)
    assert "pdgid=211" in repr(pi)
    assert "fullname='pi+'" in repr(pi)
    assert "mass=139.57" in repr(pi)


def test_basic_props():
    pi = Particle.from_pdgid(211)
    assert pi.name == 'pi'
    assert pi.pdgid == 211
    assert pi.three_charge == Charge.p


def test_lifetime_props():
    pi = Particle.from_pdgid(211)
    assert pi.lifetime == approx(26.0327460625985)   # in nanoseconds
    assert pi.ctau == approx(7804.4209306)   # in millimeters


def test_describe():
    __description = u'Lifetime = 26.033 ± 0.005 ns'
    if sys.version_info < (3,0):
        __description = __description.replace(u'±', u'+/-')
    pi = Particle.from_pdgid(211)
    assert __description in pi.describe()

    __description = """Name: gamma      ID: 22           Fullname: gamma0         Latex: $\gamma$
Mass  = 0.0 MeV
Width = 0.0 MeV
I (isospin)       = <2     G (parity)        = 0      Q (charge)       = 0
J (total angular) = 1.0    C (charge parity) = ?      P (space parity) = ?
    Antiparticle status: Same (antiparticle name: gamma0)"""
    photon = Particle.from_pdgid(22)
    assert photon.describe() == __description

    __description = 'Width = 1.89 + 0.09 - 0.18 MeV'
    Sigma_c_pp = Particle.from_pdgid(4222)
    assert __description in Sigma_c_pp.describe()


def test_ampgen_style_names():
    assert Particle.from_string('pi+').pdgid == 211
    assert Particle.from_string('pi-').pdgid == -211
    assert Particle.from_string('K~*0').pdgid == -313
    assert Particle.from_string('K*(892)bar0').pdgid == -313
    assert Particle.from_string('a(1)(1260)+').pdgid == 20213

    # Direct comparison to integer works too
    assert Particle.from_string('rho(1450)0') == 100113
    assert Particle.from_string('rho(770)0') == 113

    assert Particle.from_string('K(1)(1270)bar-') == -10323
    assert Particle.from_string('K(1460)bar-') == -100321


def test_decfile_style_names():
    assert Particle.from_dec('anti-K*0').pdgid == -313
    assert Particle.from_dec('a_1(1260)+').pdgid == 20213
    #assert Particle.from_dec("D'_1+").pdgid == 7
    #assert Particle.from_dec("D_2*+").pdgid == 8
