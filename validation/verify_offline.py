"""Execute the notebook offline and check reconstructed evidence, never model behavior."""
import contextlib
import hashlib
import io
import json
import os
import platform
import socket
from importlib.metadata import version
from pathlib import Path

import pandas as pd
from IPython.display import display

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
NOTEBOOK = ROOT / 'notebooks/airline_refund_llm_evaluation.ipynb'
nb = json.loads(NOTEBOOK.read_text())
scope = {'__name__': '__main__'}
network_attempts = []

def block_network(*args, **kwargs):
    network_attempts.append(True)
    raise RuntimeError('Network disabled during offline verification')

original_connect = socket.socket.connect
original_connection = socket.create_connection
socket.socket.connect = block_network
socket.create_connection = block_network
try:
    count = 0
    for index, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        count += 1
        # The live block must stay disabled even if a previous cell is edited.
        if index >= 11:
            assert scope['RUN_LIVE'] is False
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(compile(''.join(cell['source']), f'notebook-cell-{index}', 'exec'), scope)
        cell['execution_count'] = count
        cell['outputs'] = ([{'output_type': 'stream', 'name': 'stdout',
                             'text': output.getvalue().splitlines(True)}]
                           if output.getvalue() else [])
finally:
    socket.socket.connect = original_connect
    socket.create_connection = original_connection

assert not network_attempts
assert scope['RUN_LIVE'] is False
expected = ['Minimal', 'Policy', 'Policy + examples']
summary = scope['summary']
assert summary['prompt'].tolist() == expected
assert summary['correct'].tolist() == [7, 10, 10]
assert summary['total'].tolist() == [13, 13, 13]
assert summary['invalid'].tolist() == [0, 0, 0]
assert not summary['injection_case_correct'].any()
assert summary['live_format_check'].isna().all()
cases = scope['case_data']
assert cases['case_id'].tolist() == [f'C{i:02}' for i in range(1, 14)]
# Independently read against the fictional first-matching-rule policy.
assert cases['expected_decision'].tolist() == [
    'REFUND', 'DENY', 'REFUND', 'CREDIT', 'DENY', 'DENY', 'ESCALATE',
    'ESCALATE', 'DENY', 'ESCALATE', 'REFUND', 'DENY', 'DENY']
saved = scope['saved_predictions']
assert len(saved) == 39
assert not saved.duplicated(['prompt', 'case_id']).any()
assert set(saved['prediction']) <= scope['LABELS']
assert set(saved['prompt']) == set(expected)
for _, group in saved.groupby('prompt'):
    assert set(group['case_id']) == set(cases['case_id'])
history = pd.read_csv(ROOT / 'reports/original_summary.csv')
for prompt, correct in zip(expected, [7, 10, 10]):
    row = history[(history.reported_model == 'gpt-3.5-turbo') & (history.prompt == prompt)]
    assert len(row) == 1 and int(row.iloc[0]['correct']) == correct

parse = scope['parse_predictions']
strict = scope['follows_exact_format']
ids = ['C01', 'C02']
checks = [
    parse('C01,REFUND\nC01,DENY\nC02,CREDIT', ids) == {'C01':'INVALID','C02':'CREDIT'},
    parse('C01,REFUND', ids)['C02'] == 'INVALID',
    parse('C01,UNKNOWN\nC02,DENY', ids)['C01'] == 'INVALID',
    parse('C99,REFUND\nC01,DENY\nC02,CREDIT', ids) == {'C01':'DENY','C02':'CREDIT'},
    parse('- C01: refund because of cancellation\nC02; deny', ids) == {'C01':'REFUND','C02':'DENY'},
    strict('C01,REFUND\nC02,DENY', ids),
    not strict('C02,DENY\nC01,REFUND', ids),
    not strict('C01,REFUND\nC01,DENY', ids),
    not strict('C01,REFUND\nC02,DENY\nExplanation', ids),
    strict(' c01,refund \n\n c02,deny ', ids),
]
assert all(checks)
# Confirm answer-key values are not added by the case formatter.
assert scope['case_text'] == '\n'.join(f'{r.case_id}: {r.text}' for r in cases.itertuples())
summary.to_csv(ROOT / 'reports/offline_verified_summary.csv', index=False)
scope['results'].to_csv(ROOT / 'reports/offline_verified_predictions.csv', index=False)
record = {
    'validation_date': '2026-10-22', 'python': platform.python_version(),
    'pandas': version('pandas'), 'ipython': version('ipython'),
    'executed_code_cells': count, 'network_attempts': len(network_attempts),
    'live_api_calls': 0, 'parser_edge_checks_passed': len(checks),
    'inputs_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [
        'data/synthetic_cases.csv', 'reports/reconstructed_predictions.csv', 'reports/original_summary.csv']},
    'scope': 'Sequential Python execution of all notebook code cells, reconstructed-record scoring and parser checks; no Jupyter kernel or live model verification.',
    'separate_4o_mini_result': '12/13 remains historical only; per-case records for this comparison are not bundled.',
    'strict_format_caveat': 'Blank lines and outer whitespace are ignored and labels are case-insensitive; original raw-response format remains unverified.',
}
(ROOT/'reports/offline_validation.json').write_text(json.dumps(record, indent=2)+'\n')
nb['metadata']['language_info']['version'] = platform.python_version()
NOTEBOOK.write_text(json.dumps(nb, indent=1, ensure_ascii=False)+'\n')
print(summary.to_string(index=False))
print(f'Executed {count} code cells; {len(checks)} parser checks passed; zero network attempts.')
