# DevOps — avanço em 28/10/2026

Responsável: Tacyo Henrique. Esta é uma fotografia da preparação técnica; o Trello continua sendo o acompanhamento dos cards.

## Preparação concluída

- Namespace `biblioteca` criado no Docker Desktop, sem alterar os recursos da API de data e hora.
- Manifestos de ConfigMap, Deployment com duas réplicas e Service preparados em `k8s/`.
- Manifestos aceitos pelo servidor Kubernetes em dry-run, sem criar Pods da biblioteca.
- Procedimentos de implantação, acesso, escala e rollback documentados em `k8s/README.md`.
- Evidência real da preparação em `evidencias/2026-10-28-preparacao.txt`.

## Liberações necessárias

| Card de Tacyo | O que falta para concluir |
|---|---|
| Atividade 1 · 04 — publicar imagem inicial | Pedro concluir a aplicação unificada e Kerolyn construir/testar a imagem. Depois publicar a tag real, registrar digest e verificar acesso do cluster. |
| Atividade 1 · 06 — Deployment e Service | Confirmar contrato de porta/imagem, disponibilizar banco compartilhado e Secret; então aplicar e verificar os dois Pods e acesso HTTP. A preparação dos YAMLs está pronta. |
| Atividade 2 · 01 — escala | Biblioteca implantada, saudável e com dados compartilhados; executar e registrar 2→4→2. |
| Atividade 2 · 02 — recuperação | Biblioteca saudável; excluir um Pod, comprovar substituição e preservação dos dados. |
| Atividade 2 · 04 — atualização | Pedro entregar a alteração e Kerolyn revisar a nova imagem; publicar e verificar rollout. |
| Atividade 2 · 05 — rollback | Existência de versão anterior e atualização real; restaurar a revisão correta e conferir a aplicação. |

O provisionamento do banco e dos segredos deve seguir a configuração acordada com Pedro e a revisão de Kerolyn. Não foram inventadas credenciais, publicadas imagens antigas separadas ou executados exercícios com outra aplicação. Nenhum card dependente está concluído apenas porque seus comandos estão documentados.

## Divisão preservada

Esta preparação não altera aplicação, Dockerfiles, pipeline de segurança ou SPRINT.md. Requisitos/aceite permanecem com Gabriel, aplicação com Pedro, imagem/segurança com Kerolyn e Scrum/PO com Nicolly. A base do fork já foi marcada como concluída por Tacyo.

## Ideia reservada para depois

Tacyo pediu para guardar a ideia de preparar slides e falas para a apresentação futura, explicando os entregáveis e a participação de cada integrante. Não iniciar essa produção agora; definir o formato quando houver resultados reais da biblioteca para demonstrar.
