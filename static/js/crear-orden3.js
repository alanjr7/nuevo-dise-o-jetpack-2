        window.onload = () => {
            document.body.classList.add("loaded");
        };

        let currentInputId = 'input-phone'; 

        function selectInput(type) {
            // Actualizar ID activo
            if (type === 'phone') {
                currentInputId = 'input-phone';
                document.getElementById('group-phone').classList.add('active-field');
                document.getElementById('group-floor').classList.remove('active-field');
            } else {
                currentInputId = 'input-floor';
                document.getElementById('group-floor').classList.add('active-field');
                document.getElementById('group-phone').classList.remove('active-field');
            }
        }

        function pressKey(key) {
            const input = document.getElementById(currentInputId);
            if (!input) return;

            if (key === 'back') {
                input.value = input.value.slice(0, -1);
            } else {
                // Validación opcional: longitud máxima para piso
                if (currentInputId === 'input-floor' && input.value.length >= 4) return;
                // Validación opcional: longitud máxima para teléfono
                if (currentInputId === 'input-phone' && input.value.length >= 8) return;
                
                input.value += key;
            }
        }