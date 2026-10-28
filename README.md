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

## Imagens

- `logo-dalux-*.webp`: logo do cliente sem a linha "contra escorpião e baratas" e sem os dois ícones de proibido
  (recorte do JPG original em `_src/logo-original.jpg`, linhas 60 a 793).
- `tecnico-*.webp` e `alvo-622.webp`: recortes do criativo do próprio cliente (`_src/criativo-escorpiao.jpg`),
  sem o texto. A foto é de IA e o escudo no uniforme não é o logo da Dalux.
- `escorpiao-640.webp`: Pexels 33210385. `barata-640.webp`: Unsplash photo-1759379077720. Licença livre, sem crédito obrigatório.

## A confirmar com o cliente

- Cidade e bairros atendidos (título, descrição e dados do Google ainda dizem só "Mato Grosso do Sul").
- Garantia (tem? quantos dias?) e se emite certificado de dedetização para empresa.
- Anos de experiência, CNPJ, licença sanitária e responsável técnico.
- Fotos reais da equipe e do serviço para trocar as de banco e de IA.
- Domínio (canonical, og:image e schema apontam para `dalux-landing.vercel.app`).
