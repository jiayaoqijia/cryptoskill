import importlib.util
import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import sync_sources as sync

SKILL = b'---\nname: swap\ndescription: Swap tokens\n---\n# Swap\n'


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dest = self.root / 'skills/defi/acme-swap'
        self.dest.mkdir(parents=True)
        (self.dest / 'SKILL.md').write_bytes(SKILL)
        (self.dest / 'SOURCE.md').write_text('# Source\nhttps://github.com/acme/skills\n')

    def tearDown(self):
        self.temp.cleanup()

    def test_reference_only_update_and_owned_deletion(self):
        (self.dest / 'old.txt').write_text('obsolete')
        (self.dest / 'local.txt').write_text('local')
        (self.dest / 'TRUST.md').write_text('review')
        old = {'files': {'SKILL.md': '', 'old.txt': ''}}
        changed, hashes = sync.install_bundle(self.dest, {'SKILL.md': SKILL, 'references/new.md': b'new'}, old)
        self.assertTrue(changed)
        self.assertFalse((self.dest / 'old.txt').exists())
        self.assertEqual((self.dest / 'local.txt').read_text(), 'local')
        self.assertEqual((self.dest / 'TRUST.md').read_text(), 'review')
        self.assertEqual(len(hashes['SKILL.md']), 64)
        changed, _ = sync.install_bundle(self.dest, {'SKILL.md': SKILL, 'references/new.md': b'new'}, {'files': hashes})
        self.assertFalse(changed)

    def test_legacy_skill_filename_is_normalized(self):
        (self.dest / 'SKILL.md').unlink()
        (self.dest / 'skill.md').write_bytes(SKILL)
        changed, _ = sync.install_bundle(self.dest, {'SKILL.md': SKILL}, {})
        self.assertTrue(changed)
        self.assertIn('SKILL.md', [p.name for p in self.dest.iterdir()])
        self.assertNotIn('skill.md', [p.name for p in self.dest.iterdir()])

    def test_blocked_update_does_not_touch_existing_files(self):
        def reject(_):
            raise ValueError('blocked')
        with self.assertRaises(ValueError):
            sync.install_bundle(self.dest, {'SKILL.md': b'changed'}, {}, check=reject)
        self.assertEqual((self.dest / 'SKILL.md').read_bytes(), SKILL)

    def test_dry_run_is_read_only(self):
        changed, _ = sync.install_bundle(self.dest, {'SKILL.md': b'changed'}, {}, dry_run=True)
        self.assertTrue(changed)
        self.assertEqual((self.dest / 'SKILL.md').read_bytes(), SKILL)

    def test_rejects_path_traversal_and_metadata_overwrite(self):
        for name in ('../outside', '/outside', 'x/../../outside', 'x\\y', 'SOURCE.md', 'source.md'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                sync.install_bundle(self.dest, {'SKILL.md': SKILL, name: b'bad'}, {})
        self.assertFalse((self.root / 'outside').exists())

    def test_nested_bundle_includes_libraries_and_license(self):
        result = sync.bundle_files({'skills/swap/SKILL.md': SKILL, 'skills/swap/lib/api.py': b'code',
                                    'LICENSE': b'license', 'unrelated.txt': b'no'}, 'skills/swap/SKILL.md')
        self.assertEqual(set(result), {'SKILL.md', 'lib/api.py', 'LICENSE'})

    def test_ambiguous_match_is_not_guessed(self):
        entry = {'source': '', 'body': b'placeholder', 'slug': 'generic'}
        with self.assertRaises(ValueError):
            sync.select_skill(entry, {'a/SKILL.md': SKILL, 'b/SKILL.md': SKILL}, {})

    def test_recorded_path_is_not_silently_remapped(self):
        with self.assertRaises(ValueError):
            sync.select_skill({}, {'new/SKILL.md': SKILL}, {'path': 'removed/SKILL.md'})

    def test_archive_traversal_rejected(self):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            item = tarfile.TarInfo('repo/../../escape')
            item.size = 3
            archive.addfile(item, io.BytesIO(b'bad'))
        with self.assertRaises(ValueError):
            sync.archive_files(stream.getvalue())

    def test_archive_skips_machine_local_files(self):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for path, body in {'repo/SKILL.md': SKILL, 'repo/.DS_Store': b'junk',
                               'repo/.claude/settings.local.json': b'{}'}.items():
                item = tarfile.TarInfo(path)
                item.size = len(body)
                archive.addfile(item, io.BytesIO(body))
        self.assertEqual(set(sync.archive_files(stream.getvalue())), {'SKILL.md'})

    def run_sync(self, files, **kwargs):
        with patch.object(sync, 'dirty_skills', return_value=set()), \
             patch.object(sync, 'github_bundle', return_value=('a' * 40, files)), \
             patch.object(sync, 'security_check'):
            return sync.sync_registry(self.root, official_repos=[{'org': 'acme', 'repo': 'skills',
                'category': 'defi', 'prefix': 'acme-'}], skip_clawhub=True, **kwargs)

    def test_new_skill_is_installed_and_pinned_before_cleanup(self):
        report = self.run_sync({'swap/SKILL.md': SKILL, 'stake/SKILL.md': SKILL.replace(b'swap', b'stake')})
        self.assertEqual(report['summary']['added'], 1)
        self.assertTrue((self.root / 'skills/defi/acme-stake/SKILL.md').exists())
        lock = json.loads((self.root / 'scripts/source-lock.json').read_text())
        self.assertEqual(lock['skills']['defi/acme-stake']['revision'], 'a' * 40)
        self.assertIn('https://github.com/acme/skills', (self.root / 'skills/defi/acme-stake/SOURCE.md').read_text())

    def test_run_dry_run_does_not_write_lock_or_report(self):
        self.run_sync({'swap/SKILL.md': SKILL}, dry_run=True)
        self.assertFalse((self.root / 'scripts/source-lock.json').exists())
        self.assertFalse((self.root / 'docs/sync-report.json').exists())

    def test_failure_never_advances_pin(self):
        with patch.object(sync, 'dirty_skills', return_value=set()), \
             patch.object(sync, 'github_bundle', side_effect=ValueError('timeout')):
            report = sync.sync_registry(self.root, skip_clawhub=True)
        self.assertEqual(report['summary']['unavailable'], 1)
        self.assertFalse((self.root / 'scripts/source-lock.json').exists())

    def test_local_changes_are_preserved(self):
        with patch.object(sync, 'dirty_skills', return_value={'defi/acme-swap'}), \
             patch.object(sync, 'github_bundle', return_value=('b' * 40, {'SKILL.md': b'changed'})):
            report = sync.sync_registry(self.root, skip_clawhub=True)
        self.assertEqual(report['summary']['local_changes'], 1)
        self.assertEqual((self.dest / 'SKILL.md').read_bytes(), SKILL)

    def test_multi_repo_selection_preserves_community_classification_and_report(self):
        configs = [{'org': 'acme', 'repo': 'skills', 'category': 'defi', 'prefix': 'acme-'},
                   {'org': 'beta', 'repo': 'skills', 'category': 'analytics', 'prefix': 'beta-',
                    'official': False, 'evidence_url': 'https://github.com/beta/skills'},
                   {'org': 'unselected', 'repo': 'skills', 'category': 'defi', 'prefix': 'no-'}]
        with patch.object(sync, 'dirty_skills', return_value=set()), \
             patch.object(sync, 'github_bundle', return_value=('a' * 40, {'SKILL.md': SKILL})) as fetch, \
             patch.object(sync, 'security_check'):
            report = sync.sync_registry(self.root, configs, only_repo=['acme/skills', 'beta/skills'],
                                        skip_clawhub=True, report_path='docs/selected.json')
        self.assertEqual({call.args[0] for call in fetch.call_args_list}, {'acme/skills', 'beta/skills'})
        self.assertEqual(report['summary']['added'], 1)
        self.assertIn('**Classification**: COMMUNITY', (self.root / 'skills/analytics/beta-swap/SOURCE.md').read_text())
        self.assertTrue((self.root / 'docs/selected.json').exists())
        self.assertFalse((self.root / 'docs/sync-report.json').exists())

    def test_clawhub_owner_mismatch_stops_download(self):
        with patch.object(sync, 'fetch', return_value=b'{"owner":{"handle":"imposter"}}') as fetch:
            with self.assertRaisesRegex(ValueError, 'publisher'):
                sync.clawhub_bundle({'source': 'https://clawhub.ai/skills/alice/swap'})
        self.assertEqual(fetch.call_count, 1)

    def test_cached_revision_requires_matching_local_hashes(self):
        _, hashes = sync.install_bundle(self.dest, {'SKILL.md': SKILL}, {})
        entry = {'key': 'defi/acme-swap', 'destination': self.dest}
        state = {'repositories': {'acme/skills': 'abc'}, 'skills': {
            entry['key']: {'revision': 'abc', 'files': hashes}}}
        self.assertEqual(sync.cached_revision([entry], state, 'acme/skills'), 'abc')
        (self.dest / 'SKILL.md').write_bytes(b'changed')
        self.assertIsNone(sync.cached_revision([entry], state, 'acme/skills'))

    def test_symlink_in_bundle_is_not_silently_dropped(self):
        files = sync.ArchiveFiles()
        files['swap/SKILL.md'] = SKILL
        files.rejected.add('swap/lib')
        with self.assertRaisesRegex(ValueError, 'links'):
            sync.bundle_files(files, 'swap/SKILL.md')

    def test_empty_skill_is_not_installed(self):
        with self.assertRaisesRegex(ValueError, 'empty'):
            sync.install_bundle(self.dest, {'SKILL.md': b''}, {})

    def test_executable_modes_are_preserved(self):
        bundle = sync.ArchiveFiles()
        bundle.update({'SKILL.md': SKILL, 'scripts/run.sh': b'#!/bin/sh\necho ok\n'})
        bundle.modes['scripts/run.sh'] = 0o755
        sync.install_bundle(self.dest, bundle, {})
        self.assertTrue((self.dest / 'scripts/run.sh').stat().st_mode & 0o111)
        bundle.modes['scripts/run.sh'] = 0o644
        changed, _ = sync.install_bundle(self.dest, bundle, {})
        self.assertTrue(changed)
        self.assertFalse((self.dest / 'scripts/run.sh').stat().st_mode & 0o111)


class CatalogTests(unittest.TestCase):
    def test_related_skills_link_across_categories(self):
        spec = importlib.util.spec_from_file_location('pages', sync.ROOT / 'scripts/generate-pages.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        current = {'name': 'acme-official-swap', 'category': 'defi', 'author': 'acme'}
        sibling = {'name': 'acme-official-wallet', 'category': 'wallets', 'author': 'acme'}
        html = module._related_strip(current, [current, sibling], {})
        self.assertIn('href="../wallets/acme-official-wallet.html"', html)

    def test_frontmatter_and_classification(self):
        spec = importlib.util.spec_from_file_location('catalog', sync.ROOT / 'scripts/update-catalog.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'SKILL.md'
            path.write_text('---\nname: sample\ndescription: >-\n  First line\n  second line\ntags: [defi, swap]\n---\n')
            self.assertEqual(module.parse_skill_md_frontmatter(path)['description'], 'First line second line')
            path.write_text('Source: https://github.com/some/unofficial\n- **Classification**: COMMUNITY\n')
            self.assertEqual(module.classify_source(path), 'community')


if __name__ == '__main__':
    unittest.main()
