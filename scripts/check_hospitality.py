#!/usr/bin/env python3
"""M-011 exact source representation check; never reads ROM data."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
base = '22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc'
old = subprocess.check_output(['git', '-C', str(root), 'show', base + ':src/Base_Stats.c'], text=True)
expected = old
for species in ('SINISTCHA', 'SINISTCHA_MASTERPIECE'):
    start = expected.index('[SPECIES_' + species + ']')
    end = expected.index('\n\t}', start)
    block = expected[start:end]
    assert '.ability1 = ABILITY_WEAKARMOR,' in block
    assert '.hiddenAbility = ABILITY_HEATPROOF,' in block
    expected = expected[:start] + block.replace('.ability1 = ABILITY_WEAKARMOR,', '.ability1 = ABILITY_HOSPITALITY,') + expected[end:]
assert (root / 'src/Base_Stats.c').read_text() == expected
abilities = (root / 'include/abilities.h').read_text()
assert '#define ABILITY_HOSPITALITY ABILITY_HEALER' in abilities
assert '#define ABILITY_HEALER 0x6C' in abilities
print('M-011 DPE exact two primary slots, hidden Heatproof preserved, byte identity 0x6C PASS')
