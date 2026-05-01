# m3ga-save-selection-png

A GIMP 3.2 plug-in that exports the active selection to a PNG with correct transparency and sequential auto-naming.

## What it does

- Takes whatever selection is active (rectangle, freehand, fuzzy — anything)
- Clears everything outside the selection boundary with real alpha (not a bounding-box crop of a flattened layer)
- Crops the canvas to the selection's bounding box
- Saves to `~/gimp-selections/selection_0000.png`, incrementing the counter each run so nothing is overwritten
- Deselects on the original image and flushes the display

The menu entry appears at **File → Export → Save Selection as PNG**.

## Requirements

- GIMP 3.2+
- Python 3 (bundled with GIMP on most distros)

## Install

```bash
PLUG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/GIMP/3.2/plug-ins/save-selection-png"
mkdir -p "$PLUG_DIR"
cp save-selection-png.py "$PLUG_DIR/save-selection-png.py"
chmod +x "$PLUG_DIR/save-selection-png.py"
```

Double check [gimp dev docs](https://developer.gimp.org/resource/writing-a-plug-in/) 

Restart GIMP after installing.

## Output

Files land in `~/gimp-selections/` as `selection_0000.png`, `selection_0001.png`, etc. The directory is created automatically on first run.

## Notes

- Uses `file-png-export` (GIMP 3.2 PDB name) — not the old `file-png-save` which was removed.
- The transparency trick is invert → clear → deselect rather than a mask, which correctly handles non-rectangular freehand selections where a simple bounding-box crop would include unwanted pixels.
- The original image is never modified; all work is done on a duplicate.

## License

LGPL-2.1
