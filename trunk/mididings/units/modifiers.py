# -*- coding: utf-8 -*-
#
# mididings
#
# Copyright (C) 2008-2009  Dominic Sacré  <dominic.sacre@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import _mididings

from mididings.units.base import _Unit, _unit_repr

import mididings.util as _util
import mididings.misc as _misc


@_unit_repr
def Port(port):
    return _Unit(_mididings.Port(_util.port_number(port)))


@_unit_repr
def Channel(channel):
    return _Unit(_mididings.Channel(_util.channel_number(channel)))


@_unit_repr
def Transpose(offset):
    return _Unit(_mididings.Transpose(offset))


@_unit_repr
def Velocity(*args, **kwargs):
    value, mode = _misc.call_overload(
        'Velocity', args, kwargs, [
            lambda offset: (offset, 1),
            lambda multiply: (multiply, 2),
            lambda fixed: (fixed, 3)
        ]
    )
    return _Unit(_mididings.Velocity(value, mode))

# for backward compatibility, deprecated
def VelocityMultiply(value):
    return Velocity(multiply=value)

def VelocityFixed(value):
    return Velocity(fixed=value)


@_unit_repr
def VelocityCurve(gamma):
    return _Unit(_mididings.VelocityCurve(gamma))


@_unit_repr
def VelocitySlope(*args, **kwargs):
    notes, values, mode = _misc.call_overload(
        'VelocitySlope', args, kwargs, [
            lambda notes, offset: (notes, offset, 1),
            lambda notes, multiply: (notes, multiply, 2),
            lambda notes, fixed: (notes, fixed, 3)
        ]
    )
    # FIXME: allow arbitrary number of notes/values
    assert len(notes) == len(values) == 2
    note_lower = _util.note_number(notes[0])
    note_upper = _util.note_number(notes[1])
    return _Unit(_mididings.VelocityGradient(note_lower, note_upper, values[0], values[1], mode))


# for backward compatibility, deprecated
def VelocityGradient(note_lower, note_upper, value_lower, value_upper):
    return VelocitySlope((note_lower, note_upper), offset=(value_lower, value_upper))

def VelocityGradientMultiply(note_lower, note_upper, value_lower, value_upper):
    return VelocitySlope((note_lower, note_upper), multiply=(value_lower, value_upper))

def VelocityGradientFixed(note_lower, note_upper, value_lower, value_upper):
    return VelocitySlope((note_lower, note_upper), fixed=(value_lower, value_upper))


@_unit_repr
def CtrlMap(ctrl_in, ctrl_out):
    return _Unit(_mididings.CtrlMap(
        _util.ctrl_number(ctrl_in),
        _util.ctrl_number(ctrl_out)
    ))


@_unit_repr
def CtrlRange(ctrl, out_min, out_max, in_min=0, in_max=127):
    if not in_min < in_max:
        raise ValueError("in_min must be less than in_max")
    return _Unit(_mididings.CtrlRange(
        _util.ctrl_number(ctrl),
        out_min, out_max, in_min, in_max
    ))
