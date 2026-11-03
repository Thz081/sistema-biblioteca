#!/usr/bin/env python3
"""Demonstra atualização, rollback e retorno à imagem nova no laboratório biblioteca."""
import argparse
import base64
from datetime import datetime
import json
from pathlib import Path
import subprocess
from verify_runtime import K, cmd, pods, http

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('image',help='Imagem publicada, fixada por digest')
    parser.add_argument('--version',required=True,help='Versão esperada em /api/version')
    args=parser.parse_args()
    if not args.image.startswith('ghcr.io/thz081/biblioteca:') or '@sha256:' not in args.image:
        parser.error('Usar a imagem da biblioteca fixada por digest.')
    records=[]
    def record(message):records.append(message);print(message,flush=True)
    dep=json.loads(cmd('get','deployment','biblioteca','-o','json'))
    assert dep['spec']['replicas']==2
    previous_image=dep['spec']['template']['spec']['containers'][0]['image']
    previous_revision=dep['metadata']['annotations']['deployment.kubernetes.io/revision']
    assert previous_image!=args.image,'Atualização deve utilizar imagem diferente da atual.'
    secret=json.loads(cmd('get','secret','biblioteca-secrets','-o','json'))['data']
    value=lambda k:base64.b64decode(secret[k]).decode()
    ready=pods();assert len(ready)==2
    source=ready[0]['metadata']['name']
    previous_version=http(source,'/api/version')['version']
    token=http(source,'/api/auth/login',{'username':value('INITIAL_ADMIN_EMAIL'),'password':value('INITIAL_ADMIN_PASSWORD')},form=True)['access_token']
    books={b['id'] for b in http(source,'/api/livros',token=token)}
    loans={e['id']:e['status'] for e in http(source,'/api/emprestimos',token=token)}
    assert books and loans,'Executar verify_runtime.py antes para criar dados de referência.'
    def verify(version,stage):
        ready=pods();assert len(ready)==2
        for pod in ready:
            name=pod['metadata']['name']
            assert http(name,'/api/version')['version']==version
            assert http(name,'/api/health')['status']=='ok'
            assert http(name,'/api/auth/me',token=token)['perfil']=='ADMIN'
            assert books <= {b['id'] for b in http(name,'/api/livros',token=token)}
            current={e['id']:e['status'] for e in http(name,'/api/emprestimos',token=token)}
            assert all(current.get(i)==state for i,state in loans.items())
        record(f'{stage}: API {version}, duas réplicas prontas, livros/empréstimos e sessão preservados.')
    record('Imagem anterior: '+previous_image+'; revisão anterior: '+previous_revision)
    record('Imagem nova: '+args.image)
    record(cmd('set','image','deployment/biblioteca','app='+args.image).strip())
    record(cmd('rollout','status','deployment/biblioteca','--timeout=240s').strip())
    verify(args.version,'Atualização')
    record(cmd('rollout','undo','deployment/biblioteca','--to-revision='+previous_revision).strip())
    record(cmd('rollout','status','deployment/biblioteca','--timeout=240s').strip())
    verify(previous_version,'Rollback')
    record(cmd('set','image','deployment/biblioteca','app='+args.image).strip())
    record(cmd('rollout','status','deployment/biblioteca','--timeout=240s').strip())
    verify(args.version,'Estado final atualizado')
    record(cmd('rollout','history','deployment/biblioteca').strip())
    path=Path(__file__).resolve().parents[2]/'docs/devops/evidencias'
    path.mkdir(parents=True,exist_ok=True)
    (path/(datetime.now().astimezone().strftime('%Y%m%d%H%M%S')+'-release.txt')).write_text('\n'.join(records)+'\n')

if __name__=='__main__':main()
