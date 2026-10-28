# Dalux Dedetização · landing

Site da Dalux Dedetização (escorpião e barata, DDD 67, Mato Grosso do Sul). Primeiro cliente da oferta
"site grátis + R$50/mês de hospedagem".

Estático puro (HTML, CSS e JS), sem framework. Deploy na Vercel com `framework: null`.

## Rodar local

    npx serve -l 8890 .

## Editar

- **CSS:** a fonte da verdade é `assets/css/site.css`, mas o navegador lê a cópia inline no `index.html`.
  Depois de editar, rode `python3 build.py` (ele também carimba o `site.js` com hash).
- **WhatsApp:** número `5567993106147` e mensagem pronta ficam em `obrigado.html` (`NUM` e `TXT`).
  Todo botão aponta para `obrigado?c=<contexto>` (sem `.html`: a URL limpa da Vercel perderia a query),
  que dispara `whatsapp_click` no dataLayer antes de abrir a conversa. Pronto para o GTM, ainda não instalado.

## Imagens (v2, "na mira")

- `logo-dalux-*.webp`: logo do cliente sem a linha "contra escorpião e baratas" e sem os dois ícones de proibido
  (recorte do JPG original em `_src/logo-original.jpg`, linhas 60 a 793).
- `esc-topo-*.webp` e `esc-lado-*.webp`: escorpião-amarelo (Tityus serrulatus) de Alexandre S. Michelotto,
  Wikimedia Commons, **CC BY-SA 4.0**: o crédito no rodapé é obrigatório, não tirar.
- `barata-topo-*.webp`: Unsplash photo-1611773236409 (licença livre, sem crédito obrigatório).
- Recorte com o Vision da Apple (`swift _src/lift.swift entrada saida.png`) e limpeza do papel branco que sobra
  entre as patas (pixels claros e sem cor viram transparentes). Originais e recortes em `_src/v2/`.
- A mira, as fitas de "cuidado", a cadeia barata → escorpião → casa e o corte da casa são SVG/CSS no próprio HTML.

## A confirmar com o cliente

- Cidade e bairros atendidos (título, descrição e dados do Google ainda dizem só "Mato Grosso do Sul").
- Garantia (tem? quantos dias?) e se emite certificado de dedetização para empresa.
- Anos de experiência, CNPJ, licença sanitária e responsável técnico.
- Fotos reais da equipe e do serviço (hoje o site não tem foto de pessoa).
- Domínio (canonical, og:image e schema apontam para `dalux-landing.vercel.app`).
