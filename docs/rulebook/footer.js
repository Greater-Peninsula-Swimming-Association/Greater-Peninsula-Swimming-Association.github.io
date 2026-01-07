document.addEventListener("DOMContentLoaded", function() {
  const date = document.querySelector('.quarto-title-meta-contents .date').textContent;
  const footer = document.querySelector('.nav-footer-right');
  if (footer) {
    footer.setAttribute('data-date', date);
  }
});
