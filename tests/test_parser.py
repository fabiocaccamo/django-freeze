from django.test import TestCase

from freeze.parser import replace_base_url


class ParserTestCase(TestCase):
    """
    This class describes a parser test case.
    """

    def test_replace_base_url_with_base_url_none(self):
        text_result = replace_base_url(
            text="""<img src="/media/images/logo.jpg">""",
            base_url=None,
        )
        self.assertEqual(
            text_result,
            """<img src="/media/images/logo.jpg">""",
        )

    def test_replace_base_url_on_media_url(self):
        text_result = replace_base_url(
            text="""<img src="/media/images/logo.jpg">""",
            base_url="https://django-freeze.com/",
        )
        self.assertEqual(
            text_result,
            """<img src="https://django-freeze.com/media/images/logo.jpg">""",
        )

    def test_replace_base_url_on_static_url(self):
        text_result = replace_base_url(
            text="""<img src="/static/images/logo.jpg">""",
            base_url="https://django-freeze.com/",
        )
        self.assertEqual(
            text_result,
            """<img src="https://django-freeze.com/static/images/logo.jpg">""",
        )

    def test_replace_base_url_on_meta_http_equiv_refresh(self):
        text_result = replace_base_url(
            text="""<meta http-equiv="refresh" content="0; url=/en/">""",
            base_url="https://django-freeze.com/",
        )
        self.assertEqual(
            text_result,
            """<meta http-equiv="refresh" content="0; url=https://django-freeze.com/en/">""",
        )

    def test_replace_base_url_on_sitemap(self):
        sitemap_text = """
            <urlset>
                <url>
                    <loc>/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>/about/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>/projects/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>/contacts/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
            </urlset>
        """.strip()
        sitemap_result = replace_base_url(
            text=sitemap_text,
            base_url="https://django-freeze.com/",
        )
        expected_sitemap_result = """
            <urlset>
                <url>
                    <loc>https://django-freeze.com/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>https://django-freeze.com/about/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>https://django-freeze.com/projects/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
                <url>
                    <loc>https://django-freeze.com/contacts/</loc>
                    <changefreq>weekly</changefreq>
                    <priority>0.7</priority>
                </url>
            </urlset>
        """.strip()
        self.assertEqual(sitemap_result, expected_sitemap_result)
