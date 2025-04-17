from . import cm, _get_cmap_gallery_html
import os


def save_colormap_gallery_html(output_path):
    html_str = _get_cmap_gallery_html(cm._colormaps, sort_d=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html_str)


if __name__ == "__main__":
    output_file = os.path.join(
        os.path.dirname(__file__),
        "..",
        "docs",
        "source",
        "_static",
        "colormap_gallery.html",
    )
    output_file = os.path.abspath(output_file)
    save_colormap_gallery_html(output_file)
    print(f"Gallery HTML saved to: {output_file}")
