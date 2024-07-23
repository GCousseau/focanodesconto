document.addEventListener('DOMContentLoaded', function() {
    const ITEMS_PER_PAGE = 16;
    let currentPage = 1;
    let totalItems = 0;
    let allItems = [];

    function carregarPromocoes(page = 1, searchQuery = '') {
        fetch('promocoes.json')
            .then(response => response.json())
            .then(data => {
                allItems = data;
                totalItems = data.length;

                const filteredItems = data.filter(promocao => 
                    promocao.nome.toLowerCase().includes(searchQuery.toLowerCase())
                );

                const start = (page - 1) * ITEMS_PER_PAGE;
                const end = start + ITEMS_PER_PAGE;
                const itemsToShow = filteredItems.slice(start, end);

                const promocoesContainer = document.getElementById('promocoes');
                promocoesContainer.innerHTML = '';

                itemsToShow.forEach(promocao => {
                    const card = document.createElement('div');
                    card.className = 'promocao-card';

                    card.innerHTML = `
                        <div class="promocao-header">
                            <span class="mercado">${promocao.mercado}</span>
                            <span class="tempo">${promocao.tempo}</span>
                        </div>
                        <div class="promocao-body">
                            <img src="${promocao.imagem}" alt="${promocao.nome}">
                            <h3>${promocao.nome}</h3>
                            <p>A partir de: <span class="preco">${promocao.preco}</span></p>
                            <p>${promocao.parcelas}</p>
                            <p>${promocao.porcentagem}</p>
                            <p>${promocao.avaliacao}</p>
                        </div>
                        <div class="promocao-footer">
                            <button onclick="window.open('${promocao.link}', '_blank')">Pegar promoção</button>
                        </div>
                    `;
                    promocoesContainer.appendChild(card);
                });

                atualizarPaginas(page, filteredItems.length);
            })
            .catch(error => {
                console.error('Erro ao carregar promoções:', error);
                const promocoesContainer = document.getElementById('promocoes');
                const errorMessage = document.createElement('p');
                errorMessage.textContent = 'Erro ao carregar promoções. Por favor, tente novamente mais tarde.';
                promocoesContainer.appendChild(errorMessage);
            });
    }

    function atualizarPaginas(currentPage, filteredTotalItems) {
        const totalPages = Math.ceil(filteredTotalItems / ITEMS_PER_PAGE);
        const paginationContainer = document.getElementById('pagination');
        paginationContainer.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            if (i === currentPage) {
                button.classList.add('disabled');
                button.disabled = true;
            }
            button.addEventListener('click', () => {
                carregarPromocoes(i, document.getElementById('search-input').value);
            });
            paginationContainer.appendChild(button);
        }
    }

    document.getElementById('search-button').addEventListener('click', () => {
        carregarPromocoes(1, document.getElementById('search-input').value);
    });

    carregarPromocoes(currentPage);
});