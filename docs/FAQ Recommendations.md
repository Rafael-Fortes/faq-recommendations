---
creationDate: 2025/03/23
modificationDate: Sunday 23rd March 2025 00:35:56
tags:
  - Project
status: Stuck
docType: Roadmap
---
## FAQ Recommendations: Respostas Rápidas para seus Usuários

Empresas frequentemente utilizam FAQs (Frequently Asked Questions) para responder às dúvidas mais comuns de seus usuários de forma eficiente, evitando a necessidade de contato direto com bots ou atendentes humanos. O projeto FAQ Recommendations é uma aplicação que visa otimizar esse processo, **sugerindo a FAQ mais relevante com base na pergunta do usuário.**

## Funcionamento do FAQ Recommendations

O FAQ Recommendations utiliza [[Como um LLM funciona|modelos de linguagem]] para gerar [[O que é um Embedding|embeddings]] (representações vetoriais) das FAQs. Ao receber uma pergunta do usuário, o sistema realiza uma [[Como a Busca Semântica funciona|busca semântica]], comparando a pergunta com os embeddings das FAQs. O resultado é uma lista ordenada das FAQs mais semanticamente similares à pergunta, permitindo que o usuário encontre a resposta mais adequada de forma rápida e intuitiva.

## Backend Roadmap: Gerenciamento e Busca de FAQs

Este roadmap define as funcionalidades do backend para o gerenciamento e busca de FAQs.

**[[Documento de Requisitos Gerenciamento de FAQs|Gerenciamento de FAQs]]:**
*   [x] **Importação de FAQs:** Implementar a funcionalidade de adicionar uma nova lista de FAQs a partir de um arquivo CSV. Se a FAQ não existir, ela deverá ser criada.
*   [x] **Adição de Itens a FAQs Existentes:** Implementar a funcionalidade de adicionar um novo item a uma lista de FAQ já existente. Se a FAQ não existir, ela deverá ser criada.
*   [x] **Leitura de FAQs:** Implementar a funcionalidade de ler uma lista de FAQ específica.
*   [x] **Remoção de FAQs:** Implementar a funcionalidade de remover uma lista de FAQ completa.
*   [ ] **Remoção de Itens de FAQs:** Implementar a funcionalidade de remover um item específico de uma lista de FAQ.

**[[Documento de Requisitos Busca de FAQs|Rota de Busca de FAQs:]]**
*   [ ] **Busca Semântica de FAQs:** Implementar uma rota que, dado uma pergunta do usuário, o identificador da FAQ desejada (opcional) e o número `n` de FAQs a serem retornadas, retorne uma lista das `n` FAQs mais relevantes semanticamente à pergunta.
