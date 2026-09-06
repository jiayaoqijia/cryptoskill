import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('score_validation', SCRIPTS / 'score-skills.py')
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

from hosted_sources import check_hosted_sources


class MnemonicDetectionTests(unittest.TestCase):
    def test_normal_documentation_is_not_a_seed(self):
        for text in (
            'whether the user wants any advanced options for the platform they chose',
            'hours order placed after the close queues for the next open instead',
            'name copycats and sizing slippage and gas are both outside this skill',
        ):
            with self.subTest(text=text):
                self.assertFalse(score.contains_mnemonic(text))

    def test_valid_public_bip39_vector_is_detected(self):
        # Public test vector from trezor/python-mnemonic; no private wallet.
        phrase = 'legal winner thank year wave sausage worth useful legal winner thank yellow'
        self.assertTrue(score.contains_mnemonic(phrase))
        self.assertTrue(score.contains_mnemonic(phrase.upper()))
        self.assertTrue(score.contains_mnemonic('example below ' + phrase + ' end'))

    def test_labelled_damaged_seed_is_still_flagged(self):
        phrase = 'legal winner thank year wave sausage worth useful legal winner thank zoo'
        self.assertTrue(score.contains_mnemonic('seed_phrase = "' + phrase + '"'))

    def test_known_placeholder_is_exempt(self):
        self.assertFalse(score.contains_mnemonic('abandon ' * 11 + 'about'))

    def test_repeated_word_seed_is_not_skipped_for_low_diversity(self):
        phrase = score._BIP39.to_mnemonic(bytes([255]) * 32)
        self.assertTrue(score.contains_mnemonic(phrase))

    def test_gate_blocks_seed_without_returning_secret_text(self):
        phrase = score._BIP39.to_mnemonic(bytes([127]) * 16)
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'SKILL.md').write_text('seed_phrase = "' + phrase + '"')
            _, _, passed, reasons = score.compute_security_score(Path(folder))
        self.assertFalse(passed)
        self.assertTrue(reasons)
        self.assertNotIn(phrase, str(reasons))


class HostedSourceTests(unittest.TestCase):
    def source(self):
        return {'slug': 'test', 'project': 'Test', 'endpoint': 'https://agent.example.com/mcp',
                'documentation': 'https://example.com/docs'}

    def test_documents_endpoint_without_connecting_to_it(self):
        source = self.source()
        with patch('hosted_sources.read_documentation', return_value=source['endpoint'].encode()) as fetch:
            report = check_hosted_sources([source], dry_run=True)
        fetch.assert_called_once_with(source['documentation'])
        self.assertEqual(report['sources'][0]['status'], 'documented')

    def test_missing_endpoint_requires_review(self):
        with patch('hosted_sources.read_documentation', return_value=b'No integration here'):
            report = check_hosted_sources([self.source()], dry_run=True)
        self.assertEqual(report['sources'][0]['status'], 'needs_review')

    def test_endpoint_split_across_inline_spans(self):
        body = b'<p><span>https://</span><span>agent.example.com/mcp</span></p>'
        with patch('hosted_sources.read_documentation', return_value=body):
            report = check_hosted_sources([self.source()], dry_run=True)
        self.assertEqual(report['sources'][0]['status'], 'documented')


class HostedManifestTests(unittest.TestCase):
    def test_robinhood_is_recognized_as_a_custodial_executor(self):
        spec = importlib.util.spec_from_file_location('cap_validation', SCRIPTS / 'extract-capabilities.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = SCRIPTS.parent / 'skills/mcp-servers/robinhood-trading-mcp'
        caps, _, model, _, _ = module.extract_capabilities(path)
        self.assertTrue(caps['can_move_funds'])
        self.assertTrue(caps['requires_hosted_operator'])
        self.assertEqual(model, 'custodial_executor')
