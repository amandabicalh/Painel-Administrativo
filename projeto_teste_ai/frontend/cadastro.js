async function handleCadastro(event) {
    event.preventDefault();

    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirmPassword').value.trim();
    const mensagem = document.getElementById('mensagem');

    if (!nome || !email || !password || !confirmPassword) {
        mensagem.textContent = 'Por favor, preencha todos os campos.';
        mensagem.style.color = 'red';
        return;
    }

    if (password !== confirmPassword) {
        mensagem.textContent = 'As senhas não coincidem!';
        mensagem.style.color = 'red';
        return;
    }

    if (password.length < 6) {
        mensagem.textContent = 'A senha deve ter pelo menos 6 caracteres.';
        mensagem.style.color = 'red';
        return;
    }

    try {

        const resposta = await fetch("http://127.0.0.1:5000/cadastro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                senha: password
            })
        });

        const dados = await resposta.json();

        mensagem.textContent = dados.mensagem;
        mensagem.style.color = 'green';

        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);

    } catch (erro) {
        mensagem.textContent = "Erro ao conectar com o servidor.";
        mensagem.style.color = "red";
    }
}

document.getElementById('cadastroForm').addEventListener('submit', handleCadastro);