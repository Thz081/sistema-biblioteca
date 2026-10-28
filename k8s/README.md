# Preparação Kubernetes da biblioteca

Estes arquivos pertencem à parte DevOps de Tacyo. Foram preparados antecipadamente; a validação de schema não comprova que a aplicação unificada funciona. O namespace pode ser criado agora. Deployment, ConfigMap e Service só devem ser aplicados depois da imagem e do banco compartilhado estarem prontos.

## Contrato para integração

- Namespace, Deployment e Service: `biblioteca`.
- Contêiner: `app`, uma única aplicação com frontend e backend.
- Porta proposta: 8000, a mesma já utilizada pelo backend FastAPI. A aplicação deve escutar em `0.0.0.0`.
- Probes: GET `/health` na porta 8000. As rotas `/health` e `/version` já existem no backend; a interface precisa ser unificada por Pedro.
- Imagem reservada: `ghcr.io/thz081/biblioteca-app:1.0.0`. Esta tag não foi construída nem publicada nesta preparação. Antes de implantar, confirmar o nome final e o digest no card de publicação.
- ConfigMap `biblioteca-config`: apenas configurações não secretas.
- Secret `biblioteca-secrets`: chaves `DATABASE_URL` e `JWT_SECRET`. Valores devem ser fornecidos no ambiente com revisão de Kerolyn, sem entrar no Git ou nas evidências.
- Banco compartilhado e persistente: depende da integração de Pedro e da configuração da infraestrutura. Não usar um SQLite independente por réplica.
- Criação automática de administrador está desabilitada para evitar inicializações concorrentes; combinar a preparação do esquema e do usuário de teste com Pedro.

Esses nomes e a porta são o contrato proposto para a entrega DevOps. Gabriel valida os requisitos e Pedro/Kerolyn devem confirmar a compatibilidade da aplicação/imagem antes de ativar o Deployment. Se a integração exigir outro nome ou porta, atualizar Deployment, Service e probes juntos.

## Validação sem implantar a aplicação

```bash
kubectl --context docker-desktop apply -f k8s/namespace.yaml
kubectl --context docker-desktop apply --dry-run=server -f k8s/configmap.yaml -f k8s/deployment.yaml -f k8s/service.yaml
```

O segundo comando envia os objetos para validação do servidor e não persiste esses recursos. Não cria Pods nem valida a existência da imagem, do Secret ou a disponibilidade do banco. O namespace apenas separa recursos por nome; ele não estabelece isolamento de rede por si só.

## Implantação após liberar as dependências

Antes de executar: imagem unificada publicada e verificada, Secret criado no namespace correto, banco compartilhado acessível, esquema preparado e configuração de autenticação revisada. Confirmar o acesso do cluster ao GHCR; imagens privadas exigem configuração apropriada de imagePullSecrets.

```bash
kubectl --context docker-desktop apply -f k8s/configmap.yaml
kubectl --context docker-desktop apply -f k8s/deployment.yaml -f k8s/service.yaml
kubectl --context docker-desktop -n biblioteca rollout status deployment/biblioteca --timeout=120s
kubectl --context docker-desktop -n biblioteca get deployment,pods,service -o wide
kubectl --context docker-desktop -n biblioteca port-forward service/biblioteca 18080:80
```

Em outro terminal, consultar `http://localhost:18080/`, `/health` e `/version`. A porta 18080 é uma sugestão: se estiver ocupada, escolher outra porta local. Registrar também os fluxos de login, livros e empréstimos; responder ao health não comprova todos os requisitos.

## Operações da Atividade 2 para executar depois

```bash
kubectl --context docker-desktop -n biblioteca scale deployment biblioteca --replicas=4
kubectl --context docker-desktop -n biblioteca rollout status deployment/biblioteca --timeout=120s
kubectl --context docker-desktop -n biblioteca get pods -l app=biblioteca
kubectl --context docker-desktop -n biblioteca scale deployment biblioteca --replicas=2
kubectl --context docker-desktop -n biblioteca rollout status deployment/biblioteca --timeout=120s
```

Para recuperar um Pod, escolher um nome real de `get pods`, anotar seu UID e excluir somente esse Pod do namespace biblioteca. Aguardar o substituto e verificar os dados. Não excluir o banco, volumes, namespace ou o Deployment.

Para atualizar, publicar primeiro uma tag inédita após a alteração de Pedro e a revisão de Kerolyn. Consultar `rollout history` antes de alterar a imagem e anotar a revisão anterior. Usar `set image deployment/biblioteca app=...` com a imagem real publicada. Para rollback, informar a revisão anotada em `rollout undo deployment/biblioteca --to-revision=...`. Conferir a versão por HTTP e alinhar o YAML final. Não executar esses comandos com valores de exemplo ou antes das imagens estarem disponíveis.

Os cards só são concluídos após os resultados reais serem registrados. A preparação destes comandos não equivale à execução dos exercícios.
