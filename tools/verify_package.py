"""Check local links and release-file integrity. Does not validate rover hardware."""
from pathlib import Path
import argparse,csv,hashlib,json,re,sys
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
TEXT={'.md','.py','.json','.csv','.txt','.html','.yml','.yaml','.svg','.gitattributes','.gitignore'}
def files():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in {'.git','__pycache__','.venv'} for x in p.relative_to(ROOT).parts) and p.suffix not in {'.pyc','.log'} and p.name!='manifest.json')
def digest(p):
 data=p.read_bytes()
 if p.suffix in TEXT or p.name in {'.gitignore','.gitattributes','LICENSE'}:
  return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest(),'text-lf'
 return hashlib.sha256(data).hexdigest(),'binary'
def audit():
 errors=[]
 for p in files():
  rel=p.relative_to(ROOT).as_posix()
  if p.stat().st_size>25*1024*1024:errors.append(rel+': exceeds browser upload limit; use release assets')
  if p.suffix=='.json':
   try:json.loads(p.read_text(encoding='utf-8-sig'))
   except ValueError as e:errors.append(rel+': invalid JSON '+str(e))
  if p.suffix=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.reader(f))
   if rows and any(len(row)!=len(rows[0]) for row in rows[1:]):errors.append(rel+': inconsistent CSV column count')
  if p.suffix=='.md':
   text=p.read_text(encoding='utf-8-sig')
   text=re.sub(r'```.*?```','',text,flags=re.S)
   for link in re.findall(r'\]\(([^\s]+?)(?:\s+"[^"]*")?\)',text):
    link=link.strip('<>')
    if urlsplit(link).scheme or link.startswith('#'):continue
    path=unquote(link.split('#',1)[0])
    if path and not (p.parent/path).exists():errors.append(rel+': missing local link '+link)
 return errors

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--update-manifest',action='store_true');a=p.parse_args()
 errors=audit();mp=ROOT/'manifest.json'
 if a.update_manifest:
  if errors:
   print('\n'.join(errors));return 1
  items=[]
  for f in files():
   sha,mode=digest(f);items.append({'path':f.relative_to(ROOT).as_posix(),'bytes':f.stat().st_size,'sha256':sha,'hash_mode':mode})
  mp.write_text(json.dumps({'package':'NASA HERC 2027 TEAM BANGLADESH','prepared_date':'2026-09-23','scope':'Package contents and normalized text integrity; not hardware validation','files':items},indent=2)+'\n',encoding='utf-8')
 elif not mp.exists():errors.append('manifest.json missing; run --update-manifest after reviewing changes')
 else:
  manifest=json.loads(mp.read_text(encoding='utf-8'))
  expected={item['path'] for item in manifest['files']}
  actual={f.relative_to(ROOT).as_posix() for f in files()}
  for name in sorted(expected-actual):errors.append('Missing file: '+name)
  for name in sorted(actual-expected):errors.append('Unlisted file: '+name)
  for item in manifest['files']:
   f=ROOT/item['path']
   if f.exists() and digest(f)[0]!=item['sha256']:errors.append('Changed file: '+item['path'])
 if errors:
  print('\n'.join(errors));return 1
 print(f'PASS: {len(files())} files, valid JSON/CSV, local links and package integrity. Hardware tests are separate.')
 return 0
if __name__=='__main__':sys.exit(main())
