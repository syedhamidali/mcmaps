"""Top-level package for radarx."""

__author__ = """Hamid Ali Syed"""
__email__ = "hamidsyed37@gmail.com"


import pandas as pd
import matplotlib as mpl
import importlib.resources

# versioning
try:
    from .version import version as __version__
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"


class ColormapContainer:
    """
    A container for dynamically registering and accessing colormaps.

    Attributes
    ----------
    All colormap names are dynamically registered as attributes of this class
    and are available globally in Matplotlib by their names.
    """

    def __init__(self):
        self._colormaps = {}
        self._register_colormaps()

    def _normalize_data(self, data):
        """
        Normalize RGB data to the range [0, 1].

        Parameters
        ----------
        data : numpy.ndarray
            The RGB data array.

        Returns
        -------
        numpy.ndarray
            Normalized RGB data in the range [0, 1].
        """
        max_value = data.max()
        return data / max_value if max_value > 0 else data

    def _read_colormap_file(self, file):
        """
        Read and parse the colormap file, skipping lines until the `# R,G,B` marker.

        Parameters
        ----------
        file : Traversable
            The file to read.

        Returns
        -------
        numpy.ndarray
            Parsed RGB data as a NumPy array.
        """
        with file.open() as f:
            # Read lines until the marker is found
            for line in f:
                if line.strip() == "# R,G,B":
                    break
            # Read the remaining lines as CSV data
            return pd.read_csv(f, header=None).to_numpy()

    def _register_colormaps(self):
        """
        Dynamically register colormaps from the `data` directory and set them as attributes.

        Colormaps are registered with Matplotlib so they can be used globally by their names.
        """
        try:
            # Dynamically resolve the data path using importlib.resources
            data_path = importlib.resources.files("mcmaps.data")
            try:
                files = list(data_path.iterdir())  # Safely list files in the directory
            except Exception as e:
                print(f"Warning: Unable to list files in `data` directory: {e}")
                return

            for file in files:
                if file.suffix in {".csv", ".txt"}:
                    name = file.stem

                    # Read and normalize colormap data
                    data = self._read_colormap_file(file)
                    normalized_data = self._normalize_data(data)

                    # Create colormap and reversed version
                    cmap = mpl.colors.ListedColormap(normalized_data, name=name)
                    cmap_reversed = mpl.colors.ListedColormap(
                        normalized_data[::-1], name=f"{name}_r"
                    )

                    # Register with Matplotlib
                    mpl.colormaps.register(cmap, name=name)
                    mpl.colormaps.register(cmap_reversed, name=f"{name}_r")

                    # Add colormap to container attributes
                    self._colormaps[name] = cmap
                    self._colormaps[f"{name}_r"] = cmap_reversed
                    setattr(self, name, cmap)
                    setattr(self, f"{name}_r", cmap_reversed)
        except ModuleNotFoundError as e:
            print(f"Error loading colormaps: {e}")
        except Exception as e:
            print(f"Unexpected error while registering colormaps: {e}")

    def list_colormaps(self, include_reversed=False):
        """
        List all available colormaps included in the package.

        Parameters
        ----------
        include_reversed : bool, optional
            Whether to include reversed colormaps in the list, by default False.

        Returns
        -------
        list of str
            A list of colormap names.
        """
        if include_reversed:
            return list(self._colormaps.keys())
        return [name for name in self._colormaps if not name.endswith("_r")]


# Create a global colormap container
cm = ColormapContainer()


def save_all_colormaps_preview(output_dir="docs/colormaps", width=6, height=1):
    """
    Save preview images of all registered colormaps to a directory.

    Parameters
    ----------
    output_dir : str
        Directory where the preview images will be saved.
    width : float
        Width of the generated figure in inches.
    height : float
        Height of the generated figure in inches.
    """
    import os
    import numpy as np
    import matplotlib.pyplot as plt

    os.makedirs(output_dir, exist_ok=True)
    gradient = np.linspace(0, 1, 256).reshape(1, -1)

    for name, cmap in cm._colormaps.items():
        fig, ax = plt.subplots(figsize=(width, height))
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.set_axis_off()
        plt.tight_layout()
        output_path = os.path.join(output_dir, f"{name}.png")
        plt.savefig(output_path, dpi=150)
        plt.close(fig)


def save_colormap_gallery_html(
    output_path="docs/colormap_gallery.html", width=256, height=20
):
    """
    Save an HTML gallery of all registered colormaps for visual reference.

    Parameters
    ----------
    output_path : str
        Path to the output HTML file.
    width : int
        Width of each colormap image in pixels.
    height : int
        Height of each colormap image in pixels.
    """
    import base64
    import io
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    gradient = np.linspace(0, 1, 256).reshape(1, -1)

    html = [
        "<html><head><style>",
        "body { font-family: sans-serif; background: #f8f8f8; padding: 20px; }",
        ".cmap-img { margin-bottom: 20px; }",
        "img { border: 1px solid #ccc; display: block; margin-top: 5px; }",
        "</style></head><body><h1>Colormap Gallery</h1>",
    ]

    for name in cm.list_colormaps(include_reversed=False):
        cmap = getattr(cm, name)
        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.axis("off")
        plt.tight_layout(pad=0)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        buf.seek(0)
        plt.close(fig)

        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        html.append(f'<div class="cmap-img"><strong>{name}</strong>')
        html.append(
            f'<img src="data:image/png;base64,{img_b64}" width="{width}" height="{height}"></div>'
        )

    html.append("</body></html>")

    with open(output_path, "w") as f:
        f.write("\n".join(html))
