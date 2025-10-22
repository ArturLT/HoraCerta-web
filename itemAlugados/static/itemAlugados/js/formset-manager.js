document.addEventListener("DOMContentLoaded", () => {
    const addButton = document.getElementById("addItemBtn");
    const container = document.getElementById("itemsContainer");
    const form = document.getElementById("aluguelForm");
    const totalFormsInput = document.querySelector('[name$="-TOTAL_FORMS"]'); 
    
    const dataEntrega = document.getElementById("id_data_inicio"); 
    const dataDevolucao = document.getElementById("id_data_fim"); 

    const emptyFormTemplateSource = document.getElementById("emptyFormTemplate");
    const baseRow = emptyFormTemplateSource ? emptyFormTemplateSource.querySelector('.item-form-row') : null;

    if (!baseRow || !totalFormsInput) {
        console.error("ERRO FATAL: Elementos essenciais do Formset não encontrados. Verifique o HTML e os IDs.");
        if (addButton) addButton.disabled = true;
        return; 
    }

    const totalPreview = document.createElement("div");
    totalPreview.classList.add("total-preview");

    const formActions = form.querySelector(".form-actions");
    if (formActions) {
        formActions.insertAdjacentElement("beforebegin", totalPreview);
    } else {
        form.appendChild(totalPreview); 
    }

    addButton.addEventListener("click", () => {
        let formCount = Number.parseInt(totalFormsInput.value, 10);
        const newRow = baseRow.cloneNode(true); 
        newRow.style.display = 'flex'; 
        
        const prefixRegex = /__prefix__/g;
        const newIndex = formCount; 
        const indexPrefix = `itemalugado_set-${newIndex}-`;

        // Atualiza os nomes e IDs
        newRow.querySelectorAll('[name],[id],[for]').forEach((el) => {
            if (el.name) el.name = el.name.replace(prefixRegex, indexPrefix);
            if (el.id) el.id = el.id.replace(prefixRegex, `id_${indexPrefix}`);
            if (el.htmlFor) el.htmlFor = el.htmlFor.replace(prefixRegex, `id_${indexPrefix}`);
        });

        // 🔥 REMOVE o campo DELETE completamente
        newRow.querySelectorAll('input[name$="-DELETE"]').forEach(el => el.remove());

        // Limpa valores de input e select
        newRow.querySelectorAll('input, select').forEach((el) => {
            if (el.type === 'hidden' && el.name.endsWith('-id')) {
                el.value = '';
            } else if (el.tagName === 'INPUT' && el.type !== 'hidden') {
                el.value = '';
            } else if (el.tagName === 'SELECT') {
                el.selectedIndex = 0;
            }
        });

        container.appendChild(newRow);
        attachEventsToNewForm(newRow); 
        totalFormsInput.value = formCount + 1;
        updateTotal();
    });

    function attachEventsToNewForm(row) {
        const removeButton = row.querySelector(".btn-remove-item");
        if (removeButton) {
            removeButton.onclick = function () {
                // 🔥 Remove diretamente sem confirmação
                row.remove();
                reindexForms();
                updateTotal();
            };
        }

        row.querySelectorAll("input, select").forEach((input) => 
            input.addEventListener("input", updateTotal)
        );
    }

    function reindexForms() {
        const rows = container.querySelectorAll(".item-form-row");
        let validIndex = 0;
        
        rows.forEach((row) => {
            if (row.parentElement.id === 'emptyFormTemplate') return;

            const currentPrefixRegex = /itemalugado_set-\d+-/g;
            const newPrefix = `itemalugado_set-${validIndex}-`;

            row.querySelectorAll("input, select, label").forEach((el) => {
                if (el.name) el.name = el.name.replace(currentPrefixRegex, newPrefix);
                if (el.id) el.id = el.id.replace(/id_itemalugado_set-\d+-/g, `id_${newPrefix}`);
                if (el.htmlFor) el.htmlFor = el.htmlFor.replace(/id_itemalugado_set-\d+-/g, `id_${newPrefix}`);
            });

            row.querySelector(".btn-remove-item")?.setAttribute('data-index', validIndex);
            validIndex++;
        });
        
        totalFormsInput.value = validIndex;
    }

    function updateTotal() {
        let total = 0;
        
        const start = dataEntrega ? new Date(dataEntrega.value) : null;
        const end = dataDevolucao ? new Date(dataDevolucao.value) : null;
        
        let days = 1;
        if (start && end && start.getTime() < end.getTime()) {
            const timeDiff = end.getTime() - start.getTime();
            days = Math.max(1, Math.ceil(timeDiff / (1000 * 60 * 60 * 24)));
        }

        container.querySelectorAll(".item-form-row").forEach((row) => {
            if (row.parentElement.id === 'emptyFormTemplate') return; 

            const qtdInput = row.querySelector(`[name$='-quantidade']`);
            if (qtdInput) {
                const qtd = parseFloat(qtdInput.value) || 0;
                total += qtd * days;
            }
        });

        totalPreview.innerHTML = `<strong>Total estimado (${days} dias):</strong> R$ ${total.toFixed(2).replace('.', ',')}`;
    }

    dataEntrega?.addEventListener("change", updateTotal);
    dataDevolucao?.addEventListener("change", updateTotal);
    
    container.querySelectorAll(".item-form-row").forEach(row => {
        if (row.parentElement.id !== 'emptyFormTemplate') {
            attachEventsToNewForm(row);
        }
    });
    
    updateTotal();
    
    form.addEventListener("submit", () => {
        const submitBtn = form.querySelector(".btn-submit");
        if (submitBtn) {
            submitBtn.classList.add("loading");
            submitBtn.disabled = true;
        }
    });
});
