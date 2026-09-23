"""Arithmetic checks only. Passing these is not a rover hardware test."""
import copy
import importlib.util
import json
import math
from decimal import Decimal
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('rover_calculations', ROOT/'calculations/calculate.py')
calc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(calc)
INPUTS = json.loads((ROOT/'calculations/inputs.json').read_text(encoding='utf-8-sig'))
LEDGER = json.loads((ROOT/'data/legacy-installed-mass-ledger.json').read_text(encoding='utf-8-sig'))


class CalculationTests(unittest.TestCase):
    def test_exact_unit_conversions(self):
        self.assertEqual(calc.mm_to_inches(25.4), Decimal(1))
        self.assertEqual(calc.lb_to_kg(20), Decimal('9.07184740'))
        self.assertEqual(calc.lb_to_kg(60), Decimal('27.21554220'))
        self.assertEqual((215 - 188)/2, 13.5)
        self.assertAlmostEqual(float(calc.mm_to_inches(215)), 8.464566929133858, places=12)

    def test_documented_speed_scenarios(self):
        self.assertAlmostEqual(calc.speed_kmh(215,200),8.105309046261665,places=12)
        self.assertAlmostEqual(calc.speed_kmh(215,190),7.700043593948582,places=12)
        self.assertEqual(calc.speed_kmh(215,0),0)
        self.assertAlmostEqual(calc.speed_kmh(215,100)*2,calc.speed_kmh(215,200),places=12)

    def test_distinct_speed_limits_and_inverse(self):
        five_mph = Decimal(5)*calc.KM_PER_MILE
        self.assertEqual(five_mph,Decimal('8.046720'))
        rpm = calc.rpm_for_speed(215,8)
        self.assertAlmostEqual(rpm,197.40147980390122,places=10)
        self.assertAlmostEqual(calc.speed_kmh(215,rpm),8,places=12)
        self.assertGreater(calc.rpm_for_speed(215,float(five_mph)),rpm)
        self.assertGreater(calc.speed_kmh(215,200),float(five_mph))

    def test_nominal_energy_not_full_charge_energy(self):
        self.assertEqual(calc.nominal_wh(11.1,5000),Decimal('55.5'))
        self.assertEqual(calc.nominal_wh(11.1,2200),Decimal('24.42'))
        result=calc.build_results(INPUTS,LEDGER)
        self.assertEqual(result['total_nominal_stored_energy_Wh'],79.92)
        self.assertNotIn('runtime_minutes',result)

    def test_annulus_unit_scale_and_solid_cylinder(self):
        self.assertAlmostEqual(calc.annular_volume_cm3(20,10,10),0.75*math.pi)
        self.assertAlmostEqual(calc.annular_volume_cm3(20,0,10),math.pi)
        self.assertAlmostEqual(calc.annular_volume_cm3(40,20,20),8*calc.annular_volume_cm3(20,10,10))

    def test_infill_never_reduces_solid_skin(self):
        self.assertEqual(calc.polymer_mass_kg(10,20,0,1.2),Decimal('0.012'))
        self.assertEqual(calc.polymer_mass_kg(10,20,1,1.2),Decimal('0.036'))
        self.assertEqual(calc.polymer_mass_kg(10,20,0.5,1.2),Decimal('0.024'))
        with self.assertRaises(ValueError): calc.polymer_mass_kg(10,20,37.5,1.2)

    def test_invalid_physical_inputs_are_rejected(self):
        for invalid in (-1,float('nan'),float('inf'),None,True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError): calc.speed_kmh(invalid,200)
        with self.assertRaises(ValueError): calc.annular_volume_cm3(20,20,10)
        with self.assertRaises(ValueError): calc.annular_volume_cm3(20,21,10)
        with self.assertRaises(ValueError): calc.annular_volume_cm3(20,10,0)
        with self.assertRaises(ValueError): calc.nominal_wh(11.1,0)

    def test_wheel_source_reproduction(self):
        params={**INPUTS['legacy_analytical_wheel'],**INPUTS['updated_analytical_wheel']}
        wheel=calc.wheel_mass(params)
        self.assertAlmostEqual(wheel['rim_kg'],0.29057289236944894,places=12)
        self.assertAlmostEqual(wheel['tyre_kg'],0.4438738665043019,places=12)
        self.assertAlmostEqual(wheel['all_wheels_kg'],3.0121870354950033,places=12)
        self.assertAlmostEqual(wheel['carcass_core_inner_diameter_mm'],192.8,places=12)
        self.assertEqual(wheel['sum_of_source_displayed_parts_one_wheel_kg'],0.7531)
        self.assertEqual(wheel['sum_of_source_displayed_parts_all_wheels_kg'],3.0124)
        self.assertLess(wheel['all_wheels_kg'],calc.wheel_mass(INPUTS['legacy_analytical_wheel'])['all_wheels_kg'])

    def test_overlapping_tyre_skins_are_rejected(self):
        p=copy.deepcopy(INPUTS['legacy_analytical_wheel'])
        p['tyre_skin_mm']=10
        with self.assertRaises(ValueError): calc.wheel_mass(p)
        with self.assertRaises(ValueError): calc.wheel_mass(INPUTS['legacy_analytical_wheel'],0)

    def test_full_legacy_ledger_and_exclusions(self):
        a=calc.ledger_totals(LEDGER)
        self.assertEqual(len(a['rows']),64)
        self.assertEqual(a['drive_g'],3001.1)
        self.assertEqual(a['task_g'],1458.706)
        self.assertEqual(a['group_A_kg'],4.459806)
        rows={r['id']:r for r in a['rows']}
        self.assertEqual(rows['D08']['quantity'],4)
        self.assertEqual(rows['D08']['legacy_subtotal_g'],1160)
        self.assertEqual(rows['D01']['legacy_subtotal_g'],0)
        self.assertEqual(rows['D07']['legacy_subtotal_g'],0)
        self.assertEqual(rows['T14']['legacy_subtotal_g'],0)

    def test_unresolved_installed_mass_is_not_silently_zero(self):
        ledger=copy.deepcopy(LEDGER)
        ledger['rows'][0]['quantity_in_legacy_group_A']=1
        with self.assertRaises(ValueError): calc.ledger_totals(ledger)

    def test_duplicate_or_negative_ledger_rows_are_rejected(self):
        ledger=copy.deepcopy(LEDGER)
        ledger['rows'].append(copy.deepcopy(ledger['rows'][1]))
        with self.assertRaises(ValueError): calc.ledger_totals(ledger)
        ledger=copy.deepcopy(LEDGER)
        ledger['rows'][1]['unit_mass_g']=-1
        with self.assertRaises(ValueError): calc.ledger_totals(ledger)

    def test_source_total_is_reproduced_without_claiming_current_mass(self):
        r=calc.build_results(INPUTS,LEDGER)
        a=r['mass_audit']
        self.assertAlmostEqual(r['legacy_printed_body']['group_C_kg'],3.4465457774,places=12)
        self.assertEqual(a['pre_wheel_update_carry_total_kg'],10.973)
        self.assertEqual(a['updated_source_carry_total_kg'],10.919)
        self.assertEqual(a['source_estimate_gap_above_target_kg'],1.8471526)
        self.assertTrue(a['carry_total_matches_source'])
        self.assertFalse(a['current_configuration_reconciled'])
        self.assertIsNone(r['current_verified_installed_mass_kg'])
        self.assertFalse(r['hardware_test_results_included'])

    def test_inconsistent_wheel_dimensions_are_rejected(self):
        p=copy.deepcopy(INPUTS)
        p['current_design']['wheel']['rim_lip_to_tread_peak_mm']=15
        with self.assertRaises(ValueError): calc.build_results(p,LEDGER)

    def test_unsubstantiated_current_mass_cannot_be_promoted(self):
        p=copy.deepcopy(INPUTS)
        p['current_design']['mass']['verified_current_installed_mass_kg']=10.919
        with self.assertRaises(ValueError): calc.build_results(p,LEDGER)

    def test_cli_writes_consistent_portable_outputs(self):
        with tempfile.TemporaryDirectory() as temp:
            result=subprocess.run([sys.executable,str(ROOT/'calculations/calculate.py'),'--output-dir',temp],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            data=json.loads((Path(temp)/'results.json').read_text(encoding='utf-8'))
            self.assertEqual(data,calc.build_results(INPUTS,LEDGER))
            report=(Path(temp)/'results.md').read_text(encoding='utf-8')
            self.assertIn('Current assembled mass is not yet verified',report)
            self.assertIn('10.919',report)
            self.assertEqual(len((Path(temp)/'legacy-installed-mass.csv').read_text(encoding='utf-8').splitlines()),65)


if __name__=='__main__':
    unittest.main()
