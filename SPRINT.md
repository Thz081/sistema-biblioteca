# 🏃 Sprint 1 e 2 — Sistema da Biblioteca

Sprint 1 e 2 — Atividades Integradoras de Kubernetes

Período: 28/10/2026 a 04/11/2026\
Responsável pela documentação: Nicolly — Scrum Master e Product Owner\
Repositório: Thz081/sistema-biblioteca\
Branch de trabalho: develop\
Quadro Scrum: Biblioteca Novaris Tech\

Este arquivo é o registro oficial de planejamento e acompanhamento da sprint. As situações devem refletir o que foi efetivamente executado e validado. Planejamento, instruções dos slides e exemplos didáticos não constituem evidência de entrega.

 1. Objetivo da sprint

Preparar, implantar e validar o Sistema de Biblioteca no Kubernetes para atender às Atividades Integradoras 1 e 2.

- Atividade 1 — Implantação: preparar a aplicação unificada, construir e testar sua imagem Docker, publicá-la no GitHub Container Registry (GHCR), configurar banco compartilhado e segredos, implantar a aplicação com duas réplicas e validar seu funcionamento.
- Atividade 2 — Operação e atualização: demonstrar escalabilidade de duas para quatro réplicas e retorno para duas, recuperação automática de um Pod, publicação de uma nova versão, atualização da aplicação e rollback.

O fluxo de DevOps apresentado nos materiais de apoio será aplicado ao próprio Sistema de Biblioteca: preparar a aplicação, construir a imagem, executar testes, publicar uma versão identificável no GHCR e utilizar essa mesma imagem nos ambientes. Os exemplos de api-data-hora dos slides são apenas didáticos e não devem ser usados como nome, imagem, evidência ou resultado deste projeto.

 2. Contexto e escopo

O Sistema de Biblioteca é uma aplicação web para gerenciamento de livros, categorias, exemplares, usuários, autenticação, empréstimos, renovações e devoluções. A base tecnológica do projeto inclui Python, FastAPI, SQLite na configuração anterior, HTML, CSS e JavaScript, além de testes automatizados, Docker, Docker Compose, Terraform, Ansible e GitHub Actions.

A base validada foi integrada ao repositório atual. O histórico de testes e builds da base anterior serve como referência técnica, mas não comprova a execução das novas atividades desta sprint.

 Escopo técnico desta sprint

1. Unificar frontend e backend para execução em uma imagem e um contêiner de aplicação por Pod.
2. Construir uma imagem Docker adequada ao projeto, com .dockerignore, execução sem privilégios de root e sem inclusão de segredos.
3. Validar a imagem localmente e publicar uma tag inédita no GHCR.
4. Definir e validar banco compartilhado e persistente para que as réplicas utilizem os mesmos dados.
5. Criar Deployment com duas réplicas e Service no Kubernetes.
6. Validar os fluxos funcionais da biblioteca e a consistência dos dados entre Pods.
7. Demonstrar escala, recuperação automática, atualização e rollback.
8. Revisar segurança, documentar os resultados e preparar os dois arquivos ZIP de entrega.

 Fora do escopo

- Reutilizar imagens, nomes, logs, URLs ou evidências da API de data e hora usada nos slides.
- Declarar como concluída uma tarefa apenas porque existe um tutorial, YAML preparado, comando documentado ou pipeline configurado.
- Incluir senhas, tokens, chaves, arquivos .env, dados pessoais ou credenciais nas imagens, commits, prints ou ZIPs.
- Executar migrações destrutivas ou considerar que rollback da imagem desfaz alterações no banco de dados.

 3. Equipe e responsabilidades

| Integrante     | Cargo                        | Responsabilidades na sprint                                                                                                        |
| -------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Tacyo Henrique | DevOps                       | GHCR, infraestrutura, Kubernetes, Deployment, Service, escalabilidade, recuperação, atualização e rollback; organização do Trello. |
| Pedro Paulo    | Desenvolvedor                | Unificação do frontend e backend, integração dos dados, configuração da aplicação e implementação da nova versão.                  |
| Gabriel Alves  | Analista de requisitos       | Rastreabilidade dos requisitos, critérios de aceite, validação funcional, documentação, evidências e conferência dos ZIPs.         |
| Kerolyn        | DevSecOps                    | Segurança da imagem, revisão de segredos e permissões, varreduras e sanitização das evidências.                                    |
| Nicolly        | Scrum Master e Product Owner | Planejamento, priorização, acompanhamento, remoção de impedimentos, revisão, retrospectiva, aceite e coordenação da entrega.       |

A equipe desta sprint é composta por cinco integrantes. As tarefas devem permanecer associadas aos responsáveis definidos nos cards do Trello.

 4. Product Backlog

O Product Backlog reúne os itens necessários para atingir os objetivos das duas atividades. A priorização considera dependências técnicas: a implantação depende da aplicação unificada, da imagem e do banco compartilhado; as demonstrações da Atividade 2 dependem de uma implantação funcional.

| Prioridade | Item                                      | Resultado esperado                                                            |
| ---------- | ----------------------------------------- | ----------------------------------------------------------------------------- |
| Alta       | Validar requisitos da implantação         | Requisitos das Atividades 1 e 2 convertidos em critérios verificáveis.        |
| Alta       | Unificar frontend e backend               | Aplicação da biblioteca executada em um contêiner por Pod.                    |
| Alta       | Construir e testar imagem                 | Imagem Docker construída e validada localmente.                               |
| Alta       | Publicar imagem inicial no GHCR           | Imagem da biblioteca publicada com tag inédita e digest registrado.           |
| Alta       | Configurar banco compartilhado e segredos | Réplicas conectadas à mesma fonte persistente, sem credenciais na imagem.     |
| Alta       | Implantar duas réplicas e Service         | Deployment e Service aplicados no Kubernetes.                                 |
| Alta       | Validar Pods e fluxos funcionais          | Dois Pods prontos e funcionalidades essenciais verificadas.                   |
| Média      | Documentar implantação                    | README e evidências reais da Atividade 1 organizados.                         |
| Alta       | Demonstrar escalabilidade                 | Escala 2 → 4 → 2 registrada e validada.                                       |
| Alta       | Demonstrar recuperação automática         | Pod substituído automaticamente e novamente pronto.                           |
| Alta       | Implementar nova versão                   | Alteração visível e testada, sem migração de esquema.                         |
| Alta       | Publicar e atualizar                      | Nova imagem publicada sem sobrescrever a versão anterior e rollout validado.  |
| Alta       | Executar rollback                         | Revisão anterior restaurada e estado final verificado.                        |
| Alta       | Revisar segurança e entrega               | Imagem e evidências revisadas; dois ZIPs conferidos e demonstração preparada. |

 5. Sprint Backlog — cards, responsáveis e critérios de aceite

Os títulos abaixo correspondem aos cards existentes no Trello. As situações reproduzem o registro consultado no índice tasks/trello-cards.json e devem ser atualizadas conforme o quadro. O critério de aceite descreve o que precisa ser demonstrado; não significa que já foi aprovado.

 Preparação e organização

| Card                                                           | Responsável / prazo         | Critério de aceite                                                                                                                        | Situação registrada |
| -------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| Base · 01 — Criar o novo repositório a partir da main validada | Tacyo Henrique — 29/10, 18h | Fork e branch develop criados a partir da base validada; destino do trabalho confirmado.                                                  | Concluído           |
| Scrum · 01 — Atualizar SPRINT.md com o planejamento da sprint  | Nicolly — 29/10, 18h        | Este documento registra objetivo, equipe, Product Backlog, Sprint Backlog, critérios de aceite e Definition of Done vinculados aos cards. | A fazer             |
| Scrum · 02 — Manter acompanhamento e revisão no SPRINT.md      | Nicolly — 03/11, 18h        | Acompanhamento, impedimentos, decisões, revisão, retrospectiva e resultados finais registrados com evidências reais.                      | Product Backlog     |

 Atividade 1 — Implantação da biblioteca

| Card                                                               | Responsável / prazo         | Critério de aceite                                                                                                                                               | Situação registrada |
| ------------------------------------------------------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| Atividade 1 · 01 — Validar requisitos e critérios da implantação   | Gabriel Alves — 29/10, 18h  | Requisitos do enunciado mapeados para critérios verificáveis; aplicação unificada e compartilhamento de dados validados com a equipe.                            | A fazer             |
| Atividade 1 · 02 — Unificar frontend e backend da biblioteca       | Pedro Paulo — 29/10, 18h    | Frontend servido pela aplicação/API; uma imagem e um contêiner de aplicação por Pod; interface, rotas, login e consulta de livros preservados.                   | Product Backlog     |
| Atividade 1 · 03 — Construir imagem unificada e testar localmente  | Kerolyn — 30/10, 18h        | Dockerfile e .dockerignore revisados; imagem construída e executada localmente; execução sem root e contexto sem segredos verificados.                           | Product Backlog     |
| Atividade 1 · 04 — Publicar imagem inicial da biblioteca no GHCR   | Tacyo Henrique — 30/10, 18h | Imagem da biblioteca publicada no GHCR com tag inédita; endereço, digest e acesso necessário ao cluster registrados.                                             | Product Backlog     |
| Atividade 1 · 05 — Configurar banco compartilhado e segredos       | Pedro Paulo — 30/10, 18h    | Banco compartilhado e persistente configurado; inicialização consistente; segredos fornecidos por configuração segura, sem inclusão na imagem ou no repositório. | Product Backlog     |
| Atividade 1 · 06 — Criar Deployment com duas réplicas e Service    | Tacyo Henrique — 31/10, 18h | Deployment e Service aplicados; duas réplicas prontas; imagem correta em execução. YAMLs preparados e dry-run isoladamente não bastam para concluir.             | Em andamento        |
| Atividade 1 · 07 — Validar dois Pods e funcionamento no Kubernetes | Gabriel Alves — 31/10, 18h  | Dois Pods prontos; acesso à aplicação e fluxos essenciais testados; consistência dos dados entre réplicas comprovada.                                            | Product Backlog     |
| Atividade 1 · 08 — Documentar implantação e reunir evidências      | Gabriel Alves — 01/11, 18h  | README e índice da entrega atualizados com Dockerfile, YAMLs, referência da imagem, commit e evidências reais da biblioteca.                                     | Product Backlog     |

 Atividade 2 — Escalabilidade, recuperação, atualização e rollback

| Card                                                               | Responsável / prazo         | Critério de aceite                                                                                                                                | Situação registrada |
| ------------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| Atividade 2 · 01 — Demonstrar escala de duas para quatro e retorno | Tacyo Henrique — 02/11, 18h | Demonstrar e registrar 2 → 4 → 2 réplicas prontas; aplicação acessível e dados preservados durante a alteração.                                   | Product Backlog     |
| Atividade 2 · 02 — Demonstrar recuperação automática de um Pod     | Tacyo Henrique — 02/11, 18h | Registrar a substituição de um Pod, o novo identificador e a retomada da prontidão, sem perda dos dados persistidos.                              | Product Backlog     |
| Atividade 2 · 03 — Alterar a aplicação e identificar nova versão   | Pedro Paulo — 02/11, 18h    | Alteração funcional visível, identificador de versão atualizado e testes relevantes aprovados; sem migração de esquema.                           | Product Backlog     |
| Atividade 2 · 04 — Publicar nova imagem e realizar atualização     | Tacyo Henrique — 03/11, 18h | Nova tag publicada no GHCR sem sobrescrever a anterior; rollout concluído e nova versão identificada na aplicação.                                | Product Backlog     |
| Atividade 2 · 05 — Executar rollback e validar estado final        | Tacyo Henrique — 03/11, 18h | Revisão anterior restaurada; versão em execução, duas réplicas e dados persistidos conferidos. Configuração declarativa alinhada ao estado final. | Product Backlog     |
| Segurança · 02 — Revisar nova imagem e sanitizar evidências finais | Kerolyn — 03/11, 18h        | Nova imagem revisada; execução sem root, configurações, logs e evidências verificados; nenhum segredo ou dado pessoal exposto.                    | Product Backlog     |

 Entrega

| Card                                                           | Responsável / prazo        | Critério de aceite                                                                                                                         | Situação registrada |
| -------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- |
| Entrega · 01 — Conferir requisitos e gerar os dois ZIPs        | Gabriel Alves — 04/11, 12h | Dois ZIPs, um por atividade, conferidos quanto a conteúdo, integridade, requisitos e ausência de dados sensíveis; aceite da PO registrado. | Product Backlog     |
| Entrega · 02 — Preparar demonstração prática e confirmar envio | Nicolly — 04/11, 16h       | Demonstração organizada com participação dos cinco cargos; entregáveis validados e envio confirmado com registro verificável.              | Product Backlog     |

 6. Cronograma de referência

| Data  | Planejamento e ponto de controle                                                                            |
| ----- | ----------------------------------------------------------------------------------------------------------- |
| 28/10 | Abertura da sprint, alinhamento dos objetivos, organização do quadro e definição das responsabilidades.     |
| 29/10 | Base do repositório, documentação Scrum, validação de requisitos e unificação da aplicação.                 |
| 30/10 | Construção e teste local da imagem, publicação inicial no GHCR, banco compartilhado e revisão de segurança. |
| 31/10 | Deployment, Service, duas réplicas e validação funcional no Kubernetes.                                     |
| 01/11 | Documentação da implantação e consolidação das evidências da Atividade 1.                                   |
| 02/11 | Demonstrações de escalabilidade e recuperação automática; alteração e identificação da nova versão.         |
| 03/11 | Publicação da nova imagem, atualização, rollback e revisão final de segurança.                              |
| 04/11 | Conferência dos dois ZIPs até 12h; preparação da demonstração e confirmação do envio até 16h.               |

Os horários acima são metas internas registradas nos cards, não horários oficiais definidos pelo professor. A disponibilidade da equipe para fins de semana e para 02/11 deve ser confirmada no acompanhamento.

 7. Definition of Done — Definição de Concluído

Uma tarefa somente poderá ser marcada como concluída quando:

- O critério de aceite do respectivo card tiver sido atendido.
- A execução tiver sido verificada no ambiente correspondente; documentação ou configuração isolada não substitui teste.
- O código ou documento estiver no repositório correto, na branch de trabalho ou PR correspondente.
- Os testes pertinentes tiverem sido executados e o resultado estiver registrado.
- As evidências demonstrarem o Sistema de Biblioteca, com identificação de data, versão ou recurso quando pertinente.
- Os registros de commit, PR, execução do GitHub Actions, pacote GHCR, digest e registros Kubernetes estiverem vinculados ao card quando aplicáveis.
- A revisão de segurança confirmar ausência de senhas, tokens, chaves, arquivos .env, dados pessoais e configurações sigilosas nas imagens e evidências.
- O responsável atualizar a situação do card e registrar impedimentos ou pendências.
- O aceite da Product Owner for registrado nos itens que exigirem validação do produto.

 Definition of Done das entregas

Atividade 1: aplicação unificada executável; imagem Docker construída, testada e publicada no GHCR; banco compartilhado configurado; Deployment com duas réplicas e Service em funcionamento; fluxos essenciais e consistência dos dados validados; documentação e evidências reunidas.

Atividade 2: escala 2 → 4 → 2 demonstrada; recuperação automática de Pod comprovada; nova versão identificada, testada e publicada; atualização e rollback demonstrados; estado final e persistência dos dados conferidos.

Entrega final: dois ZIPs conferidos, demonstração preparada, evidências sanitizadas e envio confirmado.

 8. Estratégia de evidências

As evidências devem ser produzidas durante a execução e vinculadas aos respectivos cards. Priorizar:

- Código e integração: commits, PRs direcionados à branch develop e resultados reais do GitHub Actions.
- Imagem: pacote da biblioteca no GHCR, tag publicada e digest correspondente.
- Teste local: comandos executados e resposta real da aplicação da biblioteca.
- Kubernetes: arquivos YAML aplicados, estado dos Deployments, Services e Pods, registros de escala, substituição de Pod, atualização e rollback.
- Funcionalidade: comprovação dos fluxos da biblioteca e da consistência dos dados entre réplicas.
- Segurança: resultados das verificações e confirmação de que evidências e artefatos não contêm segredos ou dados pessoais.

Não inserir prints ilustrativos dos slides como se fossem resultados da execução. Não utilizar evidências da API de data e hora. Quando uma evidência ainda não existir, registrar “Pendente de execução” e atualizar após a verificação.

 9. Riscos, dependências e impedimentos

| Risco ou dependência                                 | Impacto possível                                                      | Acompanhamento                                                                   |
| ---------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Aplicação ainda não unificada                        | Impede a construção da imagem final e a implantação prevista.         | Pedro implementa; Tacyo apoia a integração e Kerolyn revisa a imagem.            |
| Banco SQLite independente por Pod                    | Pode gerar dados divergentes entre réplicas.                          | Definir e testar banco compartilhado e persistente antes da validação de escala. |
| Inicialização concorrente                            | Pode causar criação duplicada de usuários ou falhas na inicialização. | Validar estratégia de inicialização e consistência com Pedro e Gabriel.          |
| Segredos ou permissões inadequadas                   | Pode expor credenciais ou impedir publicação e execução.              | Kerolyn revisa configuração, permissões e evidências.                            |
| Acesso ao fork e ao GHCR                             | Pode bloquear contribuições ou publicação.                            | Tacyo confirma acessos e destinos do pipeline.                                   |
| Disponibilidade da equipe                            | Pode afetar prazos de fim de semana e 02/11.                          | Nicolly acompanha e registra ajustes acordados no Trello.                        |
| Rollback da imagem confundido com rollback dos dados | Pode comprometer a consistência da aplicação.                         | Preservar o banco e validar separadamente a versão da imagem e os dados.         |

Impedimentos reais devem ser registrados com data, responsável, impacto e decisão tomada. Não registrar como resolvido sem confirmação.

 10. Acompanhamento, revisão e retrospectiva

 Registro de acompanhamento

| Data          | Card / assunto             | Situação ou impedimento                    | Decisão / próximo passo            | Evidência                      |
| ------------- | -------------------------- | ------------------------------------------ | ---------------------------------- | ------------------------------ |
| 28/10 a 04/11 | Preencher durante a sprint | Pendente de atualização conforme execução. | Registrar decisões e responsáveis. | Inserir evidência verificável. |

 Revisão da sprint — 04/11/2026

Preencher após a demonstração:

- Requisitos da Atividade 1 atendidos:
- Requisitos da Atividade 2 atendidos:
- Testes e validações realizados:
- Entregáveis e registros:
- Pendências ou itens não aceitos:
- Aceite da Product Owner:
- Confirmação do envio dos dois ZIPs:

 Retrospectiva

Preencher com a equipe ao final da sprint:

- O que funcionou bem:
- O que precisa melhorar:
- Impedimentos encontrados:
- Ações de melhoria para a próxima sprint:
- Responsáveis e prazos das ações:

 11. Referências do projeto

- Repositório: sistema-biblioteca, de Thz081.
- Branch de trabalho: develop.
- Quadro Trello: Biblioteca Novaris Tech.
- Índice dos cards: tasks/trello-cards.json.
- Plano técnico: tasks/plan.md.
- Base integrada: Pull Request número 4.

 12. Histórico e manutenção

Este SPRINT.md substitui a seção provisória de planejamento, mantendo o próprio arquivo como documento Scrum da sprint.

Responsável pela atualização: Nicolly — Scrum Master e Product Owner.\
Regra de manutenção: atualizar situações, resultados, impedimentos e evidências somente após confirmação no Trello, no repositório ou no ambiente de execução.

## Histórico preservado

O documento da sprint anterior permanece em [docs/historico/SPRINT-2026-09-21-a-2026-10-05.md](docs/historico/SPRINT-2026-09-21-a-2026-10-05.md).

## Nota técnica de integração — 02/11/2026

O planejamento acima foi preservado; suas tabelas registram o planejamento original. A situação técnica verificada, os commits integrados, os resultados e os impedimentos atuais estão em [docs/devops/STATUS.md](docs/devops/STATUS.md), com evidências de runtime e release. Tacyo executou a integração e as verificações nesta revisão. Nicolly ainda deve atualizar acompanhamento, revisão, retrospectiva e aceite final; ZIPs e envio não foram concluídos por esta nota.
