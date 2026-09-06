document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById("loginForm");

        const message =
            document.getElementById("loginMessage");

        if (!form) {
            return;
        }

        form.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const email =
                    document.getElementById(
                        "email"
                    ).value;

                const senha =
                    document.getElementById(
                        "senha"
                    ).value;

                message.textContent =
                    "Entrando...";

                message.className =
                    "message";

                try {

                    const data =
                        await apiRequest(
                            "/auth/login",
                            {
                                method: "POST",

                                body: JSON.stringify({
                                    email: email,
                                    senha: senha
                                })
                            },
                            false
                        );

                    salvarToken(
                        data.access_token
                    );

                    message.textContent =
                        "Login realizado com sucesso!";

                    message.className =
                        "message success";

                    setTimeout(
                        () => {
                            window.location.href =
                                "dashboard.html";
                        },
                        500
                    );

                } catch (error) {

                    message.textContent =
                        error.message;

                    message.className =
                        "message error";
                }
            }
        );
    }
);