# mcmaps

A Python package providing pre-defined custom colormaps for visualization.

## Installation

```bash
python -m pip install git+https://github.com/syedhamidali/mcmaps
```
## Example

```python
import mcmaps  # Automatically registers colormaps

# Use the colormap directly in matplotlib
import matplotlib.pyplot as plt

plt.contourf([[0, 1], [1, 0]], cmap='SyedSpectral')
plt.colorbar()
plt.show()
```
