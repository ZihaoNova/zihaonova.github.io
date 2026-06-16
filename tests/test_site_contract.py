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


def test_site_identity_config_matches_current_public_profile() -> None:
    config = read_text("_config.yml")

    required_snippets = [
        'title                    : "Zihao Huang"',
        'repository               : "ZihaoNova/ZihaoNova.github.io"',
        'url                      : "https://zihaonova.github.io"',
        'name             : "Zihao Huang"',
        'bio              : "Faculty member (Lecturer), Zhejiang A&F University"',
        'location         : "Hangzhou, Zhejiang, China"',
        'employer         : "Zhejiang A&F University"',
        'uri              : "https://zihaonova.github.io"',
        'github           : "ZihaoNova"',
        'rednote          : "/images/RedNote.jpg"',
    ]

    for snippet in required_snippets:
        assert snippet in config

    assert "GOOGLE_SCHOLAR_ID" not in config


def test_homepage_content_is_clean_utf8_profile() -> None:
    homepage = read_text("_pages/about.md")

    required_text = [
        "Zihao Huang (黄子豪)",
        "Faculty member (Lecturer)",
        "Zhejiang A&F University",
        "University of Eastern Finland",
        "# 🔥 News",
        "# 📝 Publications",
        "# 🚀 Selected Projects",
        "# 🏢 Experience",
        "# 📖 Educations",
        "# 🎖 Honors and Awards",
        "# 🎙 Invited Talks",
        "# 💬 Services",
        "土地利用/覆盖变化及其对森林碳收支影响研究综述",
        "遥感学报",
        "整合多光谱指数与LandTrendr算法的时间序列林龄估算方法",
        "Forest age estimation from disturbance and recovery",
        "LUCC simulation under climate and human effects",
        "Forest carbon storage and NEP projection",
    ]

    for text in required_text:
        assert text in homepage

    banned_mojibake = [
        "榛勫瓙",
        "馃敟",
        "涓闄",
        "鏁村悎澶氬厜",
        "閬ユ劅瀛︽姤",
    ]
    for snippet in banned_mojibake:
        assert snippet not in homepage

    assert "2021.11.60" not in homepage
    assert "I Published" not in homepage
    assert homepage.count("class='paper-box'") == 3


def test_navigation_anchors_match_homepage_sections() -> None:
    navigation = read_text("_data/navigation.yml")
    homepage = read_text("_pages/about.md")

    required_pairs = [
        ('title: "About Me"', 'url: "/#about-me"', "id='about-me'"),
        ('title: "News"', 'url: "/#-news"', "id='-news'"),
        ('title: "Publications"', 'url: "/#-publications"', "id='-publications'"),
        ('title: "Experience"', 'url: "/#-experience"', "id='-experience'"),
        ('title: "Educations"', 'url: "/#-educations"', "id='-educations'"),
        ('title: "Honors and Awards"', 'url: "/#-honors-and-awards"', "id='-honors-and-awards'"),
        ('title: "Invited Talks"', 'url: "/#-invited-talks"', "id='-invited-talks'"),
        ('title: "Services"', 'url: "/#-services"', "id='-services'"),
    ]

    for title, nav_url, anchor in required_pairs:
        assert title in navigation
        assert nav_url in navigation
        assert anchor in homepage

    assert "Teaching" not in navigation


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


def test_custom_visual_assets_and_head_resources_exist() -> None:
    css = read_text("assets/css/main.scss")
    site_css = read_text("assets/css/site.css")
    head = read_text("_includes/head.html")
    custom_head = read_text("_includes/head/custom.html")

    required_assets = [
        "images/site-icon.svg",
        "images/browserconfig.xml",
        "images/land-cover-simulation.svg",
        "images/raster-validation.svg",
        "images/dask-pipeline.svg",
        "images/RedNote.jpg",
    ]

    for relative_path in required_assets:
        assert (ROOT / relative_path).exists(), relative_path

    assert "Zihao Huang custom polish" in css
    assert ".site-footer" in css
    assert 'href="{{ \'/assets/css/site.css\' | relative_url }}?v={{ site.time | date: \'%s\' }}"' in head
    assert ".paper-box" in site_css
    assert "linear-gradient(135deg, #2563eb, #0f766e)" in css
    assert 'href="images/site.webmanifest"' in custom_head
    assert 'href="images/site-icon.svg"' in custom_head
    assert 'content="images/browserconfig.xml?v=M44lzPylqQ"' in custom_head


def test_sidebar_contact_icons_match_current_config() -> None:
    template = read_text("_includes/author-profile.html")
    css = read_text("assets/css/site.css")

    required_fontawesome_snippets = [
        '@font-face {\n  font-family: "Font Awesome 5 Free";',
        'src: url("../fonts/fa-solid-900.woff2") format("woff2");',
        '@font-face {\n  font-family: "Font Awesome 5 Brands";',
        'src: url("../fonts/fa-brands-400.woff2") format("woff2");',
        ".fa {\n  font-family: \"Font Awesome 5 Free\";",
        ".fas {\n  font-family: \"Font Awesome 5 Free\";",
        ".fab {\n  font-family: \"Font Awesome 5 Brands\";",
        ".fa-fw {\n  text-align: center;",
        '.fa-researchgate:before {\n  content: "\\f4f8";\n}',
        '.fa-graduation-cap:before {\n  content: "\\f19d";\n}',
    ]
    for snippet in required_fontawesome_snippets:
        assert snippet in css

    required_template_snippets = [
        '{% include base_path %}',
        'author.avatar contains "://"',
        '{% if site.description and site.description != "" %}',
        'fa fa-fw fa-map-marker-alt" aria-hidden="true"></i>{{ author.location }}',
        'fa-building" aria-hidden="true"></i>{{ author.employer }}',
        'fa-link" aria-hidden="true"></i>Website',
        'fa-envelope" aria-hidden="true"></i>Email',
        'fa-researchgate" aria-hidden="true"></i>ResearchGate',
        'fa-github" aria-hidden="true"></i>GitHub',
        'fa-graduation-cap" aria-hidden="true"></i>Google Scholar',
        'ai-orcid ai-fw" aria-hidden="true"></i>ORCID',
        'fa-book-open" aria-hidden="true"></i>Rednote',
    ]
    for snippet in required_template_snippets:
        assert snippet in template

    required_css_snippets = [
        ".author__urls .fa-map-marker-alt {\n  color: #ef4444;\n}",
        ".author__urls .fa-envelope {\n  color: #64748b;\n}",
        ".author__urls .fa-link {\n  color: #2563eb;\n}",
        ".author__urls .fa-github {\n  color: #111827;\n}",
        ".author__urls .fa-researchgate {\n  color: #00a99d;\n}",
        ".author__urls .fa-graduation-cap {\n  color: #475569;\n}",
        ".author__urls .ai-orcid {\n  color: #a6ce39;\n}",
        ".author__urls .fa-book-open {\n  color: #ef4444;\n}",
    ]
    for snippet in required_css_snippets:
        assert snippet in css


def test_masthead_uses_styled_zihao_brand() -> None:
    masthead = read_text("_includes/masthead.html")
    css = read_text("assets/css/site.css")

    assert ">Homepage<" not in masthead
    assert '<a class="masthead__brand-name" href="#about-me">Zihao Huang</a>' in masthead
    assert ".masthead__brand-name {" in css
    assert 'font-family: "Palatino Linotype", "Book Antiqua", Georgia, serif;' in css
    assert "font-style: italic;" in css


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
