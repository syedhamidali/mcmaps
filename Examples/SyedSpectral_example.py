"""
Example: Using SyedSpectral Colormap
====================================

This script demonstrates how to use the `SyedSpectral` colormap included in `mcmaps`
to visualize reflectivity data.
"""

# %%
import mcmaps  # noqa
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# %%
# Create synthetic reflectivity field (looks like a cloud)
shape = (300, 300)
reflectivity = np.full(shape, -10.0)  # background dBZ

np.random.seed(101)
noise = np.random.rand(*shape)
cloud = gaussian_filter(noise, sigma=15)

cloud_normalized = (cloud - cloud.min()) / (cloud.max() - cloud.min())
cloud_dbz = cloud_normalized * 80 - 10  # -10 to 70 dBZ
cloud_mask = cloud_dbz > 0
reflectivity[cloud_mask] = cloud_dbz[cloud_mask]

# %%
# Plot using custom colormap
plt.figure(figsize=(7, 5))
plt.title("Example Reflectivity")
plt.imshow(reflectivity, cmap="SyedSpectral", vmin=-10, vmax=70, origin="lower")
plt.colorbar(label="Reflectivity (dBZ)")
plt.tight_layout()
plt.show()
