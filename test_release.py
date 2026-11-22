import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BANNED = ('Carbon', 'sweep', 'floor', 'andoff', 'ws/', 'package', '[MODEL]', 'filing', 'inventions', 'Release 2', 'qualification-basis')


class Release(unittest.TestCase):
    def setUp(self):
        with open(HERE / 'inventory.csv', newline='') as handle:
            self.rows = list(csv.DictReader(handle))

    def test_counts(self):
        outcomes = [r['outcome'] for r in self.rows]
        self.assertEqual(len(self.rows), 21)
        self.assertEqual((outcomes.count('failed'), outcomes.count('intact'), outcomes.count('not cycled'), outcomes.count('TBD')), (7, 10, 2, 2))

    def test_every_row_has_a_source_and_a_score(self):
        for row in self.rows:
            self.assertTrue(any(u.startswith('http') for u in row['sources'].split()), row['well'])
            self.assertIn(row['completeness'], list('012345'))

    def test_json_and_csv_agree(self):
        self.assertEqual(json.loads((HERE / 'inventory.json').read_text()), self.rows)

    def test_link_check_record_has_no_failure(self):
        record = json.loads((HERE / 'link-check.json').read_text())
        self.assertEqual(record['failed'], [] if isinstance(record['failed'], list) else 0)

    def test_dataset_description_names_every_column(self):
        dataset = json.loads((HERE / 'dataset.jsonld').read_text())
        self.assertEqual(dataset['variableMeasured'], list(self.rows[0]))
        self.assertEqual(dataset['@type'], 'Dataset')

    def test_synthesis_is_literature_only(self):
        for name in ('MECHANISMS.md', 'README.md', 'llms.txt'):
            text = (HERE / name).read_text()
            for word in BANNED:
                self.assertNotIn(word, text, (name, word))
        self.assertGreaterEqual((HERE / 'MECHANISMS.md').read_text().count('**confirmed'), 4)


if __name__ == '__main__':
    unittest.main()
