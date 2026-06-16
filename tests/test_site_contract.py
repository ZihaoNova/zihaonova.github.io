from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_full_template_directories_are_present() -> None:
    required_paths = [
        "_sass/_variables.scss",
        "_sass/vendor/font-awesome/fontawesome.scss",
        "assets/js/main.min.js",
        "assets/fonts/fa-solid-900.woff2",
        "google_scholar_crawler/main.py",
        ".github/workflows/google_scholar_crawler.yaml",
        "_includes/fetch_google_scholar_stats.html",
        "_includes/seo.html",
    ]

    for relative_path in required_paths:
        assert (ROOT / relative_path).exists(), relative_path


def test_default_layout_does_not_reference_missing_compress_layout() -> None:
    default_layout = read_text("_layouts/default.html")

    assert "layout: compress" not in default_layout
    assert "<!doctype html>" in default_layout


def test_site_identity_config_is_zihao() -> None:
    config = read_text("_config.yml")

    assert 'title                    : "Zihao Huang"' in config
    assert 'repository               : "ZihaoNova/ZihaoNova.github.io"' in config
    assert 'url                      : "https://zihaonova.github.io"' in config
    assert 'name             : "Zihao Huang"' in config
    assert 'bio              : "Faculty member (Lecturer), Zhejiang A&F University"' in config
    assert 'github           : "ZihaoNova"' in config
    assert "GOOGLE_SCHOLAR_ID" not in config


def test_homepage_content_is_zihao_profile() -> None:
    homepage = read_text("_pages/about.md")

    required_text = [
        "Zihao Huang",
        "Zhejiang A&F University",
        "Faculty member (Lecturer)",
        "University of Eastern Finland",
        "forest resource remote sensing",
        "forest age dynamics",
        "forest carbon cycle modeling",
        "Publications",
        "Selected Projects",
        "An Algorithm of Forest Age Estimation Based on the Forest Disturbance and Recovery Detection",
        "Integrating land use/cover change (LUCC) with forest aging",
        "Assessing the impact of land use and cover change on above-ground carbon storage",
        "Centennial spatiotemporal evolution of AGC in subtropical forests",
        "Simulating Future LUCC by Coupling Climate Change and Human Effects",
        "Spatiotemporal LUCC Simulation under Different RCP Scenarios",
        "土地利用/覆盖变化及其对森林碳收支影响研究综述",
        "Forest age estimation from disturbance and recovery",
        "LUCC simulation under climate and human effects",
        "Forest carbon storage and NEP projection",
    ]

    for text in required_text:
        assert text in homepage

    assert homepage.count("class='paper-box'") == 3


def test_news_section_structure_is_preserved() -> None:
    homepage = read_text("_pages/about.md")

    assert "id='-news'" in homepage
    assert "# 🔥 News" in homepage


def test_publication_journal_names_are_italicized_consistently() -> None:
    homepage = read_text("_pages/about.md")

    expected_journals = [
        "*IEEE Transactions on Geoscience and Remote Sensing*",
        "*Agricultural and Forest Meteorology*",
        "*Geo-spatial Information Science*",
        "*Ecological Indicators*",
        "*Remote Sensing*",
        "*ISPRS International Journal of Geo-Information*",
        "*遥感学报*",
    ]

    for journal in expected_journals:
        assert journal in homepage

    mojibake_snippets = ["鍦熷湴", "榛勫瓙", "閬ユ劅"]
    for snippet in mojibake_snippets:
        assert snippet not in homepage


def test_navigation_anchors_are_stable() -> None:
    navigation = read_text("_data/navigation.yml")
    homepage = read_text("_pages/about.md")

    required_pairs = [
        ('url: "/#about-me"', "id='about-me'"),
        ('url: "/#-news"', "id='-news'"),
        ('url: "/#-publications"', "id='-publications'"),
        ('url: "/#-honors-and-awards"', "id='-honors-and-awards'"),
        ('url: "/#-educations"', "id='-educations'"),
        ('url: "/#-invited-talks"', "id='-invited-talks'"),
        ('url: "/#-internships"', "id='-internships'"),
    ]

    for nav_url, anchor in required_pairs:
        assert nav_url in navigation
        assert anchor in homepage


def test_google_scholar_workflow_is_manual_until_configured() -> None:
    config = read_text("_config.yml")
    scripts = read_text("_includes/scripts.html")
    workflow = read_text(".github/workflows/google_scholar_crawler.yaml")
    funding = read_text(".github/FUNDING.yml")

    assert "google_scholar_enabled   : false" in config
    assert "{% if site.google_scholar_enabled %}" in scripts
    assert "workflow_dispatch:" in workflow
    assert "Check Scholar Secret" in workflow
    assert "GOOGLE_SCHOLAR_ID is not configured; skipping crawler." in workflow
    assert "schedule:" not in workflow
    assert "page_build:" not in workflow
    assert "github: RayeRen" not in funding


def test_custom_visual_assets_and_polish_exist() -> None:
    css = read_text("assets/css/main.scss")
    site_css = read_text("assets/css/site.css")
    head = read_text("_includes/head.html")

    required_assets = [
        "images/site-icon.svg",
        "images/land-cover-simulation.svg",
        "images/raster-validation.svg",
        "images/dask-pipeline.svg",
    ]

    for relative_path in required_assets:
        assert (ROOT / relative_path).exists(), relative_path

    assert "Zihao Huang custom polish" in css
    assert ".site-footer" in css
    assert 'href="assets/css/site.css"' in head
    assert ".paper-box" in site_css
    assert "linear-gradient(135deg, #2563eb, #0f766e)" in css
    assert "<base target=" not in head


def test_sidebar_contact_icons_match_colored_reference() -> None:
    template = read_text("_includes/author-profile.html")
    css = read_text("assets/css/main.scss")

    required_template_snippets = [
        'fa-map-marker-alt" aria-hidden="true"></i> {{ author.location }}',
        'fa-envelope" aria-hidden="true"></i> Email',
        'fa-github" aria-hidden="true"></i> GitHub',
        'ai-google-scholar ai-fw" aria-hidden="true"></i> Google Scholar',
        'fa-weixin" aria-hidden="true"></i> WeChat',
        'fa-book-open" aria-hidden="true"></i> Rednote',
    ]

    for snippet in required_template_snippets:
        assert snippet in template

    required_css_snippets = [
        ".author__urls .fa-map-marker-alt {\n    color: #ef4444;",
        ".author__urls .fa-envelope {\n    color: #64748b;",
        ".author__urls .fa-github {\n    color: #111827;",
        ".author__urls .ai-google-scholar {\n    color: #2563eb;",
        ".author__urls .fa-weixin {\n    color: #07c160;",
        ".author__urls .fa-book-open {\n    color: #ef4444;",
    ]

    for snippet in required_css_snippets:
        assert snippet in css


def test_public_site_does_not_render_template_author_content() -> None:
    public_files = [
        "_config.yml",
        "_pages/about.md",
        "_layouts/default.html",
        "_includes/head/custom.html",
        "assets/css/main.scss",
        "README.md",
    ]

    banned = [
        "Weidong Tang",
        "Xidian University",
        "wdtang0705",
        "NH9USaYAAAAJ",
        "mapmyvisitors",
        "Alibaba Group",
        "TeleAI",
    ]

    for relative_path in public_files:
        text = read_text(relative_path)
        for snippet in banned:
            assert snippet not in text, f"{snippet} found in {relative_path}"
