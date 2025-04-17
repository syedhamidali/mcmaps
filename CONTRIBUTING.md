# Submit Your Colormap: A Contributor's Guide

Thank you for your interest in contributing to the `mcmaps` library! Here's a short guide to help you submit your custom colormap.

---

## 1. Understand the File Format

Each colormap must be provided as a `.csv` or `.txt` file, with the following format:

1. The file can include metadata (e.g., comments, author name, credits) at the top.
2. The actual RGB data must be preceded by the marker line:
   ```
   # R,G,B
   ```
3. Each row after the marker should contain comma-separated RGB values in the range [0–255].

### Example Colormap File (`MyColormap.csv`)
```csv
# My Custom Colormap
# Author: Your Name
# License: MIT
# R,G,B
0,0,255
0,128,255
0,255,255
0,255,0
255,255,0
255,0,0
```

---

## 2. Add Your Colormap

1. Clone the repository:
   ```bash
   git clone https://github.com/syedhamidali/mcmaps.git
   cd mcmaps
   ```

2. Add your colormap file to the `data` directory:
   ```bash
   cp MyColormap.csv mcmaps/data/
   ```

3. Ensure the filename is descriptive and unique (e.g., `MyColormap.csv`).

---

## 3. Test Your Colormap

Before submitting, test your colormap locally:

1. Install the package in development mode:
   ```bash
   pip install -e .
   ```

2. Use your colormap in Matplotlib:
   ```python
   import mcmaps
   import matplotlib.pyplot as plt

   # Use your colormap
   plt.contourf([[0, 1], [1, 0]], cmap='MyColormap')
   plt.colorbar()
   plt.show()
   ```

3. Ensure it works as expected, and verify the reversed colormap (`MyColormap_r`) is also registered.

---

## 4. Submit a Pull Request

1. Commit your changes:
   ```bash
   git add mcmaps/data/MyColormap.csv
   git commit -m "Add MyColormap"
   ```

2. Push your changes to your fork:
   ```bash
   git push origin <branch-name>
   ```

3. Open a pull request on the repository:
   - Provide a short description of your colormap.
   - Include any relevant metadata, such as authorship or licensing details.

---

## 5. Review and Approval

Our maintainers will:
- Review your submission for formatting and functionality.
- Test your colormap in the library.
- Provide feedback or approve the PR.

Once approved, your colormap will be part of `mcmaps`!

---

### Example Submission Checklist

- [ ] File is placed in `mcmaps/data/`.
- [ ] File contains metadata, including author and license information.
- [ ] RGB values are normalized between 0–255 and follow the correct format.
- [ ] Successfully tested locally with Matplotlib.

---

Thank you for contributing to `mcmaps`! Together, we can make visualization even more colorful.