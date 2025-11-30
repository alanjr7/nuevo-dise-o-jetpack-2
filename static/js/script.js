document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('bg-video');
    
    // --- LÓGICA DEL VIDEO ---
    
    // Intentar reproducir el video automáticamente
    const playVideo = () => {
        if (video) {
            video.play().then(() => {
                console.log("Video reproduciéndose correctamente");
            }).catch(error => {
                console.log("Error al reproducir automáticamente:", error);
                // Aquí podrías mostrar un botón de "Play" manual si el navegador bloquea el autoplay
            });
        }
    };
    
    // Reproducir el video cuando la página esté lista
    playVideo();
    
    if (video) {
        // Detectar si el video está cargado y listo
        video.addEventListener('loadeddata', () => {
            console.log("Video cargado correctamente");
        });
        
        // Manejar errores de carga del video
        video.addEventListener('error', () => {
            console.error("Error al cargar el video");
            // Fallback: Imagen de fondo si el video falla
            document.body.style.backgroundImage = "url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1170&q=80')";
            document.body.style.backgroundSize = "cover";
            document.body.style.backgroundPosition = "center";
            
            // Ocultar el contenedor del video para ver la imagen de fondo
            const videoContainer = document.querySelector('.video-container');
            if (videoContainer) videoContainer.style.display = 'none';
        });
    }

    // --- NOTA IMPORTANTE ---
    // Hemos eliminado el "document.addEventListener('click'...)" de aquí.
    // La redirección ahora la maneja el <body> de index.html con:
    // onclick="window.location.href='{{ url_for('inicio') }}'"
    // Esto es mucho más seguro y compatible con Flask.
});