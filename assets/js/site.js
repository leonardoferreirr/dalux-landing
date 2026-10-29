// Dalux Dedetização · comportamento da página.
// Tudo é enfeite: sem este arquivo a página continua inteira e legível.
(function () {
  window.__dalux = 1;
  var doc = document.documentElement;
  var temIO = 'IntersectionObserver' in window;

  // 1. Entrada no scroll (.rv ganha .on quando aparece)
  var rv = document.querySelectorAll('.rv');
  if (!temIO) {
    rv.forEach(function (el) { el.classList.add('on'); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
      });
    }, { threshold: .15, rootMargin: '0px 0px -6% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  }

  // 2. Animação infinita só roda com a seção na tela
  if (temIO) {
    var casa = document.getElementById('casa-svg');
    var pausa = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        e.target.classList.toggle('pausa', !e.isIntersecting);
        if (casa && e.target.contains(casa) && casa.pauseAnimations) {
          e.isIntersecting ? casa.unpauseAnimations() : casa.pauseAnimations();
        }
      });
    }, { rootMargin: '120px 0px' });
    document.querySelectorAll('[data-anim]').forEach(function (el) { pausa.observe(el); });
  }

  // 3. Topo com vidro ao rolar + barra de progresso
  var topo = document.getElementById('topo');
  var barra = document.querySelector('.progresso i');
  var pedido = false;
  function rolar() {
    pedido = false;
    var y = window.scrollY, max = doc.scrollHeight - window.innerHeight;
    topo.classList.toggle('rolou', y > 8);
    doc.classList.toggle('fab', y > 520);
    if (barra) barra.style.setProperty('--p', max > 0 ? Math.min(1, y / max).toFixed(4) : 0);
  }
  window.addEventListener('scroll', function () {
    if (!pedido) { pedido = true; requestAnimationFrame(rolar); }
  }, { passive: true });
  rolar();

  // 4. Mira acompanha o mouse (só em mouse de verdade)
  var alvo = document.getElementById('alvo');
  if (alvo && window.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    var hero = document.getElementById('inicio'), mx = 0, my = 0, quadro = false;
    hero.addEventListener('pointermove', function (ev) {
      var r = hero.getBoundingClientRect();
      mx = ((ev.clientX - r.left) / r.width - .5) * 2;
      my = ((ev.clientY - r.top) / r.height - .5) * 2;
      if (!quadro) {
        quadro = true;
        requestAnimationFrame(function () {
          quadro = false;
          alvo.style.setProperty('--mx', mx.toFixed(3));
          alvo.style.setProperty('--my', my.toFixed(3));
        });
      }
    }, { passive: true });
    hero.addEventListener('pointerleave', function () {
      alvo.style.setProperty('--mx', 0); alvo.style.setProperty('--my', 0);
    });
  }

  // 5. Slideshow escorpião/barata atrás da mira: começa no primeiro sinal de gente (ou aos 12 s)
  if (alvo) {
    var gatilhos = ['pointermove', 'pointerdown', 'scroll', 'wheel', 'touchstart', 'keydown'];
    var roda = function () {
      alvo.classList.add('roda');
      gatilhos.forEach(function (g) { window.removeEventListener(g, roda); });
    };
    gatilhos.forEach(function (g) { window.addEventListener(g, roda, { passive: true }); });
    setTimeout(roda, 12000);
  }

  // 6. Mapa da casa: item da lista acende o número no desenho e vice-versa
  var itens = document.querySelectorAll('.mapa-lista li');
  var pontos = document.querySelectorAll('.hs');
  function acende(n) {
    itens.forEach(function (li) { li.classList.toggle('ativo', li.dataset.n === n); });
    pontos.forEach(function (g) { g.classList.toggle('ativo', g.dataset.n === n); });
  }
  itens.forEach(function (li) {
    li.addEventListener('mouseenter', function () { acende(li.dataset.n); });
    li.addEventListener('focus', function () { acende(li.dataset.n); });
    li.addEventListener('click', function () { acende(li.dataset.n); });
  });
  pontos.forEach(function (g) {
    g.addEventListener('click', function () {
      acende(g.dataset.n);
      var li = document.querySelector('.mapa-lista li[data-n="' + g.dataset.n + '"]');
      if (li && window.innerWidth < 900) li.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
  var lista = document.querySelector('.mapa-lista');
  if (lista) lista.addEventListener('mouseleave', function () { acende(''); });
})();
