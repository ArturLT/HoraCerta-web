let chartFaturamento = null; // gráfico de linha
let chartReceitasTop = null;  // gráfico pizza top 4 receitas
let chartDespesasTop = null;  // gráfico pizza top 4 despesas

function gerar_cor(qtd = 1) {
    var bg_color = [];
    var border_color = [];
    for (let i = 0; i < qtd; i++) {
        let r = Math.floor(Math.random() * 255);
        let g = Math.floor(Math.random() * 255);
        let b = Math.floor(Math.random() * 255);
        bg_color.push(`rgba(${r}, ${g}, ${b}, 0.2)`);
        border_color.push(`rgba(${r}, ${g}, ${b}, 1)`);
    }
    return { bg_color, border_color };
}

// Gráfico de linha Receitas x Despesas
function renderiza_despesas_mensal(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('faturamento').getContext('2d');

            if (chartFaturamento) chartFaturamento.destroy();

            const cores = gerar_cor(data.labels.length);

            chartFaturamento = new Chart(ctx, {
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
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Receitas vs Despesas - Últimos 12 Meses'
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Erro ao carregar gráfico de linha:", err));
}

// ===============================
//  Função: Top 4 Receitas
// ===============================
function renderiza_top4_receitas(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("receitasTop").getContext("2d");
            if (!ctx) return console.error("Canvas receitasTop não encontrado.");

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [
                            "#36A2EB",
                            "#4BC0C0",
                            "#9966FF",
                            "#FF9F40"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Top 4 Receitas"
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Erro ao carregar gráfico de pizza de receitas:", err));
}


// ===============================
//  Função: Top 4 Despesas
// ===============================
function renderiza_top4_despesas(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("despesasTop").getContext("2d");
            if (!ctx) return console.error("Canvas despesasTop não encontrado.");

            new Chart(ctx, {
                type: "pie",
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [
                            "#FF6384",
                            "#FF9F40",
                            "#FFCD56",
                            "#C9CBCF"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: "Top 4 Despesas"
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Erro ao carregar gráfico de pizza de despesas:", err));
}


// Executar quando a página carrega
document.addEventListener("DOMContentLoaded", function () {
    renderiza_despesas_mensal(urls.relatorio);
    renderiza_top_receitas(urls.top4_receitas);
    renderiza_top_despesas(urls.top4_despesas);
});
