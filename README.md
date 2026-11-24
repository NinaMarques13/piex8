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
- **Coleta de Métricas & Diagnóstico:** Google Forms & Google Sheets
- **Hospedagem:** GitHub Pages via GitHub Actions
- **Design & Prototipação:** Figma

### Atualização do catálogo público

O portal é estático e aberto. O catálogo publicado fica em `src/resources.json` e pode ser atualizado a partir de uma planilha `.xlsx`:

```bash
python3 scripts/import_resources.py "PIEX 7.xlsx"
```

O importador usa nome, área, plataforma, categoria, formato, carga horária e link de acesso. As colunas de conclusão e notas não são publicadas. Os conteúdos são organizados em negócios, carreiras e crescimento pessoal; registros sem link válido continuam visíveis, mas sem botão de acesso.

Essa importação gera uma cópia estática: alterações futuras na planilha só aparecem no portal depois de executar o comando novamente e publicar o `resources.json` atualizado. Para testar localmente, sirva a pasta `src` por HTTP (por exemplo, `python3 -m http.server 8000 --directory src`).

### Deploy no GitHub Pages

1. No repositório, acesse **Settings → Pages** e selecione **GitHub Actions** como origem do deploy.
2. Envie as alterações para a branch `main` ou execute manualmente o workflow **Deploy portal to GitHub Pages** na aba **Actions**.
3. O workflow valida o catálogo e publica somente a pasta `src/`. O arquivo Excel de origem não faz parte do site publicado.

Após o primeiro deploy, o portal ficará disponível em `https://ninamarques13.github.io/piex8/`.

---

## 📂 Estrutura do Repositório

```bash
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
├── scripts/
│   └── import_resources.py
├── src/
│   ├── index.html
│   └── resources.json
└── README.md