"""Run inside Blender on the concept task file; never saves or changes the source file."""
import argparse,hashlib,json,math,sys
from datetime import datetime,timezone
from pathlib import Path
import bpy
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('cad/fresh-scene-check.json'));a=p.parse_args(args)
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'cad/example-scene-measurements.json').read_text(encoding='utf-8'))
report={'record_type':'CAD_GEOMETRY_CHECK','timestamp_utc':datetime.now(timezone.utc).isoformat(),'physical_test':False,'blender_version':bpy.app.version_string,'file_name':Path(bpy.data.filepath).name,'file_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'checks':[]}
def check(name,condition,actual=None):
 report['checks'].append({'name':name,'passed':bool(condition),'actual':actual})
s=bpy.data.scenes.get('01 | Both tasks - site overview')
check('task overview scene exists',s is not None)
if s:
 bpy.context.window.scene=s;s.frame_set(1);bpy.context.view_layer.update()
 rover=[o for o in s.objects if o.get('Part ID')]
 check('separate rover object count',len(rover)==1062,len(rover))
 if rover:
  vertices=[o.matrix_world@Vector(v) for o in rover for v in o.bound_box]
  bounds=[max(v[k] for v in vertices)-min(v[k] for v in vertices) for k in range(3)]
  check('recorded concept envelope',all(abs(x-y)<4e-6 for x,y in zip(bounds,manifest['rover_bounds_m'])),bounds)
 for t in manifest['targets']:
  board=bpy.data.objects.get(t['id']+' | 4 ft square whiteboard')
  check('board '+t['id']+' size',board is not None and abs(board.dimensions.y-1.2192)<1e-6 and abs(board.dimensions.z-1.2192)<1e-6)
  actual=math.dist(t['center'],t['sensor_origin_m'])/.3048
  check('example slant '+t['id'],abs(actual-t['sensor_slant_ft'])<1e-5,actual)
  horizontal=math.hypot(t['center'][0],t['center'][1])/.3048
  check('example start range '+t['id'],abs(horizontal-t['feet'])<1e-5,horizontal)
 tri=bpy.data.objects.get('03 | Green triangle - HEIGHT 0.3048m')
 if tri:
  vv=[tri.matrix_world@Vector(v) for v in tri.bound_box]
  height=max(v.z for v in vv)-min(v.z for v in vv)
  check('triangle vertical height',abs(height-.3048)<1e-6,height)
  check('triangle lower edge above 1 ft',min(v.z for v in vv)>=.3048,min(v.z for v in vv))
 else:check('triangle exists',False)
 images=[im for im in bpy.data.images if im.name.startswith('SIM-')]
 check('three packed simulated captures',len(images)==3 and all(im.packed_file for im in images),len(images))
 check('eight scenes',len(bpy.data.scenes)==8,len(bpy.data.scenes))
 check('example command spacing',all(b['elapsed_s']-a0['elapsed_s']==30 for a0,b in zip(manifest['commands'],manifest['commands'][1:])))
report['status']='PASS' if all(x['passed'] for x in report['checks']) else 'FAIL'
report['scope']='Concept scene object counts, bounds and illustration geometry only. No radio, camera, LiDAR or physical rover test was performed.'
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2));
if report['status']!='PASS':raise RuntimeError('Concept geometry check failed; see report')
