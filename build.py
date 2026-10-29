#!/usr/bin/env python3
"""Injeta assets/css/site.css minificado dentro do <head> do index.html e gera
o que buscadores e assistentes de IA leem: o schema (JSON-LD), robots.txt,
sitemap.xml e llms.txt.

Por que inline: servido como arquivo, o CSS bloqueia a primeira pintura no
celular e derruba o Lighthouse. Inline, ele chega junto com o HTML.

A fonte da verdade continua sendo assets/css/site.css. O FAQ, os passos e os
esconderijos do schema e do llms.txt saem do próprio index.html, então basta
editar a página e rodar este script que os dois acompanham.

O domínio oficial mora só em DOMINIO. Ao conectar o domínio próprio, troque ali
e rode o build: canonical, og, schema, sitemap, robots e llms.txt passam a
apontar para ele, e o endereço .vercel.app ganha um 301 para o domínio novo.
No ar desde 29/10/2026 em www.dedetizacaoraiox.com.br (o endereço sem www já
redireciona para o www pela própria Vercel).

    python3 build.py
"""
import hashlib, json, re, sys
from datetime import date
from html import unescape
from pathlib import Path

RAIZ = Path(__file__).parent
CSS  = RAIZ / "assets/css/site.css"
JS   = RAIZ / "assets/js/site.js"
HTML = RAIZ / "index.html"

DOMINIO = "https://www.dedetizacaoraiox.com.br"
VERCEL  = "dedetizacaoraiox.vercel.app"

NOME      = "Dedetização Raio X"
FONE      = "+55 67 99310-6147"
FONE_VER  = "(67) 99310-6147"
RESUMO    = ("Dedetização em Campo Grande (MS) contra escorpião, barata de esgoto e "
             "baratinha francesinha, para casas, apartamentos, condomínios, comércios e indústrias.")
SERVICOS = [
    ("Dedetização contra escorpião",
     "Aplicação nos pontos onde o escorpião e a barata, que é a comida dele, se escondem: "
     "ralos, caixas de gordura e de esgoto, frestas, rodapés, entulho e terreno."),
    ("Dedetização contra barata de esgoto",
     "Tratamento de ralos e caixas de gordura e de esgoto, por onde a barata sobe para dentro de casa."),
    ("Dedetização contra barata francesinha",
     "Gel aplicado nas frestas dos armários, embaixo da pia, atrás da geladeira e do fogão "
     "e nos aparelhos da cozinha, onde a baratinha vive."),
    ("Dedetização para condomínios, comércios e indústrias",
     "Atendimento de áreas maiores, com visita e horário combinados para não atrapalhar o funcionamento."),
]


def minificar(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    css = re.sub(r"\n{2,}", "\n", css)
    css = re.sub(r"\s*([{}:;,>])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


def reancorar(css: str) -> str:
    """No arquivo, `../fonts/` sai de assets/css/ e chega em assets/fonts/.
    Inline no index.html, que esta na raiz, o mesmo caminho vira /fonts/ e da
    404: as fontes somem e a pagina cai no fallback sem avisar."""
    return re.sub(r"""url\((['"]?)\.\./""", r"url(\1assets/", css)


def versionar_script(html: str) -> tuple:
    """Carimba site.js com o hash do proprio conteudo.

    O Vercel serve /assets/ com max-age de um ano e immutable, o que so e
    seguro quando o nome do arquivo muda a cada versao. Com nome fixo, quem ja
    visitou fica um ANO com o JS velho."""
    if not JS.exists():
        return html, "-"
    v = hashlib.sha256(JS.read_bytes()).hexdigest()[:10]
    return re.sub(r'(src="assets/js/site\.js)(\?v=[a-f0-9]+)?"', rf'\1?v={v}"', html), v


def texto(fragmento: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", fragmento))).strip()


def carimbar_dominio(html: str) -> str:
    """Troca o domínio que está no canonical pelo de DOMINIO em toda a página."""
    m = re.search(r'<link rel="canonical" href="(https://[^/"]+)/">', html)
    if not m:
        raise SystemExit('canonical nao encontrado no index.html')
    return html.replace(m.group(1), DOMINIO)


def conteudo(html: str) -> dict:
    """O que a página diz, lido dela mesma: FAQ, passos, esconderijos e a ficha."""
    def secao(id_):
        ini = html.index(f'id="{id_}"')
        return html[ini:html.index("</section>", ini)]
    lista = lambda id_: [(texto(a), texto(b)) for a, b in
                         re.findall(r"<h3>(.*?)</h3><p>(.*?)</p>", secao(id_))]
    return {
        "faq": [(texto(q), texto(r)) for q, r in
                re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", secao("duvidas"), flags=re.S)],
        "passos": lista("como-funciona"),
        "escorpiao": lista("esconderijos"),
        "baratinha": lista("baratinha"),
        "veneno": [texto(p) for p in re.findall(r'<ol class="motivos">(.*?)</ol>', html, flags=re.S)[0].split("</li>") if texto(p)],
    }


def schema(c: dict) -> str:
    S = DOMINIO
    cidade = {"@type": "City", "name": "Campo Grande",
              "sameAs": "https://pt.wikipedia.org/wiki/Campo_Grande_(Mato_Grosso_do_Sul)"}
    grafo = [
        {"@type": "LocalBusiness", "@id": f"{S}/#empresa", "name": NOME, "description": RESUMO,
         "url": f"{S}/", "telephone": FONE,
         "image": f"{S}/assets/img/og-raiox.jpg", "logo": f"{S}/assets/img/logo-raiox-720.webp",
         "address": {"@type": "PostalAddress", "addressLocality": "Campo Grande",
                     "addressRegion": "MS", "addressCountry": "BR"},
         "areaServed": cidade,
         "contactPoint": {"@type": "ContactPoint", "telephone": FONE,
                          "contactType": "customer service", "availableLanguage": "pt-BR"},
         "knowsAbout": ["dedetização", "controle de escorpião", "escorpião-amarelo",
                        "controle de baratas", "barata de esgoto", "barata francesinha"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Serviços de dedetização",
                             "itemListElement": [
                                 {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n,
                                  "description": d, "serviceType": "Dedetização",
                                  "areaServed": cidade, "provider": {"@id": f"{S}/#empresa"}}}
                                 for n, d in SERVICOS]}},
        {"@type": "WebSite", "@id": f"{S}/#site", "url": f"{S}/", "name": NOME,
         "inLanguage": "pt-BR", "publisher": {"@id": f"{S}/#empresa"}},
        {"@type": "WebPage", "@id": f"{S}/#pagina", "url": f"{S}/",
         "name": "Dedetização em Campo Grande contra escorpião e barata",
         "isPartOf": {"@id": f"{S}/#site"}, "about": {"@id": f"{S}/#empresa"}, "inLanguage": "pt-BR",
         "primaryImageOfPage": {"@type": "ImageObject", "url": f"{S}/assets/img/og-raiox.jpg"}},
        {"@type": "HowTo", "@id": f"{S}/#como-funciona", "name": "Como funciona a dedetização",
         "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t}
                  for i, (n, t) in enumerate(c["passos"], 1)]},
        {"@type": "FAQPage", "@id": f"{S}/#duvidas", "isPartOf": {"@id": f"{S}/#pagina"},
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in c["faq"]]},
    ]
    js = json.dumps({"@context": "https://schema.org", "@graph": grafo},
                    ensure_ascii=False, separators=(",", ":"))
    return js.replace("</", "<\\/")


def llms(c: dict) -> str:
    S = DOMINIO
    lin = [f"# {NOME}", "", f"> {RESUMO} Orçamento pelo WhatsApp {FONE_VER}.", "",
           "A Raio X trata o escorpião e a barata juntos: a barata é a comida do escorpião, então "
           "não adianta matar um e deixar o outro em casa. A aplicação é feita onde eles se escondem, "
           "e depois do serviço o cliente recebe as orientações de prevenção.", "",
           "## Serviços", ""]
    lin += [f"- **{n}:** {d}" for n, d in SERVICOS]
    lin += ["", "## Como funciona", ""]
    lin += [f"{i}. **{n}.** {t}" for i, (n, t) in enumerate(c["passos"], 1)]
    lin += ["", "## Onde o escorpião se esconde", ""]
    lin += [f"- **{n}:** {t}" for n, t in c["escorpiao"]]
    lin += ["", "## Onde a baratinha francesinha se esconde", ""]
    lin += [f"- **{n}:** {t}" for n, t in c["baratinha"]]
    lin += ["", "## Por que o veneno de mercado não resolve a francesinha", ""]
    lin += [f"- {t}" for t in c["veneno"]]
    lin += ["", "## Perguntas frequentes", ""]
    for q, r in c["faq"]:
        lin += [f"### {q}", "", r, ""]
    lin += ["## Contato", "",
            f"- WhatsApp: {FONE_VER}",
            f"- Pedir orçamento: {S}/obrigado?c=llms",
            f"- Site: {S}/",
            "- Área atendida: Campo Grande, Mato Grosso do Sul, Brasil", ""]
    return "\n".join(lin)


def extras(c: dict, mudou: bool) -> None:
    (RAIZ / "robots.txt").write_text(
        "# Buscadores e assistentes de IA podem ler o site inteiro.\n"
        "# A página obrigado fica de fora do índice pelo noindex dela, não por aqui.\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")

    mapa = RAIZ / "sitemap.xml"
    antes = re.search(r"<lastmod>([\d-]+)</lastmod>", mapa.read_text()) if mapa.exists() else None
    dia = date.today().isoformat() if mudou or not antes else antes.group(1)
    mapa.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{DOMINIO}/</loc><lastmod>{dia}</lastmod></url>\n"
        "</urlset>\n", encoding="utf-8")

    (RAIZ / "llms.txt").write_text(llms(c), encoding="utf-8")


def redirecionar_vercel() -> None:
    """Com domínio próprio, o .vercel.app vira cópia da página. O 301 evita
    que o Google indexe os dois endereços."""
    arq = RAIZ / "vercel.json"
    cfg = json.loads(arq.read_text(encoding="utf-8"))
    outros = [r for r in cfg.get("redirects", [])
              if not any(h.get("value") == VERCEL for h in r.get("has", []))]
    if VERCEL not in DOMINIO:
        # a raiz vai à parte: na Vercel o "/:path*" não pegou a página inicial
        host = [{"type": "host", "value": VERCEL}]
        outros += [{"source": "/", "has": host, "destination": f"{DOMINIO}/", "permanent": True},
                   {"source": "/:path*", "has": host, "destination": f"{DOMINIO}/:path*", "permanent": True}]
    if outros:
        cfg["redirects"] = outros
    else:
        cfg.pop("redirects", None)
    novo = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"
    if novo != arq.read_text(encoding="utf-8"):
        arq.write_text(novo, encoding="utf-8")


def main() -> int:
    if not CSS.exists() or not HTML.exists():
        print("assets/css/site.css ou index.html nao encontrado", file=sys.stderr)
        return 1

    enxuto = reancorar(minificar(CSS.read_text(encoding="utf-8")))
    html = HTML.read_text(encoding="utf-8")

    if re.search(r"""url\((['"]?)\.\./""", enxuto):
        print("ainda ha caminho relativo ../ no CSS inline", file=sys.stderr)
        return 1

    ini, fim = html.find("<style>"), html.find("</style>")
    if ini == -1 or fim == -1:
        print("bloco <style> nao encontrado no index.html", file=sys.stderr)
        return 1

    novo = carimbar_dominio(html[:ini] + "<style>" + enxuto + html[fim:])
    c = conteudo(novo)
    novo, n = re.subn(r'(<script type="application/ld\+json" id="schema">).*?(</script>)',
                      lambda m: m.group(1) + schema(c) + m.group(2), novo, flags=re.S)
    if n != 1:
        print('bloco <script id="schema"> nao encontrado no index.html', file=sys.stderr)
        return 1
    novo, versao = versionar_script(novo)

    mudou = novo != html
    if mudou:
        HTML.write_text(novo, encoding="utf-8")
    extras(c, mudou)
    redirecionar_vercel()
    print(f"css -> {len(enxuto)} B | index.html {len(novo)} B | site.js?v={versao} | "
          f"faq {len(c['faq'])} | {DOMINIO}" + ("" if mudou else " | html sem mudança"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
