#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import GLib
from gi.repository import Gio
import os
import sys

PROC_NAME = "plug-in-m3ga-save-selection-png"
BINARY    = "m3ga-save-selection-png"
OUT_DIR   = os.path.expanduser("~/gimp-selections")


def next_path():
    os.makedirs(OUT_DIR, exist_ok=True)
    n = 0
    while True:
        p = os.path.join(OUT_DIR, f"selection_{n:04d}.png")
        if not os.path.exists(p):
            return p
        n += 1


def run(procedure, run_mode, image, drawables, config, data):
    success, non_empty, x1, y1, x2, y2 = Gimp.Selection.bounds(image)

    if not non_empty:
        Gimp.message("No active selection. Please draw a selection first!")
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

    dup = image.duplicate()
    dup.flatten()

    layer = dup.get_layers()[0]
    layer.add_alpha()

    # The GIMP 3.2 Hybrid Fix
    Gimp.Selection.invert(dup)
    layer.edit_clear()
    Gimp.Selection.none(dup)

    dup.crop(x2 - x1, y2 - y1, x1, y1)

    path = next_path()

    # FIXED: In GIMP 3.0+, it is "file-png-export", not "file-png-save"
    proc = Gimp.get_pdb().lookup_procedure('file-png-export')
    cfg  = proc.create_config()
    cfg.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE)
    cfg.set_property('image',    dup)
    cfg.set_property('file',     Gio.File.new_for_path(path))

    proc.run(cfg)

    dup.delete()

    # Deselect the selection on the original image
    Gimp.Selection.none(image)
    Gimp.displays_flush()

    Gimp.message(f"Success! Saved to {path}")

    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


class SaveSelectionPng(Gimp.PlugIn):
    def do_query_procedures(self):
        return [PROC_NAME]

    def do_create_procedure(self, name):
        if name != PROC_NAME:
            return None
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, run, None)
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        procedure.set_menu_label("_Save Selection as PNG")
        procedure.set_attribution("Megaguy32", "Megaguy32", "2026")
        procedure.add_menu_path("<Image>/File/Export")
        procedure.set_documentation(
            "Save current selection as an incremental PNG",
            "Exports the active selection to ~/gimp-selections/selection_NNNN.png "
            "with transparency outside the freehand boundary.",
            None)
        return procedure


Gimp.main(SaveSelectionPng.__gtype__, sys.argv)
