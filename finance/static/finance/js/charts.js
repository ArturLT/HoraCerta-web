function gerar_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push('rgba(${r}, ${g}, ${b}, ${0.2})')
        border_color.push('rgba(${r}, ${g}, ${b}, ${0.2})')
    }
    return {bg_color, border_color};
}

function renderiza_despesas_mensal(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('faturamento').getContext('2d');
            const cores = gerar_cor(data.labels.length);

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Receitas',
                            data: data.data1,
                            backgroundColor: cores.bg_color,
                            borderColor: cores.border_color,
                            borderWidth: 1
                        },
                        {
                            label: 'Despesas',
                            data: data.data2,
                            backgroundColor: "#CB1EA8",
                            borderColor: "#CB1EA8",
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Receitas vs Despesas - Últimos 12 Meses'
                        }
                    }
                }
            });
        });
}

document.addEventListener("DOMContentLoaded", function () {
    renderiza_despesas_mensal("/relatorio/");
});