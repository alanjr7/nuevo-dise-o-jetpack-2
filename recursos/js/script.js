 document.addEventListener('click', function(){
      window.location.href = 'inicio.html';
        });
        document.addEventListener('DOMContentLoaded', function() {
            const video = document.getElementById('bg-video');
            
            
            // Intentar reproducir el video automáticamente
            const playVideo = () => {
                video.play().then(() => {
                    console.log("Video reproduciéndose correctamente");
                }).catch(error => {
                    console.log("Error al reproducir automáticamente:", error);
                    // Mostrar mensaje para el usuario si es necesario
                });
            };
            
            // Reproducir el video cuando la página esté lista
            playVideo();
            
            
            
            // Detectar si el video está cargado y listo
            video.addEventListener('loadeddata', () => {
                console.log("Video cargado correctamente");
            });
            
            // Manejar errores de carga del video
            video.addEventListener('error', () => {
                console.error("Error al cargar el video");
                // Podríamos mostrar una imagen de fondo alternativa aquí
                document.body.style.backgroundImage = "url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80')";
                document.body.style.backgroundSize = "cover";
                document.body.style.backgroundPosition = "center";
            });
        });
        