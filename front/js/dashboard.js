document.addEventListener(
    "DOMContentLoaded",
    async () => {

        if (!estaLogado()) {
            window.location.href =
                "login.html";

            return;
        }

        try {

            const data =
                await apiRequest(
                    "/dashboard/resumo"
                );

            document.getElementById(
                "vendasHoje"
            ).textContent =
                formatarMoeda(
                    data.vendas.hoje
                );

            document.getElementById(
                "vendasMes"
            ).textContent =
                formatarMoeda(
                    data.vendas.mes
                );

            document.getElementById(
                "totalPedidos"
            ).textContent =
                data.pedidos.total;

            document.getElementById(
                "pedidosPendentes"
            ).textContent =
                data.pedidos.pendentes;

            document.getElementById(
                "clientesTotal"
            ).textContent =
                data.clientes.total;

            document.getElementById(
                "produtosTotal"
            ).textContent =
                data.produtos.total;

            document.getElementById(
                "estoqueBaixo"
            ).textContent =
                data.produtos.estoque_baixo;

            document.getElementById(
                "pedidosConcluidos"
            ).textContent =
                data.pedidos.concluidos;

        } catch (error) {

            console.error(error);

            const message =
                document.getElementById(
                    "dashboardMessage"
                );

            if (message) {
                message.textContent =
                    error.message;

                message.className =
                    "message error";
            }
        }
    }
);


function formatarMoeda(valor) {

    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
}


