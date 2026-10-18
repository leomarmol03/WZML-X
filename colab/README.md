# WZML-X en Google Colab

El notebook [`WZML-X-Colab.ipynb`](WZML-X-Colab.ipynb) automatiza la instalación de dependencias de Linux y Python, prepara una configuración privada en el runtime, inicia el bot sin ejecutar el actualizador de contenedor y abre la UI web mediante un túnel de Cloudflare.

## Inicio rápido

1. Abre el notebook en Google Colab y habilita **Internet access** en el runtime.
2. Ejecuta las celdas en orden. El notebook descarga la rama `wzv3` de `leomarmol03/WZML-X`; puedes cambiar `REPO_URL` y `BRANCH` en la primera celda si despliegas otra copia.
3. Introduce `BOT_TOKEN`, `OWNER_ID`, `TELEGRAM_API` y `TELEGRAM_HASH` cuando se soliciten. También puedes guardarlos en **Secrets** de Colab con esos nombres. `DATABASE_URL` es opcional, pero se recomienda MongoDB Atlas para conservar configuraciones entre runtimes.
4. Mantén el runtime activo mientras uses el bot. La celda del túnel imprime el enlace público de la UI; el propio bot recibe ese enlace para habilitar el selector de archivos.

Si usas MongoDB Atlas, recuerda que la IP de salida de Colab puede cambiar entre sesiones y debe estar permitida por la lista de acceso de Atlas. Evita abrir el acceso a cualquier IP salvo que comprendas el riesgo y tengas credenciales de base de datos robustas.

## Límites importantes de Colab

- Colab no es un servidor 24/7: el runtime puede desconectarse o reiniciarse, y los archivos locales desaparecen al terminar la sesión.
- Usa el notebook para pruebas o sesiones temporales, no para alojar un bot de producción.
- La descarga de archivos queda en el almacenamiento local temporal de Colab. El bot limpia su carpeta de descargas al iniciar; no apuntes `WZML_DOWNLOAD_DIR` a una carpeta persistente si no quieres que se borre en cada arranque.
- El notebook ejecuta `python -m bot` directamente. **No uses `start.sh` en Colab**: ese entrypoint ejecuta el actualizador de despliegue, pensado para contenedores y que puede limpiar archivos del repositorio.
- JDownloader y SABnzbd se dejan desactivados para ahorrar memoria y evitar servicios extra. Aria2 y qBittorrent sí se instalan para el flujo de torrents, con un límite inicial de dos tareas simultáneas.
- La integración MEGA depende de un binding nativo compatible del SDK C++ que viene en la imagen Docker, pero no en `requirements.txt`. En Colab se desactiva automáticamente si ese binding falta o no es compatible; las operaciones MEGA mostrarán un error claro en lugar de impedir el arranque. No instales `mega`/`mega.py` desde PyPI como sustituto: son clientes diferentes. No se verificó un método de compilación del binding que funcione con el runtime actual de Colab; además, la binding Python antigua del SDK oficial (por ejemplo, v3.9.7) no expone `MegaUploadOptions`, que requiere este código, así que no se propone una instalación engañosa desde esa fuente.
- No publiques el notebook con credenciales ni pegues secretos en celdas de código. El archivo `config.py` se crea solo dentro del runtime.

Para un bot siempre disponible, usa Docker/VPS como indica el README principal.
