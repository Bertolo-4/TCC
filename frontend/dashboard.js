document.addEventListener('DOMContentLoaded', () => {
    const cardsContainer = document.getElementById('cards-container');
    const progressListContainer = document.getElementById('progress-list-container');
    const apiUrl = '/api/exercicios';

    // --- Validação inicial dos containers ---
    if (!cardsContainer || !progressListContainer) {
        console.error('Erro: Um dos containers (cards ou lista de progresso) não foi encontrado no HTML.');
        return;
    }

    // --- Lógica para buscar e renderizar os exercícios ---
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Falha na resposta da rede.');
            }
            return response.json();
        })
        .then(exercicios => {
            cardsContainer.innerHTML = '';
            progressListContainer.innerHTML = '';

            if (exercicios.length === 0) {
                cardsContainer.innerHTML = '<p>Nenhum exercício disponível.</p>';
                progressListContainer.innerHTML = '<p>Nenhum progresso para exibir.</p>';
                return;
            }

            const colors = ['orange', 'green', 'purple', 'red', 'blue', 'cyan', 'yellow'];

            // Percorre a lista COMPLETA de exercícios
            exercicios.forEach((exercicio, index) => {
                const colorClass = colors[index % colors.length];

                // --- Parte 1: Cria os CARDS (APENAS OS 3 PRIMEIROS) ---
                // A variável 'index' começa em 0, então a condição (index < 3)
                // será verdadeira para os itens 0, 1 e 2.
                if (index < 3) {
                    const cardElement = document.createElement('a');
                    cardElement.href = `/telas_html/resolverExer.html?id=${exercicio.id_exercicio}`;
                    cardElement.style.textDecoration = 'none';
                    cardElement.style.color = 'inherit';
                    cardElement.innerHTML = `
                        <article class="card">
                            <div class="title">${exercicio.titulo}</div>
                            <div class="progress">
                                <div class="fill fill-${colorClass}" style="width:0%"></div>
                            </div>
                        </article>
                    `;
                    cardsContainer.appendChild(cardElement);
                }

                // --- Parte 2: Cria a LISTA DE PROGRESSO (PARA TODOS OS EXERCÍCIOS) ---
                // Este bloco de código executa para cada exercício, sem limite.
                const listItemLink = document.createElement('a');
                listItemLink.href = `/telas_html/resolverExer.html?id=${exercicio.id_exercicio}`;
                listItemLink.style.textDecoration = 'none';
                listItemLink.style.color = 'inherit';
                listItemLink.innerHTML = `
                    <div class="list-item" role="listitem">
                        <div class="item-icon c-${colorClass}" aria-hidden="true">Q${index + 1}</div>
                        <div class="item-main">
                            <div class="item-title">${exercicio.titulo}</div>
                            <div class="item-progress" aria-hidden="true">
                                <div class="fill fill-${colorClass}" style="width:0%"></div>
                            </div>
                        </div>
                       
                        <button class="menu-btn" aria-label="Mais opções">⋯</button>
                    </div>
                `;
                progressListContainer.appendChild(listItemLink);
            });
        })
        .catch(error => {
            console.error('Erro ao buscar ou processar os exercícios:', error);
            cardsContainer.innerHTML = `<p style="color: red;">Falha ao carregar os exercícios.</p>`;
            progressListContainer.innerHTML = '';
        });

    
    // --- Lógica de Eventos para os botões de Ação (Editar e Excluir) ---
    // Colocamos essa lógica aqui para que ela não dependa diretamente do fetch,
    // apenas escute os eventos no container pai.

    progressListContainer.addEventListener('click', (event) => {
        const target = event.target;

        // Lógica para o botão de Excluir
        if (target.classList.contains('delete-btn')) {
            const exercicioId = target.dataset.id;
            if (confirm('Tem certeza de que deseja excluir este exercício?')) {
                fetch(`/api/exercicios/${exercicioId}`, { method: 'DELETE' })
                    .then(response => {
                        if (response.ok) {
                            target.closest('a').remove(); // Remove o item da lista na tela
                        } else {
                            alert('Falha ao excluir. O exercício pode ter respostas associadas.');
                        }
                    })
                    .catch(err => console.error('Erro de rede ao excluir:', err));
            }
        }

       
    });
});