#!/usr/bin/env python3
"""Provisiona somente o laboratório biblioteca no Docker Desktop, sem gravar segredos em disco."""
import json
from pathlib import Path
import secrets
import subprocess

ROOT = Path(__file__).resolve().parents[2]
K = ["kubectl", "--context", "docker-desktop"]

def run(*args):
    subprocess.run(K + list(args), cwd=ROOT, check=True)

def main():
    run("apply", "-f", "k8s/namespace.yaml")
    existing = subprocess.run(K + ["-n", "biblioteca", "get", "secret", "biblioteca-secrets", "--ignore-not-found", "-o", "name"], capture_output=True, text=True, check=True)
    if not existing.stdout.strip():
        password = secrets.token_urlsafe(32)
        secret = {"apiVersion": "v1", "kind": "Secret", "metadata": {"name": "biblioteca-secrets", "namespace": "biblioteca"}, "type": "Opaque", "stringData": {
            "POSTGRES_PASSWORD": password,
            "DATABASE_URL": f"postgresql+psycopg://biblioteca:{password}@biblioteca-postgres:5432/biblioteca",
            "JWT_SECRET": secrets.token_urlsafe(48),
            "INITIAL_ADMIN_EMAIL": "admin@biblioteca.example.com",
            "INITIAL_ADMIN_PASSWORD": secrets.token_urlsafe(24),
        }}
        subprocess.run(K + ["create", "-f", "-"], input=json.dumps(secret), text=True, check=True)
    else:
        print("Secret existente preservado; credenciais não foram alteradas.")
    run("apply", "-f", "k8s/postgres.yaml", "-f", "k8s/configmap.yaml")
    run("-n", "biblioteca", "rollout", "status", "deployment/biblioteca-postgres", "--timeout=240s")
    run("apply", "-f", "k8s/init-db.yaml")
    run("-n", "biblioteca", "wait", "--for=condition=complete", "job/biblioteca-init-db", "--timeout=240s")
    run("apply", "-f", "k8s/deployment.yaml", "-f", "k8s/service.yaml")
    run("-n", "biblioteca", "rollout", "status", "deployment/biblioteca", "--timeout=240s")
    print("Laboratório pronto. Não excluir o PVC para executar escala ou rollback.")

if __name__ == "__main__":
    main()
