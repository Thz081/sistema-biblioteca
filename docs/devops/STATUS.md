# Auditoria e integração — 02/11/2026

Responsável técnico pela integração e execução desta revisão: Tacyo Henrique. Fuso das datas: America/Fortaleza. Evidências de contêiner podem mostrar UTC do dia seguinte; a execução registrada começou em 02/11 no horário local.

## Resultado técnico

- Imagem unificada, um contêiner de aplicação por Pod, com frontend Nginx e backend FastAPI.
- Imagem inicial da Kerolyn `ghcr.io/thz081/biblioteca:0.1.0`, digest `sha256:32470de27c5f5fd559a549d257a693e9525c949eb3cc7e75d8bdd7f9ae19322c`, baixada e testada.
- Release corrigida `ghcr.io/thz081/biblioteca:0.1.2`, digest `sha256:bab085505278ce7dc632e43748b43334523e22ac61e527ac446760ce9cdc923b`. Versão da API: `1.0.2`.
- Dois Pods prontos, Service ClusterIP 80→8080 e PostgreSQL compartilhado com PVC 1 GiB no namespace `biblioteca` do Docker Desktop.
- Inicialização de esquema e administrador em Job antes das réplicas, sem credenciais no Git. O administrador é desabilitado no startup das réplicas.
- Login e perfil, cadastro, catálogo, livro/exemplar, empréstimo, renovação e devolução verificados entre Pods diferentes.
- Escala 2→4→2 e recuperação automática de um Pod comprovadas com preservação de dados e UID diferente.
- Atualização API 1.0.0→1.0.2, rollback real para 1.0.0 e retorno final à versão corrigida 1.0.2. Livros, empréstimos e sessão preservados em ambas as réplicas.
- Frontend: 3 testes aprovados; backend: 6 testes aprovados no CI da release. As duas regressões acrescentadas cobrem login/perfil e sessão do leitor sem endpoints administrativos.
- Interface do leitor conferida no navegador após a atualização: catálogo disponível, comandos administrativos ocultos e sessão carregada sem erro de permissão.
- Interface, `/api/health`, `/api/version`, `/api/docs` e `/api/openapi.json` respondem HTTP 200 na porta local 18080.
- Build local e Compose isolado verificados; Compose saudável e API 1.0.2 em 18081. Projeto temporário de validação encerrado preservando o volume. Contêiner `biblioteca-auditoria`, criado nesta revisão, foi parado.

## O que foi integrado e corrigido

1. `main` e `develop` do fork divergiam. A documentação de Nicolly na main foi integrada, preservando seu planejamento; a branch de trabalho foi corrigida para develop.
2. Os commits `cf319a4` e `52fefb9`, com título “Conteiner unificado”, não alteravam arquivos. O commit real de Pedro, `5231b65`, de 29/10, estava somente na develop do repositório anterior. Foi integrado preservando autoria.
3. Havia duas definições concorrentes de unificação. O Dockerfile da raiz, preparado por Kerolyn, passou a ser o caminho do Compose e do CI. Os Dockerfiles individuais e start.sh são legados, não usados nesta entrega.
4. Caminhos do Compose e etapas antigas de build separado não eram compatíveis com a integração. O pipeline agora testa e constrói a imagem unificada; tags inéditas publicam no GHCR.
5. Os YAMLs preparados em 28/10 usavam porta/health provisórios. Foram ajustados para 8080 e `/api/health`, e a imagem foi fixada por digest.
6. O domínio `.local` do administrador gerava HTTP 500 ao serializar o perfil. Foi usado domínio de exemplo válido e corrigida a configuração inicial do laboratório.
7. A sessão de leitor tentava consultar endpoints administrativos. Agora usa seus empréstimos e dados permitidos; a API continua aplicando autorização.
8. O proxy da documentação foi configurado com `API_ROOT_PATH=/api`.
9. O Compose herdava o .env legado e tentava abrir SQLite em caminho incompatível. Usa agora `.env.unificada` opcional e `BIBLIOTECA_DATABASE_URL` para configuração explícita, sem alterar o arquivo antigo.

Commits de correção: [5ea8d6c](https://github.com/Thz081/sistema-biblioteca/commit/5ea8d6c), [528756d](https://github.com/Thz081/sistema-biblioteca/commit/528756d). [CI da release 0.1.2 aprovado](https://github.com/Thz081/sistema-biblioteca/actions/runs/41558543422).

## Evidências e reprodução

- [Runtime, escala e recuperação](evidencias/20261102220521-runtime.txt).
- [Atualização, rollback e estado final](evidencias/20261102221850-release.txt).
- [Procedimentos Kubernetes](../../k8s/README.md).
- Scripts: `scripts/devops/bootstrap.py`, `verify_runtime.py` e `verify_release.py`.
- O arquivo de 28/10 permanece como histórico de preparação; não é prova de execução das atividades.

## Conferência dos cards atuais

| Card | Resultado da conferência |
| --- | --- |
| Base · 01 | Fork e develop existentes; conclusão previamente registrada por Tacyo preservada. |
| Scrum · 01 | SPRINT.md de Nicolly integrado. Planejamento existente; acompanhamento final é outro card. |
| Scrum · 02 | Reaberto Em andamento: estava concluído com checklist 0/3; revisão, retrospectiva e encerramento ainda sem comprovação. |
| Atividade 1 · 01 | Requisitos e aceite de Gabriel continuam pendentes; a execução técnica não substitui a validação do analista. |
| Atividade 1 · 02 | Unificação integrada e verificada, com os históricos de Pedro e Kerolyn preservados e correções desta auditoria documentadas no card. |
| Atividade 1 · 03 | Imagem da Kerolyn confirmada por build, execução e UID não-root; ausência de .env/banco no diretório da aplicação verificada. |
| Atividade 1 · 04 | Publicação inicial confirmada por digest, pull e execução no cluster; card de Tacyo atualizado com evidências. |
| Atividade 1 · 05 | Infraestrutura e teste técnico realizados nesta revisão. Aceite do card de Pedro permanece pendente; não atribuir automaticamente a ele a conclusão executada por Tacyo. Sem migração do SQLite antigo. |
| Atividade 1 · 06 | Card de Tacyo concluído com Deployment, Service, duas réplicas e evidências reais. |
| Atividade 1 · 07 | Evidências técnicas disponíveis para Gabriel; conferir os critérios e registrar seu aceite funcional. |
| Atividade 1 · 08 | README e evidências atualizados tecnicamente; Gabriel ainda deve consolidar a documentação formal da entrega. |
| Atividade 2 · 01 | Card de Tacyo concluído: escala 2→4→2 comprovada em todas as réplicas. |
| Atividade 2 · 02 | Card de Tacyo concluído: substituição de um Pod e preservação de dados comprovadas. |
| Atividade 2 · 03 | Nova versão e correções existem nos commits desta auditoria; responsável deve revisar a contribuição e o aceite do card, sem atribuição falsa de autoria. |
| Atividade 2 · 04 | Card de Tacyo concluído: nova imagem publicada e rollout verificado. |
| Atividade 2 · 05 | Card de Tacyo concluído: rollback demonstrado e YAML alinhado à versão corrigida final. |
| Segurança · 01 | Varreduras automatizadas de código, dependências e segredos ainda precisam da revisão/entrega de Kerolyn. Testes de aplicação e imagem não equivalem a SAST/SCA. |
| Segurança · 02 | A revisão final de segurança e sanitização do pacote de evidências continua com Kerolyn. |
| Entrega · 01 | Dois ZIPs e cobertura formal das atividades ainda pendentes de Gabriel e aceite da PO. |
| Entrega · 02 | Reaberto A fazer: estava concluído com checklist 0/3, sem comprovação de demonstração, ZIPs ou envio. |

Há também cards novos de Gabriel para mapear requisitos e validar contêiner único/dados entre réplicas. Eles se relacionam aos cards Atividade 1 · 01 e 07; manter rastreabilidade e aceite do responsável, sem presumir que o teste técnico os concluiu.

## Limites e pendências

O laboratório usa dados sintéticos. Os bancos e contêineres antigos foram preservados e não foram migrados para o PostgreSQL. PVC local não substitui backup nem alta disponibilidade de banco em produção. As verificações técnicas desta revisão não constituem auditoria exaustiva de segurança, aceite da PO, retrospectiva, geração dos ZIPs ou confirmação de envio.

## Ideia reservada

Preparar futuramente slides e falas para explicar entregáveis e participação de cada integrante. A ideia foi guardada a pedido de Tacyo; sua produção não foi iniciada nesta revisão.
