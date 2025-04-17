import pandas as pd
import numpy as np
import matplotlib as mpl
import importlib.resources


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
                    cmap_reversed = mpl.colors.ListedColormap(normalized_data[::-1], name=f"{name}_r")

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