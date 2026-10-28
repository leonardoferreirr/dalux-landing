// Dalux Dedetização · entrada suave dos blocos abaixo da dobra.
// Só deslocamento (transform): sem JS, ou sem IntersectionObserver, tudo já aparece no lugar.
(function () {
  var itens = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window)) {
    for (var i = 0; i < itens.length; i++) itens[i].classList.add('on');
    return;
  }
  var io = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  for (var j = 0; j < itens.length; j++) io.observe(itens[j]);
})();
