import unittest
from pathlib import Path

from wordscraper import word_scrape

TEST_DOC = Path("./test_doc.docx")


class TestWordscraper(unittest.TestCase):
    def test_word_scrape(self):
        self.assertEqual(
            word_scrape(TEST_DOC),
            r"""Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Duis autem vel eum iriure dolor. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Ut wisi enim ad minim. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. BILD. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. TABELLE. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. FORM. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. GEGENDERTE AUSDRÜCKE: Bauarbeiter*innen, Ärzt*innen, Lesb*innen. SONDERZEICHENPARADE: [!][@][#][$][%][^][&][*][_][-][=][+][|][\][;][:][’][”][,][<][.][>][/][?][~]. UMLAUTE: ÄaÜüÖö. FORMATIERUNG: Fetter Text, Kursiver Text, Durch- und unterstrichener Text. EMAILADRESSE: max.mustermann@gmail.com. """,  # noqa: E501
        )


if __name__ == "__main__":
    unittest.main()
