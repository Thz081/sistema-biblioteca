#!/usr/bin/env python3
"""Verifica o laboratório e, com --exercise, executa escala e recuperação reais."""
import argparse
import base64
from datetime import datetime
import json
from pathlib import Path
import secrets
import subprocess

K = ["kubectl", "--context", "docker-desktop", "-n", "biblioteca"]
WORKER = '''import sys,json,urllib.request,urllib.parse,urllib.error
s=json.load(sys.stdin)
d=s.get("data")
h=s.get("headers",{})
if d is not None:
 if s.get("form"):
  d=urllib.parse.urlencode(d).encode()
 else:
  d=json.dumps(d).encode();h["Content-Type"]="application/json"
r=urllib.request.Request("http://127.0.0.1:8080"+s["path"],data=d,headers=h,method=s.get("method","POST" if d is not None else "GET"))
try:
 with urllib.request.urlopen(r,timeout=15) as res:
  body=res.read().decode(); print(json.dumps({"status":res.status,"body":json.loads(body) if body.startswith(("{","[")) else body}))
except urllib.error.HTTPError as e:
 print(json.dumps({"status":e.code,"body":e.read().decode()}))
'''

def cmd(*args):
    return subprocess.check_output(K + list(args), text=True)

def pods():
    data=json.loads(cmd("get","pods","-l","app=biblioteca","-o","json"))
    return [p for p in data['items'] if not p['metadata'].get('deletionTimestamp') and any(c['type']=='Ready' and c['status']=='True' for c in p['status'].get('conditions',[]))]

def http(pod,path,data=None,token=None,form=False,expected=200):
    spec={'path':path,'data':data,'form':form}
    if token: spec['headers']={'Authorization':'Bearer '+token}
    output=subprocess.check_output(K+['exec','-i',pod,'--','python','-c',WORKER],input=json.dumps(spec),text=True)
    result=json.loads(output)
    assert result['status']==expected, f"{path}: esperado {expected}, recebido {result['status']}"
    return result['body']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--exercise',action='store_true');args=parser.parse_args()
    records=[]
    def record(message): records.append(message);print(message,flush=True)
    data=json.loads(cmd('get','secret','biblioteca-secrets','-o','json'))['data']
    value=lambda key:base64.b64decode(data[key]).decode()
    ready=pods();assert len(ready)==2, 'Iniciar a validação com duas réplicas prontas.'
    p0,p1=[p['metadata']['name'] for p in ready]
    login=lambda p,email,password:http(p,'/api/auth/login',{'username':email,'password':password},form=True)['access_token']
    token=login(p0,value('INITIAL_ADMIN_EMAIL'),value('INITIAL_ADMIN_PASSWORD'))
    assert http(p1,'/api/auth/me',token=token)['perfil']=='ADMIN'
    record('Login no Pod '+p0+' e perfil autenticado no Pod '+p1+': OK')
    run_id=datetime.now().astimezone().strftime('%Y%m%d%H%M%S')
    category=http(p0,'/api/categorias',{'nome':'Validacao '+run_id},token,expected=201)
    book=http(p0,'/api/livros',{'titulo':'Livro de validacao '+run_id,'autor':'Laboratorio DevOps','categoria_id':category['id']},token,expected=201)
    copy=http(p0,f"/api/livros/{book['id']}/exemplares",{'tombo':'DEVOPS-'+run_id},token,expected=201)
    password=secrets.token_urlsafe(24);email='leitor'+run_id+'@example.com'
    reader=http(p0,'/api/usuarios',{'nome':'Leitor de validacao','email':email,'senha':password,'perfil':'LEITOR'},token,expected=201)
    reader_token=login(p1,email,password)
    loan=http(p1,'/api/emprestimos',{'exemplar_id':copy['id']},reader_token,expected=201)
    assert any(b['id']==book['id'] for b in http(p1,'/api/livros',token=reader_token))
    http(p0,f"/api/emprestimos/{loan['id']}/renovar",{},reader_token)
    returned=http(p1,f"/api/emprestimos/{loan['id']}/devolver",{},reader_token)
    assert returned['status']=='DEVOLVIDO'
    record(f"Cadastro, livro, exemplar, emprestimo, renovacao e devolucao entre Pods diferentes: OK (livro={book['id']}, emprestimo={loan['id']})")
    def check_state(count,phase):
        ready=pods();assert len(ready)==count
        for pod in ready:
            name=pod['metadata']['name']
            assert http(name,'/api/health')['status']=='ok'
            assert any(b['id']==book['id'] for b in http(name,'/api/livros',token=token))
            assert any(e['id']==loan['id'] and e['status']=='DEVOLVIDO' for e in http(name,'/api/emprestimos',token=token))
        record(f'{phase}: {count} Pods prontos; mesmos dados e JWT verificados em todos.')
        return ready
    check_state(2,'Inicial')
    if args.exercise:
        try:
            record(cmd('scale','deployment/biblioteca','--replicas=4').strip())
            record(cmd('rollout','status','deployment/biblioteca','--timeout=180s').strip())
            check_state(4,'Escala para quatro')
        finally:
            record(cmd('scale','deployment/biblioteca','--replicas=2').strip())
            record(cmd('rollout','status','deployment/biblioteca','--timeout=180s').strip())
        ready=check_state(2,'Retorno para duas')
        old=ready[0]['metadata'];previous={p['metadata']['uid'] for p in ready}
        record(cmd('delete','pod',old['name']).strip())
        record(cmd('rollout','status','deployment/biblioteca','--timeout=180s').strip())
        cmd('wait','--for=condition=Ready','pod','-l','app=biblioteca','--timeout=180s')
        after=check_state(2,'Recuperacao')
        new=[p for p in after if p['metadata']['uid'] not in previous];assert new
        record('Pod substituido: '+old['name']+' UID='+old['uid']+' -> '+new[0]['metadata']['name']+' UID='+new[0]['metadata']['uid'])
    versions={http(p['metadata']['name'],'/api/version')['version'] for p in pods()}
    record('Versoes da API: '+', '.join(sorted(versions)))
    record(cmd('get','deploy,pods,svc,pvc','-o','wide').strip())
    record('Fixtures sinteticas mantidas no banco do laboratorio para verificacao posterior. Nenhum segredo registrado.')
    directory=Path(__file__).resolve().parents[2]/'docs/devops/evidencias';directory.mkdir(parents=True,exist_ok=True)
    (directory/f'{run_id}-runtime.txt').write_text('\n'.join(records)+'\n')

if __name__=='__main__':main()
