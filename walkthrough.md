# 🚀 Walkthrough: EnigmaIQ Health Engine Implementation

Este documento detalla la creación y configuración del "Proyecto Gemelo" para la automatización de salud en Instagram.

## 1. Concepto y Estrategia
Se ha creado un motor independiente llamado `AI-Health-Instagram-Engine` diseñado específicamente para el nicho de biohacking y ciencia de la salud.

- **Nicho:** Retos de Ejercicio Físico de 30 días (Biohacking, Fisiología).
- **Formato:** Instagram Reels (9:16) a 30 FPS constantes.
- **Estilo Visual:** **Realismo Anatómico (Estilo EnigmaIQ)** - Entornos realistas (habitaciones/gimnasios) con modelos humanos detallados mostrando musculatura y órganos.

## 2. Nueva Identidad Visual 🧪
Hemos evolucionado de fondos oscuros de neón a un estilo mucho más realista, profesional y viral, simulando visualizaciones médicas en 3D de alta gama dentro de entornos cotidianos.

## 3. Configuración de GitHub Actions (Horarios Pico)
El bot está configurado para ejecutarse automáticamente **dos veces al día** en las horas de mayor interacción (9:00 AM y 7:00 PM hora local). Para que funcione, debes ir a tu repositorio en GitHub y configurar los siguientes **Secrets**:

| Secret Name | Descripción |
| :--- | :--- |
| `IG_USER_ID` | ID de tu perfil profesional de Instagram. |
| `FACEBOOK_PAGE_ACCESS_TOKEN` | Token de Meta con permisos de publicación. |
| `GEMINI_API_KEY` | Tu API Key de Google Gemini. |
| `GCP_PROJECT_ID` | ID de tu proyecto en Google Cloud. |
| `GCS_BUCKET_NAME` | Nombre del bucket para alojar los videos. |
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | El contenido completo del archivo JSON de tu Service Account. |

## 4. Estructura del Código y Subida "A Prueba de Balas"
- `flows/image_content_generator/pipeline/daily_automated_content.py`: El cerebro que orquestra todo.
- `flows/image_content_generator/pipeline/prompt_shorts/health/constants.py`: Donde vive la personalidad del bot (prompts de EnigmaIQ y retos físicos).
- `tools/social_media/instagram.py`: El encargado de la subida oficial. **Utiliza URLs Firmadas de Google Cloud Storage (Signed URLs) para garantizar una entrega 100% estable a los servidores de Meta**, evadiendo los bloqueos del protocolo de subida binaria.

---
> [!TIP]
> El bot ya está en piloto automático. Publicará tus Reels de retos físicos todos los días a las 9:00 AM y a las 7:00 PM.
