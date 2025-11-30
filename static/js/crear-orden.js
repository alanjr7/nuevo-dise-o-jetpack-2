document.addEventListener('DOMContentLoaded', () => {
    const recipientInput = document.getElementById('recipient-name');
    const keys = document.querySelectorAll('.key');

    keys.forEach(key => {
        key.addEventListener('click', () => {
            const keyValue = key.textContent.trim();

            if (key.classList.contains('key-backspace')) {
                // Lógica para la tecla de borrar
                recipientInput.value = recipientInput.value.slice(0, -1);
            } else if (key.classList.contains('key-space')) {
                // Lógica para la barra espaciadora
                recipientInput.value += ' ';
            } else {
                // Lógica para letras y números
                recipientInput.value += keyValue;
            }
        });
    });

    // Opcional: Evitar que el input físico del teclado interfiera si es un quiosco táctil
    recipientInput.addEventListener('focus', (e) => {
        e.target.blur();
    });
});
