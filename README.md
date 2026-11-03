# Sistema de Biblioteca — Novaris Tech

Aplicação acadêmica para usuários, livros, exemplares, empréstimos, renovações e devoluções. A entrega atual executa frontend Nginx e backend FastAPI em **uma imagem e um contêiner de aplicação por Pod**. No Kubernetes, as réplicas compartilham PostgreSQL com volume persistente.

## Equipe e acompanhamento

| Integrante | Responsabilidade |
| --- | --- |
| Tacyo Henrique | DevOps e organização do Trello |
| Pedro Paulo | Desenvolvimento |
| Gabriel Alves | Análise de requisitos e validação |
| Kerolyn | DevSecOps |
| Nicolly | Scrum Master e Product Owner |

[Quadro Trello](https://trello.com/b/tseoOgOv/biblioteca-novaris-tech) · [SPRINT.md](SPRINT.md) · [Plano](tasks/plan.md) · [Situação técnica e pendências](docs/devops/STATUS.md).

Fluxo de integração: desenvolver em `develop`, executar verificações e abrir PR para `main`. O fork `Thz081/sistema-biblioteca` é o destino atual; commits feitos no repositório anterior precisam ser integrados explicitamente.

## Imagem unificada

O **Dockerfile da raiz** é a definição usada no Compose, no CI e no Kubernetes. Nginx escuta em 8080 e encaminha `/api/` ao FastAPI em `127.0.0.1:8000`, dentro do mesmo contêiner. As configurações ficam em `docker/`. Os Dockerfiles individuais e `app/start.sh` são artefatos legados; não são usados no fluxo atual.

- Interface: `/`.
- Disponibilidade: `/api/health`.
- Versão da aplicação: `/api/version` (configuração `APP_VERSION`).
- Documentação da API: `/api/docs`.
- A tag da imagem e a versão da API são identificadores distintos; registrar ambos nas evidências.

## Executar no Kubernetes local

Pré-requisitos: Docker Desktop e seu Kubernetes ativos, contexto `docker-desktop`, `kubectl` e Python 3. O provisionamento abaixo é exclusivo do namespace `biblioteca`.

```bash
python3 scripts/devops/bootstrap.py
kubectl --context docker-desktop -n biblioteca port-forward service/biblioteca 18080:80
```

Acessar **http://localhost:18080**. Manter o terminal do port-forward aberto; reabrir o comando se o Pod conectado for substituído durante testes.

O bootstrap gera credenciais aleatórias diretamente em um Secret, preserva um Secret existente, provisiona o PostgreSQL e inicializa o esquema/administrador em Job antes de subir as duas réplicas. Não usa o banco SQLite nem os dados dos contêineres antigos. Este banco PostgreSQL é do laboratório, sem migração automática do banco antigo.

O administrador inicial do laboratório usa `admin@biblioteca.example.com`. A senha não está no repositório: o operador pode consultá-la localmente com `kubectl get secret` e decodificação base64 da chave `INITIAL_ADMIN_PASSWORD`. Não copiar o valor para cards, prints ou arquivos versionados. Base64 não é criptografia.

Mais detalhes, limites do laboratório, escala e rollback em [k8s/README.md](k8s/README.md).

## Executar uma instância local com Compose

```bash
docker compose -f backendcombanco/docker-compose.yml up -d --build
```

Acessar **http://localhost:18081**. Usa um volume nomeado e SQLite apenas para uma instância. `DATABASE_URL` pode apontar a outro banco. A criação automática de administrador é desabilitada por padrão; configurar variáveis de inicialização em arquivo local quando necessário. Não usar SQLite separado por Pod para simular dados compartilhados.

O arquivo opcional `backendcombanco/.env` é resolvido em relação ao Compose. Não versionar credenciais. Para parar, usar `docker compose -f backendcombanco/docker-compose.yml down` sem `-v`, preservando o volume.

## Testes e verificação

Desenvolvimento: Python 3.12 e Node.js 24, como no CI.

```bash
python3 -m venv backendcombanco/.venv
source backendcombanco/.venv/bin/activate
npm run setup
npm test
```

O frontend tem dois testes de utilitários. O backend tem seis testes incluindo login e carregamento de perfil. Os testes unitários não substituem a validação no Kubernetes.

Com o laboratório pronto, a verificação abaixo cria dados sintéticos, autentica em réplicas diferentes e confere livro, exemplar, empréstimo, renovação e devolução:

```bash
python3 scripts/devops/verify_runtime.py
# Acrescenta escala 2→4→2 e exclusão de um único Pod para comprovar recuperação:
python3 scripts/devops/verify_runtime.py --exercise
```

A verificação deixa as fixtures no banco do laboratório e registra somente resultados sanitizados em `docs/devops/evidencias/`. Não executá-la em produção. A escala retorna a duas réplicas mesmo se a validação com quatro falhar.

## CI e publicação

[Workflow](.github/workflows/ci-cd.yml): testes frontend e backend, seguidos de build do Dockerfile da raiz. Tags inéditas `v*` publicam a imagem `ghcr.io/thz081/biblioteca:<versão-da-tag>`. Branches e PRs validam sem publicar. Não sobrescrever tags antigas. Os YAMLs devem fixar a imagem publicada por digest.

O código de 29/10 do repositório anterior foi integrado preservando sua autoria. Os caminhos de Compose/pipeline foram alinhados à imagem unificada revisada. Resultados da API de data e hora não são evidência desta entrega.

## Entregas acadêmicas

Atividade 1: aplicação unificada, imagem publicada, Deployment com duas réplicas, Service e validação funcional. Atividade 2: escala, recuperação, nova versão, atualização e rollback. A documentação de evidências técnicas não equivale ao aceite da PO, aos dois ZIPs ou à confirmação de envio; consultar o status antes de marcar esses cards como concluídos.

Projeto desenvolvido para fins acadêmicos.
