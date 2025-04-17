import mcmaps
import numpy as np
import matplotlib.pyplot as plt


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


def test_save_colormap_gallery_html():
    """Test and save an HTML gallery of all registered colormaps."""
    from mcmaps import cm

    output_path = "docs/test_colormap_gallery.html"
    colormaps = cm.list_colormaps(include_reversed=False)

    with open(output_path, "w") as f:
        f.write("<html><body>\n")
        for name in colormaps:
            f.write(f"<h2>{name}</h2>\n")
            f.write(
                f"<div style='background: {getattr(cm, name)(0)}; width: 100px; height: 100px;'></div>\n"
            )
        f.write("</body></html>\n")
