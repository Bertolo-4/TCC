document.addEventListener('DOMContentLoaded', function() {
    // --- Seletores de Elementos ---
    const tabs = document.querySelectorAll('.tab-item');
    const panels = document.querySelectorAll('.panel');
    const runButton = document.querySelector('.run-button');
    const outputArea = document.querySelector('.output-area');
    const codeEditorArea = document.querySelector('.code-editor-area');
    const enunciadoPanel = document.querySelector('.panel-enunciado');

    const codeEditor = document.createElement('textarea');
    codeEditor.setAttribute('id', 'code-editor');
    codeEditor.setAttribute('spellcheck', 'false');
    codeEditorArea.appendChild(codeEditor);
    
    const urlParams = new URLSearchParams(window.location.search);
    const exercicioId = urlParams.get('id');

    async function loadExercicio() {
        // Mostra o "Carregando..."
        document.body.classList.add('loading');

        try {
            if (!exercicioId) {
                throw new Error('ID do exercício não encontrado na URL.');
            }

            // --- CÓDIGO CORRETO PARA BUSCAR O EXERCÍCIO ---
            // Faz a chamada GET correta para buscar os dados do exercício.
            const response = await fetch(`/api/exercicio/${exercicioId}`);
            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }
            const data = await response.json();
            
            enunciadoPanel.innerHTML = `
                <h2>${data.titulo}</h2>
                <p>${data.enunciado_adaptado.replace(/\n/g, '<br>')}</p>
            `;

            codeEditor.value = data.template_codigo || '// Escreva seu código aqui.';

        } catch (error) {
            console.error('Erro ao carregar exercício:', error);
            enunciadoPanel.innerHTML = `
                <h2>Erro ao carregar exercício</h2>
                <p>${error.message}</p>
            `;
            codeEditor.value = '// Erro ao carregar o exercício.';
        } finally {
            // Esconde o "Carregando..." e mostra o conteúdo
            document.body.classList.remove('loading');
        }
    }

    // Chama a função para carregar os dados da página
    loadExercicio();

    // --- Lógica para troca de abas ---
    function switchTab(targetTab) {
        tabs.forEach(tab => tab.classList.remove('active'));
        panels.forEach(panel => panel.classList.remove('active'));
        targetTab.classList.add('active');
        const targetPanel = document.querySelector(`.panel[data-panel="${targetTab.dataset.tab}"]`);
        if (targetPanel) {
            targetPanel.classList.add('active');
        }
    }
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab));
    });

    // --- Lógica do botão "Run" ---
    runButton.addEventListener('click', async () => {
        // A variável com o código do aluno é criada APENAS AQUI
        const code = codeEditor.value; 
        if (!code.trim()) {
            alert('Por favor, insira algum código.');
            return;
        }

        outputArea.textContent = 'Executando e corrigindo...';
        switchTab(document.querySelector('.tab-item[data-tab="saida"]'));

        try {
            // Envia o código para a rota de correção
           const response = await fetch(`/api/exercicio/${exercicioId}/run-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ codigo: code }), // A variável 'code' é usada aqui
            });
            alert(code);
            const data = await response.json();
            if (!response.ok) {
                alert(response.status);
                throw new Error(data.detail || `Erro na API: ${response.status}`);
            
            }

            outputArea.textContent = data.output;
        } catch (error) {
            console.error('Erro ao executar código:', error);
            outputArea.textContent = `Erro: ${error.message}`;
        }
    });
    
    // --- Define a aba ativa inicial ---
    const initialActiveTab = document.querySelector('.tab-item.active');
    if (initialActiveTab) {
        switchTab(initialActiveTab);
    }
});