# Laboratório Kubernetes da biblioteca

Contexto: `docker-desktop`. Todos os objetos desta entrega pertencem ao namespace `biblioteca`; a API de data e hora e os contêineres antigos são independentes. A imagem unificada executa Nginx e FastAPI em um contêiner de aplicação por Pod, como exigido pela atividade. PostgreSQL é um serviço de dados separado.

## Provisionamento e configuração

```bash
python3 scripts/devops/bootstrap.py
kubectl --context docker-desktop -n biblioteca get deploy,pods,svc,pvc
kubectl --context docker-desktop -n biblioteca port-forward service/biblioteca 18080:80
```

Interface: http://localhost:18080. Health: `/api/health`. Versão: `/api/version`. Documentação: `/api/docs`. Service porta 80 → contêiner porta 8080 → proxy interno para FastAPI porta 8000. O port-forward conecta um Pod; reiniciar o comando quando esse Pod for substituído. Ele não demonstra balanceamento entre réplicas.

O script preserva credenciais existentes. Em uma instalação nova, gera valores aleatórios apenas na memória e envia diretamente à API Kubernetes, sem arquivos de senhas. Secret `biblioteca-secrets` contém `DATABASE_URL`, `JWT_SECRET`, `POSTGRES_PASSWORD`, `INITIAL_ADMIN_EMAIL` e `INITIAL_ADMIN_PASSWORD`. Não copiar valores para o Git, logs, Trello, prints ou ZIPs. Kubernetes Secret usa base64, que não equivale a criptografia; este ambiente é um laboratório local.

O PostgreSQL possui uma réplica, Service ClusterIP e PVC de 1 GiB. Os dados não são os do SQLite antigo: não houve migração dos contêineres anteriores. O armazenamento local do Docker Desktop não constitui backup nem banco de produção com alta disponibilidade. Não expor o banco por NodePort ou porta pública.

O Job `biblioteca-init-db` inicializa esquema e administrador **antes** das réplicas. Nas réplicas `CREATE_INITIAL_ADMIN=false`; o esquema já existe quando o lifespan verifica as tabelas. O Job usa a implementação existente da aplicação, sem criar uma segunda definição de esquema. No laboratório ele roda uma vez; se precisar refazê-lo, confirmar banco e configuração antes de recriar o Job. Não excluir PVC, banco ou namespace para repetir escala ou rollback.

O usuário da aplicação é UID 10001/GID 999, sem elevação de privilégios. A aplicação não recebe a senha de bootstrap do administrador em suas variáveis; recebe apenas URL do banco e chave JWT. O namespace separa nomes, mas não cria por si só isolamento de rede.

## Validação real das réplicas

```bash
python3 scripts/devops/verify_runtime.py
python3 scripts/devops/verify_runtime.py --exercise
```

O segundo comando verifica 2→4→2 réplicas e exclui somente um Pod da aplicação. Cada réplica é consultada individualmente por HTTP usando `kubectl exec`: a prova de consistência não depende do port-forward selecionar réplicas diferentes. São criados usuários e registros sintéticos no banco do laboratório. Evidências sanitizadas ficam em `docs/devops/evidencias/`.

## Atualização e rollback

Usar uma tag inédita publicada pelo CI e confirmar seu digest. A versão da API é registrada separadamente da tag da imagem. O script exige imagem da biblioteca com digest:

```text
python3 scripts/devops/verify_release.py IMAGEM_REAL_COM_DIGEST --version VERSAO_REAL_DA_API
```

Substituir ambos os argumentos pelos valores reais publicados. O script anota imagem e revisão anteriores, aplica a nova imagem, verifica versão e dados em ambos os Pods, volta à revisão anotada e verifica a versão anterior. Por fim aplica novamente a imagem nova validada para deixar o ambiente corrigido. O rollback da imagem não desfaz mudanças no banco; estas versões não alteram o esquema.

Após a demonstração, alinhar a imagem de `deployment.yaml` com o estado final e aplicar o YAML. Não misturar `set image` com um YAML desatualizado. Atualizar a imagem do Job de inicialização somente em uma nova instalação ou em uma manutenção planejada: seu template é imutável depois de criado.

## Referências técnicas

- [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/): execução da inicialização antes da aplicação.
- [Aplicação com armazenamento persistente](https://kubernetes.io/docs/tasks/run-application/run-single-instance-stateful-application/): volume e separação entre dados e Pods.

Os arquivos `2026-10-28-preparacao.txt` registram apenas a preparação inicial. As evidências posteriores de runtime e release são as comprovações da execução; não interpretar o dry-run antigo como demonstração funcional.
