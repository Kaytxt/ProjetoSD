document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Previne o comportamento padrão do link (o "teletransporte")
            event.preventDefault();

            // Pega o ID da seção do atributo href (ex: '#localizacao')
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                // Rola a página suavemente para a seção alvo
                window.scrollTo({
                    top: targetSection.offsetTop,
                    behavior: 'smooth'
                });
            }

            // Remove a classe 'active' de todos os links
            navLinks.forEach(item => {
                item.classList.remove('active');
            });

            // Adiciona a classe 'active' ao link clicado
            this.classList.add('active');
        });
    });
});