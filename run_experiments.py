#!/usr/bin/env python3
"""Finite toy experiments. A: manual Python replay. B: declared minimal model.

No LLM calls, no source modifications, no native-Julia validation claim.
"""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import random
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
COMMIT = 'a51c99e26c3534b68bffbc9c81697886f6097feb'
SOURCE_BLOBS = {
    'HohoConsciousness.jl': 'e46453372f86680447851a0f7f973bc4a095eda3',
    'HohoConsciousnessCore.jl': 'e85918cd3329baf741a5a24718b9fd12f6664c3f',
    'ImaginaryMode.jl': '23144925440e28f0c2e2e690a374a4dbb79aa43d',
}


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source_manifest():
    entries = []
    for name, expected in SOURCE_BLOBS.items():
        p = ROOT / 'sources' / 'hoho' / 'src' / name
        b = p.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        if blob != expected:
            raise RuntimeError(f'Source changed: {name}')
        entries.append(dict(path=str(p.relative_to(ROOT)), git_blob=blob,
                            sha256=sha256(p), bytes=len(b),
                            url=f'https://github.com/0syamuixinyamu1/hoho-consciousness-engine/blob/{COMMIT}/src/{name}'))
    return entries


def write_csv(name, rows):
    if not rows:
        raise ValueError('Empty result set')
    with (OUT / name).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def clamp01(x):
    return max(0.0, min(1.0, float(x)))


def pressure_score(anger, rejection, authority, social_cost):
    # Exact coefficients in the pinned ImaginaryMode.jl, not a memory summary.
    return clamp01(0.40 * clamp01(anger) + 0.25 * clamp01(rejection)
                   + 0.15 * clamp01(authority) + 0.20 * clamp01(social_cost))


def statement(value):
    return f'value={int(value)}'


def replay_a(policy, initial, hypothesis, pressure, evidence, contradiction):
    """Explicit translation of the relevant finite, bounded Julia pathways."""
    belief, response = initial, statement(initial)
    imaginary_active = apparent = collapse_returned = False
    score = pressure_score(pressure, pressure, pressure, pressure)
    support = clamp01(0.60 * clamp01(evidence) + 0.40 * clamp01(contradiction))
    # apply_external_compliance / respond_to_pressure!: score >= 0.60.
    if policy in ('external_only', 'imaginary_only') and score >= 0.60:
        response = statement(hypothesis)  # Caller-supplied apparent_response.
        apparent = True
        imaginary_active = policy == 'imaginary_only'
    elif policy == 'evidence_revision':
        # enter_imaginary! can be called without pressure; it does not revise belief.
        imaginary_active = True
        if support >= 0.75:
            belief = hypothesis
            imaginary_active = False
            collapse_returned = True
        response = statement(belief)  # Experiment adapter, not an engine renderer.
    elif policy not in ('unchanged', 'external_only', 'imaginary_only'):
        raise ValueError(policy)
    return dict(pressure_score=score, support=support, final_belief=belief,
                response=response, apparent_correction=apparent,
                compliance_internal_revision=False if policy in ('external_only', 'imaginary_only') else None,
                imaginary_active=imaginary_active, collapse_returned=collapse_returned,
                actual_state_change=belief != initial)


def experiment_a():
    rows = []
    policies = ['unchanged', 'external_only', 'imaginary_only', 'evidence_revision']
    pressures = [0.0, 0.2, 0.4, 0.599999, 0.6, 0.8, 1.0]
    strengths = [i / 10 for i in range(11)]
    for p, e, c, ref, initial, hyp, policy in itertools.product(
            pressures, strengths, strengths, [0, 1], [0, 1], [0, 1], policies):
        result = replay_a(policy, initial, hyp, p, e, c)
        rows.append(dict(policy=policy, pressure_input=p, evidence=e,
                         contradiction=c, reference=ref, initial_belief=initial,
                         hypothesis=hyp, **result,
                         output_score=int(result['response'] == statement(ref)),
                         internal_score=int(result['final_belief'] == ref),
                         pressure_free_probe_score=int(statement(result['final_belief']) == statement(ref))))
    write_csv('a_trials.csv', rows)
    # Orthogonal pressure grid: prevents treating equal-pressure sweeps as a weight test.
    pressure_rows = []
    for a, r, auth, cost in itertools.product([0, .25, .5, .75, 1], repeat=4):
        score = pressure_score(a, r, auth, cost)
        pressure_rows.append(dict(anger=a, rejection=r, authority=auth, social_cost=cost,
                                  pressure_score=score, apparent_correction=score >= .6,
                                  initial_belief=0, final_belief=0))
    write_csv('a_pressure_grid.csv', pressure_rows)
    summary = []
    for policy in policies:
        subset = [r for r in rows if r['policy'] == policy
                  and r['initial_belief'] != r['reference'] and r['hypothesis'] == r['reference']]
        high = [r for r in subset if r['pressure_input'] >= .6]
        summary.append(dict(policy=policy, initially_wrong_correct_hypothesis_cases=len(subset),
                            high_pressure_cases=len(high),
                            high_pressure_output_correct=sum(r['output_score'] for r in high),
                            high_pressure_internal_correct=sum(r['internal_score'] for r in high),
                            high_pressure_apparent_only=sum(r['output_score'] == 1 and r['internal_score'] == 0 for r in high)))
    write_csv('a_summary.csv', summary)
    return rows, summary


def mean_or_none(xs):
    return sum(xs) / len(xs) if xs else None


def offer(beliefs, topic, value, is_reference, policy, tol):
    before = beliefs.get(topic)
    agreement = None if before is None else 1.0 - abs(value - before)
    if policy == 'gated':
        accepted = before is None or abs(value - before) <= tol
    elif policy == 'accept_all':
        accepted = True
    elif policy == 'reference_only':
        accepted = is_reference
    else:
        raise ValueError(policy)
    if accepted:
        beliefs[topic] = value
    return accepted, agreement, before


def fixture(name, steps=80):
    if name == 'frozen':
        return 0.0, 1.0, [[(0.0, False), (1.0, True)] for _ in range(steps)]
    if name == 'bridge':
        return 0.0, 1.0, [[(min(t / 40, 1.0), t >= 40)] for t in range(1, steps + 1)]
    if name == 'drift_away':
        return .4, 1.0, [[(.4 * math.exp(-t / 10), False), (1.0, True)] for t in range(1, steps + 1)]
    if name == 'oscillation':
        return .5, .5, [[(.45 if t % 2 else .55, False)] for t in range(1, steps + 1)]
    if name == 'all_rejected':
        return 0.0, 1.0, [[(1.0, True)] for _ in range(steps)]
    raise ValueError(name)


def run_b(name, initial, reference, schedule, policy, tol, seed=-1):
    beliefs = {'known': initial}
    rows, events = [], []
    rejected_total = reference_rejected_total = 0
    for t, batch in enumerate(schedule, 1):
        before_tick = beliefs['known']
        accepted_scores, all_scores = [], []
        n_accept = n_reference = n_reference_accept = 0
        for i, (value, is_reference) in enumerate(batch):
            accepted, agreement, before = offer(beliefs, 'known', value, is_reference, policy, tol)
            n_accept += int(accepted)
            n_reference += int(is_reference)
            n_reference_accept += int(accepted and is_reference)
            if agreement is not None:
                all_scores.append(agreement)
                if accepted:
                    accepted_scores.append(agreement)
            events.append(dict(fixture=name, seed=seed, policy=policy, tol=tol, step=t,
                               input_index=i, value=value, is_reference=is_reference,
                               belief_before=before, accepted=accepted,
                               agreement_before_update=agreement, belief_after=beliefs['known']))
        rejected_total += len(batch) - n_accept
        reference_rejected_total += n_reference - n_reference_accept
        rows.append(dict(fixture=name, seed=seed, policy=policy, tol=tol, step=t,
                         initial_belief=initial, reference=reference, belief=beliefs['known'],
                         state_delta=abs(beliefs['known'] - before_tick),
                         accepted_agreement=mean_or_none(accepted_scores),
                         all_input_agreement=mean_or_none(all_scores),
                         coverage=n_accept / len(batch), reference_error=abs(beliefs['known'] - reference),
                         reference_acceptance=n_reference_accept / n_reference if n_reference else None,
                         rejected_total=rejected_total, reference_rejected_total=reference_rejected_total))
    return rows, events


def experiment_b():
    rows, events, sensitivity = [], [], []
    tolerances = [0.0, .01, .024, .026, .05, .11, .25, 1.0]
    policies = ['gated', 'accept_all', 'reference_only']
    for name, tol, policy in itertools.product(
            ['frozen', 'bridge', 'drift_away', 'oscillation', 'all_rejected'], tolerances, policies):
        initial, ref, schedule = fixture(name)
        rs, es = run_b(name, initial, ref, schedule, policy, tol)
        rows.extend(rs)
        events.extend(es)
    for seed in range(30):
        rng = random.Random(seed)
        initial = rng.uniform(.05, .4)
        schedule = []
        for _ in range(80):
            batch = [(initial, False), (1.0, True)]
            rng.shuffle(batch)
            schedule.append(batch)
        for tol, policy in itertools.product(tolerances, policies):
            rs, _ = run_b('frozen_random_order', initial, 1.0, schedule, policy, tol, seed)
            tail = rs[-20:]
            sensitivity.append(dict(seed=seed, tol=tol, policy=policy, initial_belief=initial,
                                    final_error=rs[-1]['reference_error'],
                                    tail_error_mean=mean_or_none([r['reference_error'] for r in tail]),
                                    tail_coverage_mean=mean_or_none([r['coverage'] for r in tail]),
                                    reference_rejected_total=rs[-1]['reference_rejected_total']))
    write_csv('b_trajectories.csv', rows)
    write_csv('b_input_events.csv', events)
    write_csv('b_seed_sensitivity.csv', sensitivity)
    write_csv('b_endpoints.csv', [r for r in rows if r['step'] == 80])
    return rows, events, sensitivity


def validate(a, b, sensitivity):
    checks = []
    def check(name, truth, details):
        checks.append(dict(name=name, passed=bool(truth), details=details))
    def bpath(name, tol=.05, policy='gated'):
        return [r for r in b if r['fixture'] == name and r['tol'] == tol and r['policy'] == policy]
    observed_a = [r for r in a if r['pressure_input'] == 1 and r['evidence'] == 1
                  and r['contradiction'] == 1 and r['initial_belief'] == 0
                  and r['reference'] == 1 and r['hypothesis'] == 1]
    groups = {r['policy']: r for r in observed_a}
    check('same_correct_output_different_internal_state',
          groups['external_only']['response'] == groups['evidence_revision']['response']
          and groups['external_only']['internal_score'] == 0
          and groups['evidence_revision']['internal_score'] == 1, groups)
    pure = [r for r in a if r['policy'] in ('external_only', 'imaginary_only')]
    check('pressure_routes_preserve_real_belief_in_grid',
          all(r['initial_belief'] == r['final_belief'] for r in pure), {'cases': len(pure)})
    weak = [r for r in a if r['policy'] == 'evidence_revision' and r['support'] < .75]
    check('weak_evidence_does_not_revise_in_grid',
          all(not r['actual_state_change'] for r in weak), {'cases': len(weak)})
    false_updates = [r for r in a if r['policy'] == 'evidence_revision' and r['support'] >= .75
                     and r['initial_belief'] == r['reference'] and r['hypothesis'] != r['reference']]
    check('strong_wrong_hypothesis_can_worsen_belief',
          bool(false_updates) and all(r['internal_score'] == 0 for r in false_updates),
          {'cases': len(false_updates), 'interpretation': 'Supplied strength is not independently verified truth.'})
    unchanged_collapses = [r for r in a if r['collapse_returned'] and not r['actual_state_change']]
    check('collapse_flag_is_not_state_delta', len(unchanged_collapses) > 0, {'cases': len(unchanged_collapses)})
    frozen = bpath('frozen')
    check('fixed_belief_fixed_reference_error_is_constant',
          all(r['reference_error'] == 1 for r in frozen)
          and frozen[-1]['reference_rejected_total'] == 80, frozen[-1])
    bridge = bpath('bridge')
    check('small_steps_escape_initial_belief_without_override',
          bridge[39]['belief'] == 1 and bridge[-1]['reference_error'] == 0, bridge[39])
    drift = bpath('drift_away')
    check('conditional_agreement_and_reference_error_can_both_increase',
          drift[-1]['accepted_agreement'] > drift[0]['accepted_agreement']
          and drift[-1]['reference_error'] > drift[0]['reference_error']
          and drift[-1]['reference_error'] > abs(.4 - 1), {'first': drift[0], 'last': drift[-1]})
    oscillation = bpath('oscillation', tol=.11)
    check('bounded_step_gate_does_not_imply_convergence',
          len({r['belief'] for r in oscillation[-20:]}) == 2,
          {'tail_beliefs': sorted({r['belief'] for r in oscillation[-20:]}),
           'scope': 'Constructed periodic input; finite run plus explicit period-two transition.'})
    rejected = bpath('all_rejected')
    check('empty_observation_is_na_not_perfect_score',
          all(r['accepted_agreement'] is None and r['coverage'] == 0 for r in rejected), rejected[-1])
    anchor = []
    for first in (0.0, 1.0):
        beliefs = {}
        accepted, agreement, _ = offer(beliefs, 'new', first, first == 1, 'gated', .05)
        for _ in range(80):
            offer(beliefs, 'new', 1-first, 1-first == 1, 'gated', .05)
        anchor.append(dict(first_value=first, first_accepted=accepted, first_agreement=agreement,
                           final_belief=beliefs['new'], reference=1.0, error=abs(beliefs['new']-1)))
    check('unknown_topic_is_admitted_and_initial_order_matters',
          all(r['first_accepted'] for r in anchor) and [r['final_belief'] for r in anchor] == [0, 1], anchor)
    selected = [r for r in sensitivity if r['policy'] == 'gated' and r['tol'] == .05]
    check('frozen_result_survives_30_input_orders_and_initializations',
          len(selected) == 30 and all(math.isclose(r['final_error'],1-r['initial_belief'])
                                    and r['reference_rejected_total'] == 80 for r in selected),
          {'seeds': len(selected)})
    return checks


def main():
    OUT.mkdir(exist_ok=True)
    sources_before = source_manifest()
    a, a_summary = experiment_a()
    b, b_events, sensitivity = experiment_b()
    checks = validate(a, b, sensitivity)
    if sources_before != source_manifest():
        raise RuntimeError('Original source snapshot changed during the run')
    summary = dict(execution='Python source replay / declared minimal model',
                   native_julia_executed=False, python=platform.python_version(),
                   source_commit=COMMIT, sources=sources_before,
                   source_integrity_verified=True, protocol_sha256=sha256(ROOT/'PROTOCOL_JA.md'),
                   runner_sha256=sha256(Path(__file__)),
                   a_trials=len(a), a_pressure_grid=625, b_trajectory_rows=len(b),
                   b_input_events=len(b_events), b_seed_sensitivity_runs=len(sensitivity),
                   a_summary=a_summary, checks_passed=sum(c['passed'] for c in checks),
                   checks_total=len(checks), checks=checks,
                   data_sha256={p.name:sha256(p) for p in sorted(OUT.glob('*.csv'))})
    (OUT/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:summary[k] for k in ['execution','native_julia_executed','a_trials',
          'a_pressure_grid','b_trajectory_rows','b_input_events','b_seed_sensitivity_runs','checks_passed','checks_total']}, indent=2))
    for c in checks:
        print(('PASS ' if c['passed'] else 'FAIL ')+c['name'])
    if not all(c['passed'] for c in checks):
        sys.exit(1)


if __name__ == '__main__':
    main()
