import mcmaps
import numpy as np
import matplotlib.pyplot as plt

from mcmaps import cm
from mcmaps.__init__ import _get_cmap_gallery_html


def test_load_and_register_colormaps():
    """Test that colormaps are loaded and registered correctly."""
    colormaps = mcmaps.cm.list_colormaps()
    assert isinstance(colormaps, list)
    assert len(colormaps) > 0
    for cmap_name in colormaps:
        assert hasattr(mcmaps.cm, cmap_name)


def test_reversed_colormaps():
    """Ensure reversed colormaps are registered correctly."""
    colormaps = mcmaps.cm.list_colormaps()
    for cmap_name in colormaps:
        reversed_name = f"{cmap_name}_r"
        assert reversed_name in mcmaps.cm.list_colormaps(include_reversed=True)
        assert hasattr(mcmaps.cm, reversed_name)


def test_plot_sample_colormap():
    cmap = getattr(mcmaps.cm, "SyedSpectral", None)
    assert cmap is not None

    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.imshow(gradient, aspect="auto", cmap=cmap)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig("tests/output/test_syedspectral_colormap.png")


def test_save_all_colormaps_preview():
    """Test and save a single figure showing all registered colormaps."""
    from mcmaps import cm
    import matplotlib.pyplot as plt
    import os

    colormaps = cm.list_colormaps(include_reversed=False)
    n_maps = len(colormaps)
    gradient = np.linspace(0, 1, 256).reshape(1, -1)

    fig, axes = plt.subplots(nrows=n_maps, figsize=(8, 0.4 * n_maps))
    if n_maps == 1:
        axes = [axes]

    for ax, name in zip(axes, colormaps):
        cmap = getattr(cm, name)
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.set_axis_off()
        ax.set_title(name, fontsize=8, loc="left", pad=2)

    plt.tight_layout()
    os.makedirs("tests/output", exist_ok=True)
    plt.savefig("tests/output/all_colormaps_preview.png", dpi=150)
    plt.close(fig)


def test_get_cmap_gallery_html_basic():
    html_output = _get_cmap_gallery_html(cm._colormaps)
    assert "<div" in html_output
    assert "img" in html_output
    for name in cm.list_colormaps():
        assert f'alt="{name}"' in html_output
        assert f'title="{name}"' in html_output


def test_get_cmap_gallery_html_sorted():
    from bs4 import BeautifulSoup

    def extract_names(html):
        soup = BeautifulSoup(html, "html.parser")
        return [strong.get_text() for strong in soup.find_all("strong")]

    html_unsorted = _get_cmap_gallery_html(cm._colormaps, sort_d=False)
    html_sorted = _get_cmap_gallery_html(cm._colormaps, sort_d=True)

    names_unsorted = extract_names(html_unsorted)
    names_sorted = extract_names(html_sorted)

    assert sorted(names_unsorted) == names_sorted
