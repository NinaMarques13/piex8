# 🚀 CapacitaLocal — Portal de Letramento Digital e Recursos Livres

[![ODS 4 - Educação de Qualidade](https://img.shields.io/badge/ODS-4_Educa%C3%A7%C3%A3o_de_Qualidade-c2192c?style=for-the-badge)](https://sdgs.un.org/goals/goal4)
[![ODS 8 - Trabalho Decente](https://img.shields.io/badge/ODS-8_Trabalho_Decente-a21942?style=for-the-badge)](https://sdgs.un.org/goals/goal8)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> **O CapacitaLocal** é um ecossistema digital e projeto de extensão universitária voltado para a inclusão digital, segurança financeira e autonomia de trabalhadores autônomos, feirantes, pequenos prestadores de serviço e microempreendedores (MEIs).

---

## 🎯 Sobre o Projeto

Muitos trabalhadores autônomos possuem smartphones, mas enfrentam barreiras para utilizar ferramentas digitais no gerenciamento de seus negócios, ficando vulneráveis a golpes digitais (como o golpe do Pix) ou perdendo oportunidades por falta de presença online.

O **CapacitaLocal** atua como um **Hub/Portal Web centralizador e intuitivo**, acessível diretamente via **QR Code** espalhados em pontos comunitários de alta confiança (igrejas, associações de bairro e feiras livres). O portal organiza, valida e disponibiliza materiais gratuitos, vídeos práticos, guias em PDF e ferramentas de gestão em uma interface leve e *mobile-first*.

---

## 🌐 Objetivos de Desenvolvimento Sustentável (ODS)

- **[ODS 4] Educação de Qualidade:** Curadoria de conteúdos educativos acessíveis, com linguagem direta e focados no desenvolvimento de habilidades digitais e práticas.
- **[ODS 8] Trabalho Decente e Crescimento Econômico:** Fortalecimento do microempreendedorismo local e promoção da segurança em transações financeiras digitais.

---

## 🔄 Fluxo de Funcionamento e Arquitetura

[ Cartaz / QR Code na Comunidade ]
                │
                ▼
[ Google Forms de Diagnóstico ] ─── (Métricas via Google Sheets)
                │
                ▼ (Redirecionamento Automático)
[ Hub Web CapacitaLocal ]
    ├── 💰 Finanças & Pix Seguro
    ├── 📱 WhatsApp Business & Divulgação
    └── 📦 Organização do Negócio & Modelos em PDF

1. **Acesso Sem Barreiras:** O usuário lê o QR Code no ponto de atendimento comunitário.
2. **Validação Rápida (Google Forms):** Coleta diagnóstica mínima (bairro e ramo de atuação) para geração de estatísticas de impacto.
3. **Acesso Instantâneo ao Hub:** Redirecionamento direto para a biblioteca de conteúdos gratuitos (sem necessidade de cadastros complexos ou senhas).

---

## 🛠️️ Tecnologias Utilizadas

- **Frontend:** HTML5 Semântico, Tailwind CSS / Bootstrap (*Mobile-first*)
- **Coleta de Métricas & Diagnóstico:** Google Forms & Google Sheets API
- **Hospedagem:** Vercel / GitHub Pages / Render
- **Design & Prototipação:** Figma

---

## 📂 Estrutura do Repositório

```bash
├── docs/             # Documentação acadêmica e relatórios de extensão
├── src/              # Código-fonte da aplicação Web (Hub)
│   ├── assets/       # Imagens, ícones e arquivos estáticos
│   ├── css/          # Estilização responsiva
│   ├── js/           # Scripts de navegação e filtros
│   └── index.html    # Página principal do Portal
└── README.md         # Documentação técnica do projeto