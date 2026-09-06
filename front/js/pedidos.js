document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (!estaLogado()) {
            window.location.href =
                "login.html";

            return;
        }

        carregarPedidos();
    }
);


async function carregarPedidos() {

    const tabela =
        document.getElementById(
            "pedidosTableBody"
        );

    try {

        const pedidos =
            await apiRequest(
                "/pedidos/"
            );

        tabela.innerHTML = "";

        if (pedidos.length === 0) {

            tabela.innerHTML = `
                <tr>
                    <td colspan="6">
                        Nenhum pedido cadastrado.
                    </td>
                </tr>
            `;

            return;
        }

        pedidos.forEach(
            pedido => {

                tabela.innerHTML += `
                    <tr>

                        <td>
                            #${pedido.id}
                        </td>

                        <td>
                            Cliente #${pedido.cliente_id}
                        </td>

                        <td>
                            ${formatarMoeda(
                                pedido.total
                            )}
                        </td>

                        <td>
                            <span class="status">
                                ${pedido.status}
                            </span>
                        </td>

                        <td>
                            ${formatarData(
                                pedido.created_at
                            )}
                        </td>

                        <td>

                            <select
                                onchange="
                                    alterarStatus(
                                        ${pedido.id},
                                        this.value
                                    )
                                "
                            >

                                <option value="">
                                    Alterar
                                </option>

                                <option value="Pendente">
                                    Pendente
                                </option>

                                <option value="Confirmado">
                                    Confirmado
                                </option>

                                <option value="Preparando">
                                    Preparando
                                </option>

                                <option value="Enviado">
                                    Enviado
                                </option>

                                <option value="Concluído">
                                    Concluído
                                </option>

                                <option value="Cancelado">
                                    Cancelado
                                </option>

                            </select>

                        </td>

                    </tr>
                `;
            }
        );

    } catch (error) {

        console.error(error);

        tabela.innerHTML = `
            <tr>
                <td colspan="6">
                    ${error.message}
                </td>
            </tr>
        `;
    }
}


async function alterarStatus(
    pedidoId,
    status
) {

    if (!status) {
        return;
    }

    try {

        await apiRequest(
            `/pedidos/${pedidoId}/status`,
            {
                method: "PUT",

                body: JSON.stringify({
                    status: status
                })
            }
        );

        await carregarPedidos();

    } catch (error) {

        alert(error.message);

        carregarPedidos();
    }
}


function formatarMoeda(valor) {

    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
}


function formatarData(data) {

    return new Date(data)
        .toLocaleString(
            "pt-BR"
        );
}