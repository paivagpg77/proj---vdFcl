document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (!estaLogado()) {
            window.location.href =
                "login.html";

            return;
        }

        carregarProdutos();
    }
);


async function carregarProdutos() {

    const tabela =
        document.getElementById(
            "produtosTableBody"
        );

    try {

        const produtos =
            await apiRequest(
                "/produtos/"
            );

        tabela.innerHTML = "";

        if (produtos.length === 0) {

            tabela.innerHTML = `
                <tr>
                    <td colspan="7">
                        Nenhum produto cadastrado.
                    </td>
                </tr>
            `;

            return;
        }

        produtos.forEach(
            produto => {

                const estoqueBaixo =
                    produto.estoque <=
                    produto.estoque_minimo;

                tabela.innerHTML += `
                    <tr>

                        <td>
                            ${produto.id}
                        </td>

                        <td>
                            ${produto.nome}
                        </td>

                        <td>
                            ${produto.categoria || "-"}
                        </td>

                        <td>
                            ${formatarMoeda(
                                produto.preco
                            )}
                        </td>

                        <td class="${
                            estoqueBaixo
                                ? "estoque-baixo"
                                : "estoque-normal"
                        }">
                            ${produto.estoque}
                        </td>

                        <td>
                            ${produto.ativo
                                ? "Ativo"
                                : "Inativo"}
                        </td>

                        <td>
                            <button
                                class="btn btn-danger"
                                onclick="excluirProduto(${produto.id})"
                            >
                                Excluir
                            </button>
                        </td>

                    </tr>
                `;
            }
        );

    } catch (error) {

        console.error(error);

        tabela.innerHTML = `
            <tr>
                <td colspan="7">
                    ${error.message}
                </td>
            </tr>
        `;
    }
}


async function criarProduto(event) {

    event.preventDefault();

    const dados = {

        nome:
            document.getElementById(
                "nome"
            ).value,

        descricao:
            document.getElementById(
                "descricao"
            ).value || null,

        preco:
            Number(
                document.getElementById(
                    "preco"
                ).value
            ),

        estoque:
            Number(
                document.getElementById(
                    "estoque"
                ).value
            ),

        estoque_minimo:
            Number(
                document.getElementById(
                    "estoque_minimo"
                ).value
            ),

        categoria:
            document.getElementById(
                "categoria"
            ).value || null
    };

    try {

        await apiRequest(
            "/produtos/",
            {
                method: "POST",
                body: JSON.stringify(dados)
            }
        );

        document.getElementById(
            "produtoForm"
        ).reset();

        carregarProdutos();

    } catch (error) {

        alert(error.message);
    }
}


async function excluirProduto(id) {

    const confirmar =
        confirm(
            "Deseja realmente excluir este produto?"
        );

    if (!confirmar) {
        return;
    }

    try {

        await apiRequest(
            `/produtos/${id}`,
            {
                method: "DELETE"
            }
        );

        carregarProdutos();

    } catch (error) {

        alert(error.message);
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