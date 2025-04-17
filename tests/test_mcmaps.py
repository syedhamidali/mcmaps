import pytest
import mcmaps
import matplotlib as mpl

def test_load_and_register_colormaps():
    """Test loading and registering colormaps."""
    mcmaps._load_and_register_colormaps()

    # Verify a colormap is loaded
    cmap = mpl.colormaps.get("test_colormap")
    assert cmap is not None, "Colormap 'test_colormap' was not registered."

    # Verify reversed colormap
    cmap_reversed = mpl.colormaps.get("test_colormap_r")
    assert cmap_reversed is not None, "Reversed colormap was not registered."