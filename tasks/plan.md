# Plano de implementação das atividades Kubernetes da biblioteca

## Estado e repositório

Planejamento confirmado em 28/10/2026. As tarefas estão no Trello: https://trello.com/b/tseoOgOv/biblioteca-novaris-tech

Repositório de execução: https://github.com/Thz081/sistema-biblioteca
Branch de trabalho: `develop`. PRs de implementação devem apontar a `develop`; integrar em `main` após validação. O repositório original permanece como `upstream` local; `origin` aponta para o fork de Tacyo.

A base foi preparada pelo merge de `NicolyMissehelli:develop` em `NicolyMissehelli:main`, PR https://github.com/NicolyMissehelli/sistema-biblioteca/pull/4, commit `e7b64f74540d81e85941dbb769fbd9ffa1e90d2b`. O fork e sua develop partiram dessa revisão. Testes frontend/backend e builds passaram no CI do PR; os dois testes frontend também passaram localmente. O venv local não tinha pytest, por isso a verificação do backend usou o CI aprovado.

A implementação das novas atividades ainda não foi executada. Não confundir planejamento com evidências de entrega. As tarefas novas devem gerar provas da biblioteca; resultados da API de data e hora não servem para comprovar este projeto.

## Equipe confirmada pelo usuário

| Integrante | Cargo | Responsabilidade |
|---|---|---|
| Tacyo Henrique | DevOps | GHCR, infraestrutura, Kubernetes, escala, recuperação, atualização e rollback; mantém Trello |
| Pedro Paulo | Desenvolvedor | Unificação da aplicação, integração de dados e nova versão |
| Gabriel Alves | Analista de requisitos | Rastreabilidade dos requisitos, critérios de aceite, validação funcional, evidências e conferência dos ZIPs |
| Kerolyn | DevSecOps | Segurança da imagem, segredos, varreduras e permissões do pipeline |
| Nicolly | Scrum Master e PO | Objetivo, backlog, acompanhamento, revisão, retrospectiva, aceite e coordenação de entrega no repositório |

Vinicius saiu do grupo. Ele não recebe tarefas nesta sprint. Membros em cards históricos foram preservados, sem remoção de acesso ao quadro.

Nicolly atualiza e mantém `SPRINT.md` conforme os cards. O arquivo principal contém a base da sprint atual; o documento anterior foi preservado em `docs/historico/SPRINT-2026-09-21-a-2026-10-05.md`. Não criar um documento Scrum duplicado. Este plano e o índice JSON apenas registram decisões e links; o acompanhamento das tarefas permanece no Trello.

## Quadro atualizado

Os 17 cards do antigo Product Backlog foram arquivados de forma recuperável. Os 35 cards históricos de Concluído e os cards de orientação das listas foram preservados. Foram criados 20 cards novos, sem GOV-01/GOV-02: a organização do quadro é feita por Tacyo, não uma entrega atribuída à equipe Scrum.

Cada card tem membro responsável, cargo, prioridade/estimativa inicial, tipo de verificação, prazo real no Trello, dependências, critérios de aceite, checklist nativo, referência ao novo repositório e situação. Nenhuma tarefa foi declarada concluída sem execução.

Estado inicial: Base · 01 em Em andamento (fork e develop já criados, preparação pendente); Scrum · 01 e Atividade 1 · 01 em A fazer; demais tarefas no Product Backlog até satisfazer dependências.

## Decisões e riscos técnicos

A biblioteca atual usa frontend Nginx e backend FastAPI separados. A atividade 1 pede adaptação para uma aplicação em um único contêiner. Proposta: servir os arquivos do frontend pela API, mantendo uma imagem e um contêiner de aplicação por Pod. Pedro implementa; Tacyo apoia portas/infraestrutura e Kerolyn revisa imagem e configuração.

A configuração publicada usa SQLite em volume. SQLite independente por Pod cria dados divergentes e não atende ao fluxo da biblioteca com réplicas. Definir banco compartilhado e persistente antes da escala. PostgreSQL é candidato compatível com o driver já listado, mas exige testar esquema, inicialização e usuários. O banco é tratado como dependência de infraestrutura; Gabriel deve validar essa interpretação do enunciado antes da implementação.

Não embutir banco real, .env, JWT ou credenciais na imagem. Todas as réplicas precisam de configuração JWT consistente. Evitar criação concorrente de administrador durante a inicialização. Preservar os dados existentes e não executar migrações destrutivas neste laboratório.

Usar tags novas para a aplicação unificada; preservar as imagens antigas separadas. A atualização da atividade 2 deve ser pequena e sem mudança de esquema. Rollback de imagem não reverte dados de banco.

## Sequência e pontos de controle

1. Confirmar fork/develop, acessos e destinos de CI/GHCR; documentar Scrum e requisitos.
2. Unificar a aplicação e implementar dados compartilhados.
3. Construir e revisar a imagem; verificar pipeline e segredos; publicar versão inicial.
4. Implantar Deployment/Service com duas réplicas; validar fluxos e reunir evidências da atividade 1.
5. Registrar 2→4→2 réplicas e substituição automática de Pod.
6. Implementar alteração, verificar nova imagem, publicar, atualizar e executar rollback.
7. Sanitizar evidências, validar critérios, gerar dois ZIPs e realizar a demonstração.

Pontos de controle: após implantação, comprovar fluxo funcional e dados entre réplicas; após rollback, comprovar versão anterior e persistência; antes dos ZIPs, conferir todos os requisitos e revisão de segurança. Definição de concluído: critérios atendidos, verificação realizada, commit/PR no repositório correto e evidência vinculada; aceite da PO quando aplicável.

## Cronograma e índice dos cards

Prazo final informado: quarta-feira, 04/11/2026. Horários internos: tarefas em geral às 18h; ZIPs em 04/11 às 12h; envio em 04/11 às 16h, todos em America/Fortaleza. Esses horários são metas da equipe, não um horário oficial de entrega fornecido pelo professor. Validar disponibilidade para as datas de fim de semana e 02/11.

| Card | Responsável | Prazo | Link |
|---|---|---|---|
| Base · 01 — Criar o novo repositório a partir da main validada | Tacyo Henrique | 29/10/2026 18:00 | [Abrir](https://trello.com/c/G9pj3gpI) |
| Scrum · 01 — Atualizar SPRINT.md com o planejamento da sprint | Nicolly | 29/10/2026 18:00 | [Abrir](https://trello.com/c/IHxFKfh3) |
| Scrum · 02 — Manter acompanhamento e revisão no SPRINT.md | Nicolly | 03/11/2026 18:00 | [Abrir](https://trello.com/c/wSaPNW4a) |
| Atividade 1 · 01 — Validar requisitos e critérios da implantação | Gabriel Alves | 29/10/2026 18:00 | [Abrir](https://trello.com/c/qqhZ2YKO) |
| Atividade 1 · 02 — Unificar frontend e backend da biblioteca | Pedro Paulo | 29/10/2026 18:00 | [Abrir](https://trello.com/c/8NY7LUMu) |
| Atividade 1 · 03 — Construir imagem unificada e testar localmente | Kerolyn | 30/10/2026 18:00 | [Abrir](https://trello.com/c/X56o0quq) |
| Atividade 1 · 04 — Publicar imagem inicial da biblioteca no GHCR | Tacyo Henrique | 30/10/2026 18:00 | [Abrir](https://trello.com/c/4J3F5Dk8) |
| Atividade 1 · 05 — Configurar banco compartilhado e segredos | Pedro Paulo | 30/10/2026 18:00 | [Abrir](https://trello.com/c/5GuevME9) |
| Atividade 1 · 06 — Criar Deployment com duas réplicas e Service | Tacyo Henrique | 31/10/2026 18:00 | [Abrir](https://trello.com/c/CMEaYHrP) |
| Atividade 1 · 07 — Validar dois Pods e funcionamento no Kubernetes | Gabriel Alves | 31/10/2026 18:00 | [Abrir](https://trello.com/c/Tkd4GuCm) |
| Atividade 1 · 08 — Documentar implantação e reunir evidências | Gabriel Alves | 01/11/2026 18:00 | [Abrir](https://trello.com/c/KKwUhqmh) |
| Atividade 2 · 01 — Demonstrar escala de duas para quatro e retorno | Tacyo Henrique | 02/11/2026 18:00 | [Abrir](https://trello.com/c/Y84rRjuW) |
| Atividade 2 · 02 — Demonstrar recuperação automática de um Pod | Tacyo Henrique | 02/11/2026 18:00 | [Abrir](https://trello.com/c/fQn7lVBZ) |
| Atividade 2 · 03 — Alterar a aplicação e identificar nova versão | Pedro Paulo | 02/11/2026 18:00 | [Abrir](https://trello.com/c/ytplViTH) |
| Atividade 2 · 04 — Publicar nova imagem e realizar atualização | Tacyo Henrique | 03/11/2026 18:00 | [Abrir](https://trello.com/c/ynuoQxer) |
| Atividade 2 · 05 — Executar rollback e validar estado final | Tacyo Henrique | 03/11/2026 18:00 | [Abrir](https://trello.com/c/51lfL6TW) |
| Entrega · 01 — Conferir requisitos e gerar os dois ZIPs | Gabriel Alves | 04/11/2026 12:00 | [Abrir](https://trello.com/c/kHlfB3FM) |
| Entrega · 02 — Preparar demonstração prática e confirmar envio | Nicolly | 04/11/2026 16:00 | [Abrir](https://trello.com/c/yjbFbMWC) |
| Segurança · 01 — Integrar varreduras e revisar segredos do pipeline | Kerolyn | 30/10/2026 18:00 | [Abrir](https://trello.com/c/gseGCjRR) |
| Segurança · 02 — Revisar nova imagem e sanitizar evidências finais | Kerolyn | 03/11/2026 18:00 | [Abrir](https://trello.com/c/xHKWC3yZ) |

## Pendências de preparação

- Conferir se os cinco integrantes têm o acesso necessário ao fork, ou combinar contribuições por forks/PRs. Criar o fork não transfere automaticamente a colaboração do repositório de origem.
- Validar GitHub Actions no fork e ajustar os destinos de publicação para a imagem unificada. A primeira publicação depende da revisão DevSecOps.
- Confirmar com o professor o formato da demonstração e a interpretação do banco como infraestrutura separada.
- Confirmar nomes/contas sem alterar autoria de commits de terceiros. Não atribuir implementações automáticas a integrantes que ainda não as executaram.
