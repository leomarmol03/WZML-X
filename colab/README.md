# WZML-X en Google Colab

El notebook [`WZML-X-Colab.ipynb`](WZML-X-Colab.ipynb) usa **udocker 1.3.17** para ejecutar sin Docker daemon ni privilegios reales la imagen base `mysterysd/wzmlx:wzadv` que usa el `Dockerfile` del proyecto. Monta el checkout en `/usr/src/app`, instala allí `requirements.txt` en `/wzvenv` y ejecuta el bot con ese Python, sin `start.sh` ni `update.py`. La imagen está pensada para aportar los binarios y el binding nativo de MEGA que faltan en un runtime Python de Colab.

Se eligió udocker/PRoot en modo P2 en lugar de FREEROOT porque permite reutilizar directamente la imagen base del despliegue y su entorno, sin añadir otra capa de runtime. PRoot no proporciona aislamiento fuerte, así que ejecuta solo la imagen de confianza del proyecto; esto no convierte Colab en un host de producción.

## Inicio rápido

1. Abre el notebook en Google Colab y habilita **Internet access** en el runtime.
2. Ejecuta las celdas en orden. La configuración actual clona la rama `arena/d3f87987-wzml-x` de `leomarmol03/WZML-X`; puedes cambiar `REPO_URL` y `BRANCH` en la primera celda si usas un fork o una rama ya integrada.
3. La primera instalación usa `pip` para udocker, descarga sus herramientas PRoot y hace pull de `mysterysd/wzmlx:wzadv` desde Docker Hub. El contenedor y la imagen ocupan varios GB y solo viven en el disco temporal del runtime.
4. Introduce `BOT_TOKEN`, `OWNER_ID`, `TELEGRAM_API` y `TELEGRAM_HASH` cuando se soliciten. También puedes guardarlos en **Secrets** de Colab con esos nombres. `DATABASE_URL` es opcional, pero se recomienda MongoDB Atlas para conservar configuraciones entre runtimes.
5. Mantén el runtime activo mientras uses el bot. La celda del túnel imprime el enlace público de la UI; el bot lee esa URL desde un archivo montado para habilitar el selector de archivos.

La celda de preparación comprueba dentro del contenedor los binarios y `MEGA_SDK_AVAILABLE`. La imagen `wzadv` debería proporcionar el binding compatible que usa el despliegue Docker. Si la importación falla, el adaptador opcional del bot permite iniciar sin MEGA y el log indica el motivo; en ese caso no se deben instalar `mega`/`mega.py` de PyPI como sustituto porque son clientes distintos.

Si Docker Hub limita o falla el pull, vuelve a ejecutar la celda después de un tiempo y revisa el error que imprime udocker. En Colab, la IP de salida cambia entre sesiones; si usas MongoDB Atlas, permite la IP vigente. No abras el acceso a cualquier IP salvo que comprendas el riesgo.

## Límites importantes de Colab

- Colab no es un servidor 24/7: el runtime puede desconectarse o reiniciarse, y el contenedor, las descargas y los archivos locales desaparecen al terminar la sesión.
- Usa el notebook para pruebas o sesiones temporales, no para alojar un bot de producción. udocker no ofrece aislamiento fuerte comparable a Docker con daemon; no ejecutes imágenes no confiables.
- El bot limpia su carpeta de descargas al iniciar; no apuntes `WZML_DOWNLOAD_DIR` a una carpeta persistente si no quieres que se borre en cada arranque.
- **No ejecutes `start.sh` en Colab**: el notebook llama directamente a `/wzvenv/bin/python -m bot` y omite el actualizador de despliegue.
- JDownloader y SABnzbd se dejan desactivados; Aria2 y qBittorrent permanecen activos con un límite inicial de dos tareas simultáneas.
- Cloudflare Quick Tunnel es público y temporal. No compartas su URL si la UI contiene datos que deban permanecer privados.
- No publiques el notebook con credenciales ni pegues secretos en celdas de código. `config.py` se crea solo en el runtime con permisos restringidos.

Para un bot siempre disponible, usa Docker/VPS como indica el README principal.
