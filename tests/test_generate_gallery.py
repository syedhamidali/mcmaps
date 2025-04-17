from mcmaps import generate_gallery


def test_generate_colormap_gallery_html(tmp_path):
    # Define output path using pytest's tmp_path fixture
    output_path = tmp_path / "test_colormap_gallery.html"

    # Run the function
    generate_gallery.save_colormap_gallery_html(str(output_path))

    # Assertions
    assert output_path.exists(), "HTML file was not created."
    content = output_path.read_text()
    assert "<html>" in content
    assert "</html>" in content
    assert "Colormap Gallery" in content
