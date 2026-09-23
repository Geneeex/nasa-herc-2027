#!/usr/bin/env python3
"""Reproduce proposal arithmetic without claiming hardware validation.

Python 3.10+; standard library only. Run from any directory.
The current aluminium-chassis installed mass remains unreconciled.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MM_PER_INCH = Decimal('25.4')
KG_PER_LB = Decimal('0.45359237')
KM_PER_MILE = Decimal('1.609344')


def number(value, name='value', *, allow_zero=False):
    """Reject missing, boolean, negative and nonfinite physical inputs."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f'{name} must be a finite number')
    n = float(value)
    if not math.isfinite(n) or (n < 0 if allow_zero else n <= 0):
        raise ValueError(f'{name} must be finite and ' + ('nonnegative' if allow_zero else 'positive'))
    return n


def fraction(value, name='infill'):
    n = number(value, name, allow_zero=True)
    if n > 1:
        raise ValueError(f'{name} must be between 0 and 1, not a percentage')
    return n


def mm_to_inches(mm):
    number(mm, 'millimetres', allow_zero=True)
    return Decimal(str(mm)) / MM_PER_INCH


def lb_to_kg(lb):
    number(lb, 'pounds', allow_zero=True)
    return Decimal(str(lb)) * KG_PER_LB


def nominal_wh(voltage, capacity_mah):
    number(voltage, 'nominal voltage')
    number(capacity_mah, 'capacity')
    return Decimal(str(voltage)) * Decimal(str(capacity_mah)) / 1000


def speed_kmh(diameter_mm, wheel_rpm):
    d = number(diameter_mm, 'wheel diameter')
    rpm = number(wheel_rpm, 'wheel RPM', allow_zero=True)
    return math.pi * (d / 1000) * rpm * 60 / 1000


def rpm_for_speed(diameter_mm, kmh):
    d = number(diameter_mm, 'wheel diameter')
    speed = number(kmh, 'speed', allow_zero=True)
    return speed * 1_000_000 / (math.pi * d * 60)


def annular_volume_cm3(outer_mm, inner_mm, width_mm):
    outer = number(outer_mm, 'outer diameter')
    inner = number(inner_mm, 'inner diameter', allow_zero=True)
    width = number(width_mm, 'width')
    if inner >= outer:
        raise ValueError('Inner diameter must be smaller than outer diameter')
    # Diameter-to-area factor 1/4 and mm3-to-cm3 factor 1/1000.
    return math.pi * (outer**2 - inner**2) * width / 4000


def polymer_mass_kg(solid_cm3, core_cm3, infill, density_g_cm3):
    number(solid_cm3, 'solid volume', allow_zero=True)
    number(core_cm3, 'core volume', allow_zero=True)
    fraction(infill)
    number(density_g_cm3, 'density')
    return (Decimal(str(solid_cm3)) + Decimal(str(core_cm3)) * Decimal(str(infill))) * Decimal(str(density_g_cm3)) / 1000


def wheel_mass(parameters, count=4):
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise ValueError('Wheel count must be a positive integer')
    p = parameters
    width = number(p['width_mm'], 'wheel width')
    diameter = number(p['diameter_mm'], 'complete wheel diameter')
    barrel_outer = number(p['rim_barrel_outer_diameter_mm'], 'rim diameter')
    carcass_outer = number(p['tyre_carcass_outer_diameter_mm'], 'carcass diameter')
    carcass_inner = number(p['tyre_carcass_inner_diameter_mm'], 'tyre inside diameter')
    skin = number(p['tyre_skin_mm'], 'tyre skin')
    if not barrel_outer <= carcass_inner < carcass_outer <= diameter:
        raise ValueError('Rim, tyre carcass and complete wheel diameters are inconsistent')
    barrel = annular_volume_cm3(barrel_outer, p['rim_barrel_inner_diameter_mm'], width)
    rim_mass = float(polymer_mass_kg(barrel + number(p['rim_extra_solid_cm3'], allow_zero=True), p['rim_extra_core_cm3'], p['rim_core_infill_fraction'], p['petg_density_g_cm3']))
    envelope = annular_volume_cm3(carcass_outer, carcass_inner, width)
    core_outer, core_inner, core_width = carcass_outer - 2 * skin, carcass_inner + 2 * skin, width - 2 * skin
    core = annular_volume_cm3(core_outer, core_inner, core_width)
    skins = envelope - core
    tyre_volume = skins + fraction(p['tyre_core_infill_fraction']) * core + number(p['tread_solid_cm3'], allow_zero=True)
    tyre_mass = float(polymer_mass_kg(tyre_volume, 0, 0, p['tpu_density_g_cm3']))
    coupler_mass = number(p['legacy_hex_coupler_mass_g'], 'coupler mass') / 1000
    one = rim_mass + tyre_mass + coupler_mass
    source_displayed_one = sum(Decimal(str(x)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) for x in (rim_mass, tyre_mass, coupler_mass))
    return {
        'barrel_volume_cm3':barrel, 'rim_polymer_volume_cm3':barrel + p['rim_extra_solid_cm3'] + p['rim_core_infill_fraction'] * p['rim_extra_core_cm3'],
        'carcass_envelope_cm3':envelope, 'carcass_core_cm3':core, 'carcass_skins_cm3':skins,
        'carcass_core_outer_diameter_mm':core_outer, 'carcass_core_inner_diameter_mm':core_inner, 'carcass_core_width_mm':core_width,
        'filled_tyre_and_tread_cm3':tyre_volume, 'rim_kg':rim_mass, 'tyre_kg':tyre_mass, 'legacy_hex_coupler_kg':coupler_mass,
        'one_wheel_kg':one, 'all_wheels_kg':count * one, 'count':count,
        'sum_of_source_displayed_parts_one_wheel_kg':float(source_displayed_one),
        'sum_of_source_displayed_parts_all_wheels_kg':float(count * source_displayed_one)
    }


def ledger_totals(ledger):
    seen = set()
    totals = {'D':Decimal(0), 'T':Decimal(0)}
    audited = []
    for row in ledger['rows']:
        item_id = row['id']
        if item_id in seen or len(item_id) != 3 or item_id[0] not in totals or not item_id[1:].isdigit():
            raise ValueError(f'Duplicate or invalid ledger ID: {item_id}')
        seen.add(item_id)
        qty = row['quantity_in_legacy_group_A']
        if isinstance(qty, bool) or not isinstance(qty, int) or qty < 0:
            raise ValueError(f'{item_id}: installed quantity must be a nonnegative integer')
        unit = row['unit_mass_g']
        if qty:
            number(unit, f'{item_id} unit mass')
            subtotal = qty * Decimal(str(unit))
        else:
            if unit is not None:
                number(unit, f'{item_id} unit mass', allow_zero=True)
            subtotal = Decimal(0)
        totals[item_id[0]] += subtotal
        audited.append({'id':item_id, 'name':row['name'], 'quantity':qty, 'unit_mass_g':unit, 'legacy_subtotal_g':float(subtotal), 'basis':row['basis'], 'note':row['source_note']})
    return {'drive_g':float(totals['D']), 'task_g':float(totals['T']), 'group_A_kg':float(sum(totals.values()) / 1000), 'rows':audited}


def carry(value):
    return Decimal(str(value)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)


def build_results(inputs, ledger):
    if inputs['schema_version'] != 1:
        raise ValueError('Unsupported input schema')
    current = inputs['current_design']
    wheel = current['wheel']
    span = (number(wheel['diameter_mm']) - number(wheel['rim_lip_outer_diameter_mm'])) / 2
    if not math.isclose(span, number(wheel['rim_lip_to_tread_peak_mm']), abs_tol=1e-9):
        raise ValueError('Rim-to-tread span does not agree with the supplied diameters')
    if current['mass']['verified_current_installed_mass_kg'] is not None:
        raise ValueError('Reconcile the aluminium body and current coupling ledger before recording a verified current mass')
    dims = [{'name':name, 'mm':value, 'inches':float(mm_to_inches(value))} for name,value in [
        ('Overall wheel diameter',wheel['diameter_mm']),('Overall wheel width',wheel['width_mm']),('Rim lip outer diameter',wheel['rim_lip_outer_diameter_mm']),('Rim lip to tread peak',span),
        ('Rover length',current['rover']['length_mm']),('Rover width',current['rover']['width_mm']),('Ground to camera top, excluding antenna',current['rover']['height_to_camera_mm'])]]
    mph_limit = Decimal(str(current['speed']['competition_limit_mph']))
    number(mph_limit, 'mph ceiling')
    limit_kmh = mph_limit * KM_PER_MILE
    target = number(current['speed']['engineering_target_kmh'], 'engineering speed target')
    speeds = [{'wheel_rpm':rpm,'kmh':speed_kmh(wheel['diameter_mm'],rpm),'mph':speed_kmh(wheel['diameter_mm'],rpm)/float(KM_PER_MILE)} for rpm in current['speed']['wheel_rpm_scenarios']]
    batteries = []
    for battery in current['batteries']:
        batteries.append({**battery, 'nominal_energy_Wh':float(nominal_wh(battery['nominal_voltage_V'],battery['capacity_mAh']))})
    a = ledger_totals(ledger)
    old = wheel_mass(inputs['legacy_analytical_wheel'], wheel['count'])
    new_parameters = {**inputs['legacy_analytical_wheel'],**inputs['updated_analytical_wheel']}
    revised = wheel_mass(new_parameters, wheel['count'])
    body = inputs['legacy_printed_body']
    body_parts = [{'name':p['name'], 'solid_cm3':p['solid_cm3'],'core_cm3':p['core_cm3'], 'mass_kg':float(polymer_mass_kg(p['solid_cm3'],p['core_cm3'],body['core_infill_fraction'],body['density_g_cm3']))} for p in body['parts']]
    c = sum(polymer_mass_kg(p['solid_cm3'],p['core_cm3'],body['core_infill_fraction'],body['density_g_cm3']) for p in body['parts'])
    a_carry, c_carry = carry(a['group_A_kg']), carry(c)
    new_carry = a_carry + carry(revised['all_wheels_kg']) + c_carry
    old_carry = a_carry + carry(old['all_wheels_kg']) + c_carry
    mass = current['mass']
    estimate = Decimal(str(mass['documented_estimate_kg']))
    target_kg = lb_to_kg(mass['scoring_target_lb'])
    return {
        'team':inputs['team'],'calculation_status':'Reproduced analytical arithmetic only; no hardware test or current mass validation.',
        'current_verified_installed_mass_kg':None,'hardware_test_results_included':False,
        'dimensions':dims,'rim_to_tread_span_mm':span,
        'speed':{'scenarios':speeds,'mph_ceiling':float(mph_limit),'equivalent_kmh_ceiling':float(limit_kmh),'wheel_rpm_at_mph_ceiling':rpm_for_speed(wheel['diameter_mm'],float(limit_kmh)),'engineering_target_kmh':target,'wheel_rpm_at_engineering_target':rpm_for_speed(wheel['diameter_mm'],target)},
        'batteries':batteries,'total_nominal_stored_energy_Wh':float(sum(nominal_wh(b['nominal_voltage_V'],b['capacity_mAh']) for b in current['batteries'])),
        'legacy_installed_equipment':a,'legacy_wheel_185mm_rim':old,'updated_source_wheel_188mm_rim':revised,
        'legacy_printed_body':{'parts':body_parts,'group_C_kg':float(c)},
        'mass_audit':{'group_A_carry_kg':float(a_carry),'updated_group_B_carry_kg':float(carry(revised['all_wheels_kg'])),'legacy_group_C_carry_kg':float(c_carry),
            'pre_wheel_update_carry_total_kg':float(old_carry),'updated_source_carry_total_kg':float(new_carry),'updated_source_unrounded_total_kg':a['group_A_kg']+revised['all_wheels_kg']+float(c),
            'source_documented_estimate_kg':float(estimate),'source_documented_estimate_lb':float(estimate/KG_PER_LB),'carry_total_matches_source':new_carry==estimate,
            'scoring_target_kg':float(target_kg),'source_estimate_gap_above_target_kg':float(estimate-target_kg),'source_estimate_gap_above_target_lb':float(estimate/KG_PER_LB-Decimal(str(mass['scoring_target_lb']))),
            'handbook_maximum_kg':float(lb_to_kg(mass['handbook_maximum_lb'])),'updated_wheel_delta_kg':revised['all_wheels_kg']-old['all_wheels_kg'],
            'current_configuration_reconciled':False}
    }


def render_report(r):
    a = r['mass_audit']
    speed = r['speed']
    w = r['updated_source_wheel_188mm_rim']
    lines = ['# Calculation results', '', '**NASA HERC 2027 TEAM BANGLADESH**', '',
        '**Current assembled mass is not yet verified.** We reproduce the source arithmetic below. The source mass document still uses a printed CF-PLA chassis and brass hex couplers; the current design specifies a 6061-T6 aluminium chassis and clamping couplings. A correct sum does not resolve that design difference.', '',
        '## Dimensions and unit conversions', '', 'We use 25.4 mm per inch. These are proposal dimensions, not manufactured measurements.', '', '| Dimension | mm | in |','|---|---:|---:|']
    for d in r['dimensions']:
        lines.append(f"| {d['name']} | {d['mm']:g} | {d['inches']:.4f} |")
    lines += ['', 'Rim lip to tread peak = (215 - 188) / 2 = 13.5 mm. This is the radial span including tread, not a solid TPU wall. The 421 mm camera height excludes the antenna; it is not the complete excursion-ready height.', '',
        '## Speed arithmetic', '', 'No-slip speed in km/h = pi x wheel diameter in mm x wheel RPM x 60 / 1,000,000.', '', '| Wheel RPM scenario | km/h | mph |','|---:|---:|---:|']
    for s in speed['scenarios']:
        lines.append(f"| {s['wheel_rpm']:g} | {s['kmh']:.6f} | {s['mph']:.6f} |")
    lines += ['',f"5 mph is exactly {speed['equivalent_kmh_ceiling']:.5f} km/h; at 215 mm diameter this corresponds to {speed['wheel_rpm_at_mph_ceiling']:.6f} wheel RPM. Our stricter 8 km/h target corresponds to {speed['wheel_rpm_at_engineering_target']:.6f} wheel RPM.", '',
        'The 190 RPM case is a scenario, not a measured or guaranteed loaded speed. Neither RPM figure defines a validated transmitter setting. We must measure full-charge forward/reverse speed, mixed steering, startup behaviour and downhill stopping, allowing for measurement uncertainty and tyre deflection.', '',
        '## Battery nominal energy', '', 'Nominal Wh = nominal V x mAh / 1000.', '', '| Separate battery | Nominal V | Capacity (mAh) | Nominal Wh |','|---|---:|---:|---:|']
    for b in r['batteries']:
        lines.append(f"| {b['system'].title()} | {b['nominal_voltage_V']:g} | {b['capacity_mAh']:g} | {b['nominal_energy_Wh']:.2f} |")
    lines += ['',f"Combined nominal stored energy: 55.50 + 24.42 = {r['total_nominal_stored_energy_Wh']:.2f} Wh. The packs remain electrically separate. This sum is not a shared available energy pool or a runtime estimate. We do not use the 12.6 V full-charge voltage to calculate nominal Wh. Runtime requires measured loads, conversion losses, cutoff behaviour and reserve through results review.", '',
        '## Updated analytical wheel in the source mass document', '',
        'The Google Doc read on 23 September 2026 confirms the following simplified model. These are analytical planning volumes and densities, not CAD mesh material volumes or slicer results. The model treats the 188 mm outer lip as the barrel and tyre-seat diameter; final fit geometry must be checked.', '',
        '| Calculation | Result |','|---|---:|',
        f"| Rim barrel: pi x (188 squared - 182 squared) x 90 / 4000 | {w['barrel_volume_cm3']:.6f} cm3 |",
        f"| PETG volume: barrel + 55 solid + 0.375 x 45 core | {w['rim_polymer_volume_cm3']:.6f} cm3 |",
        f"| PETG mass: volume x 1.27 / 1000 | {w['rim_kg']:.9f} kg |",
        f"| Tyre envelope: pi x (205 squared - 188 squared) x 90 / 4000 | {w['carcass_envelope_cm3']:.6f} cm3 |",
        f"| Tyre core: pi x (200.2 squared - 192.8 squared) x 85.2 / 4000 | {w['carcass_core_cm3']:.6f} cm3 |",
        f"| Solid skins: envelope - core | {w['carcass_skins_cm3']:.6f} cm3 |",
        f"| TPU volume: skins + 0.15 x core + 60 solid tread | {w['filled_tyre_and_tread_cm3']:.6f} cm3 |",
        f"| TPU mass: volume x 1.21 / 1000 | {w['tyre_kg']:.9f} kg |",
        f"| Historical brass hex coupler allowance | {w['legacy_hex_coupler_kg']:.4f} kg |",
        f"| One analytical wheel including historical coupler | {w['one_wheel_kg']:.9f} kg |",
        f"| Four analytical wheels including historical couplers | {w['all_wheels_kg']:.9f} kg |", '',
        'The 2.4 mm skins set core diameters to 205 - 2 x 2.4 = 200.2 mm and 188 + 2 x 2.4 = 192.8 mm, and width to 90 - 2 x 2.4 = 85.2 mm. The raised tread height is (215 - 205) / 2 = 5 mm. The 55 cm3 solid and 45 cm3 core rim allowances and 60 cm3 tread allowance still need final CAD/slicer reconciliation.', '',
        f"The source adds its displayed values: 0.2906 + 0.4439 + 0.0186 = {w['sum_of_source_displayed_parts_one_wheel_kg']:.4f} kg per wheel; four give {w['sum_of_source_displayed_parts_all_wheels_kg']:.4f} kg, carried as 3.012 kg. We also retain unrounded results so rounding is visible. Bearings, spindles and motors were counted in legacy Group A; they are not added again here.", '',
        '## Historical installed-equipment and body audit', '',
        'We reproduce all 64 ledger rows, including exclusions, in [legacy-installed-mass.csv](legacy-installed-mass.csv). The source notes distinguish allocations, references and unresolved masses. Supplier links are retained as historical provenance, not new verification.', '',
        f"Legacy drive equipment: {r['legacy_installed_equipment']['drive_g']:.3f} g. Legacy task equipment: {r['legacy_installed_equipment']['task_g']:.3f} g. Group A = {r['legacy_installed_equipment']['group_A_kg']:.6f} kg, carried as {a['group_A_carry_kg']:.3f} kg.", '',
        'Legacy body formula: mass in kg = 1.21 x (solid cm3 + 0.375 x core cm3) / 1000.', '',
        '| Legacy printed body part | Solid cm3 | Core cm3 | kg |','|---|---:|---:|---:|']
    for p in r['legacy_printed_body']['parts']:
        lines.append(f"| {p['name']} | {p['solid_cm3']:.6f} | {p['core_cm3']:.6f} | {p['mass_kg']:.9f} |")
    lines += ['',f"Legacy Group C is {r['legacy_printed_body']['group_C_kg']:.10f} kg, carried as {a['legacy_group_C_carry_kg']:.3f} kg. These printed chassis volumes must not be reused for the aluminium chassis.", '',
        '| Source accounting | kg |','|---|---:|',f"| Group A carry | {a['group_A_carry_kg']:.3f} |",f"| Updated Group B carry | {a['updated_group_B_carry_kg']:.3f} |",f"| Legacy Group C carry | {a['legacy_group_C_carry_kg']:.3f} |",f"| Source carry total | {a['updated_source_carry_total_kg']:.3f} |",f"| Same analytical scenario without intermediate rounding | {a['updated_source_unrounded_total_kg']:.9f} |", '',
        f"The earlier 185 mm rim calculation carried {a['pre_wheel_update_carry_total_kg']:.3f} kg. Revising only its wheel dimensions changes the four-wheel analytical mass by {a['updated_wheel_delta_kg']:.9f} kg and reproduces the source's {a['source_documented_estimate_kg']:.3f} kg total. This reconciles the arithmetic, not the current material and hardware configuration.", '',
        '## Documented estimate and scoring target', '',
        f"20 lb x 0.45359237 = {a['scoring_target_kg']:.7f} kg. The source's 10.919 kg estimate equals {a['source_documented_estimate_lb']:.6f} lb.", '',
        f"Source estimate minus target = 10.919 - {a['scoring_target_kg']:.7f} = {a['source_estimate_gap_above_target_kg']:.7f} kg ({a['source_estimate_gap_above_target_lb']:.6f} lb). The 60 lb maximum converts to {a['handbook_maximum_kg']:.7f} kg. These comparisons do not establish current rover compliance.", '',
        '## What remains before we can report a current mass', '',
        '- Replace the printed-chassis mass model with the retained aluminium sections, sheets, joints and actual suspension/carrier parts. Purchased stock and offcuts are not installed mass.',
        '- Reconcile the current clamping couplings, spindle bearings, flanges and retention parts with the older hex-coupler accounting; count each fitted part once.',
        '- Confirm final materials, print geometry and slicer settings for rims, tyres, covers and enclosures, then weigh representative finished parts.',
        '- Replace planning allocations and unresolved supplier net weights with measured installed quantities and masses.',
        '- Weigh the full excursion-ready assembly with both batteries and all fitted equipment. Keep the scale record and configuration alongside the result.', '',
        'We exclude the other archived PA12/aluminium/TPU wheel mass report because it describes different materials. We do not blend that mass into the PETG/TPU design.', '',
        'Generated from [inputs.json](inputs.json), [the source excerpt](../data/source-mass-calculation-excerpt.json), [the legacy ledger](../data/legacy-installed-mass-ledger.json) and [provenance](../data/calculation-provenance.json). Unit conversions use exact international inch, foot, pound and mile factors; pi-based geometry uses Python double precision. Extra digits expose the arithmetic and do not imply measurement accuracy.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs',type=Path,default=HERE/'inputs.json')
    parser.add_argument('--ledger',type=Path,default=ROOT/'data/legacy-installed-mass-ledger.json')
    parser.add_argument('--output-dir',type=Path,default=HERE)
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text(encoding='utf-8-sig'))
    ledger = json.loads(args.ledger.read_text(encoding='utf-8-sig'))
    results = build_results(inputs,ledger)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'results.json').write_text(json.dumps(results,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    (args.output_dir/'results.md').write_text(render_report(results),encoding='utf-8')
    with (args.output_dir/'legacy-installed-mass.csv').open('w',newline='',encoding='utf-8') as file:
        rows = results['legacy_installed_equipment']['rows']
        writer = csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Generated results.json, results.md and legacy-installed-mass.csv. Hardware validation: not performed.')


if __name__ == '__main__':
    main()
