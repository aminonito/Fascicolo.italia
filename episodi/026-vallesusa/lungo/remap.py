import json,os,sys,shutil
sys.path.insert(0,'.')
from script import SCENES
old={}
for f in os.listdir('vometa'):
    m=json.load(open('vometa/'+f)); old[m['key']]=int(f[:-5])
os.makedirs('vm2',exist_ok=True); os.makedirs('au2',exist_ok=True)
miss=[]
for si,sc in enumerate(SCENES):
    k=json.dumps(sc,ensure_ascii=False)
    if k in old:
        o=old[k]; shutil.copy(f'vometa/{o}.json',f'vm2/{si}.json'); shutil.copy(f'audio/s{o}.wav',f'au2/s{si}.wav')
    else: miss.append(si)
print("missing",miss)
shutil.rmtree('vometa'); os.rename('vm2','vometa')
for f in os.listdir('audio'):
    if f.startswith('s') and f[1:-4].isdigit(): os.remove('audio/'+f)
for f in os.listdir('au2'): shutil.move('au2/'+f,'audio/'+f)
os.rmdir('au2')
