// ...existing code...
document.addEventListener("DOMContentLoaded", function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getCsrfToken() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        if (el && el.value) return el.value;
        return getCookie('csrftoken');
    }

    const csrftoken = getCsrfToken();
    if (!csrftoken) console.warn('CSRF token não encontrado — requisições POST podem falhar.');

    const deleteModalElement = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    let aluguelIdToDelete = null;

    // --- Fluxo com modal (se presente) ---
    if (deleteModalElement && window.bootstrap) {
        const deleteModal = new bootstrap.Modal(deleteModalElement);

        deleteModalElement.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget || null;
            aluguelIdToDelete = button && button.getAttribute ? button.getAttribute('data-aluguel-id') : null;
            const modalBody = deleteModalElement.querySelector('.modal-body p');
            if (modalBody) modalBody.innerHTML = `Você tem certeza que deseja <strong>excluir</strong> o Aluguel ID: ${aluguelIdToDelete}?`;
        });

        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', function () {
                if (!aluguelIdToDelete) {
                    console.error("ID do aluguel não encontrado para exclusão. Cancelando.");
                    return;
                }
                const deleteUrl = `/alugueis/excluir/${aluguelIdToDelete}/`;
                confirmDeleteBtn.disabled = true;
                confirmDeleteBtn.innerHTML = 'Excluindo...';

                fetch(deleteUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken || '',
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify({})
                })
                .then(response => {
                    confirmDeleteBtn.disabled = false;
                    confirmDeleteBtn.innerHTML = 'Excluir';

                    if (response.ok) {
                        deleteModal.hide();
                        // remover linha da tabela em vez de reload para melhor UX
                        const btn = document.querySelector(`[data-aluguel-id="${aluguelIdToDelete}"]`);
                        const tr = btn && btn.closest('tr');
                        if (tr) tr.remove();
                        return;
                    }
                    // tenta ler mensagem do servidor
                    return response.text().then(text => {
                        let msg = 'Erro desconhecido.';
                        try { msg = JSON.parse(text).message || JSON.parse(text).error || text; } catch (e) { msg = text || msg; }
                        alert('Falha na exclusão: ' + msg);
                    });
                })
                .catch(error => {
                    confirmDeleteBtn.disabled = false;
                    confirmDeleteBtn.innerHTML = 'Excluir';
                    alert('Um erro de rede ocorreu. Verifique sua conexão.');
                    console.error('Erro de rede:', error);
                });
            });
        }
    }

    // --- Fluxo direto sem modal: clique em .btn-delete faz a requisição ---
    document.addEventListener('click', function (event) {
        const btn = event.target.closest && event.target.closest('.btn-delete');
        if (!btn) return;

        // Se modal existe e foi usado, ignore aqui (evita duplicidade)
        if (deleteModalElement) return;

        event.preventDefault();

        const aluguelId = btn.dataset.aluguelId || btn.getAttribute('data-aluguel-id');
        const deleteUrl = btn.dataset.deleteUrl || (aluguelId ? `/alugueis/excluir/${aluguelId}/` : null);

        if (!deleteUrl) {
            console.error('URL de exclusão não encontrada no botão.');
            return;
        }

        // sem modal — opcional: confirmar com confirm() ou não (conforme sua escolha)
        // if (!confirm('Deseja realmente excluir este aluguel?')) return;

        btn.disabled = true;

        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken || '',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            btn.disabled = false;
            if (response.ok) {
                const tr = btn.closest('tr');
                if (tr) tr.remove();
                return;
            }
            return response.text().then(text => {
                let msg = 'Erro desconhecido.';
                try { msg = JSON.parse(text).message || JSON.parse(text).error || text; } catch (e) { msg = text || msg; }
                alert('Falha na exclusão: ' + msg);
            });
        })
        .catch(err => {
            btn.disabled = false;
            alert('Erro ao excluir: ' + (err.message || 'Erro de rede.'));
            console.error(err);
        });
    });

});
// ...existing code...