# AI-Health-Instagram-Engine (EnigmaIQ Edition) 🧬✨

Este es el motor de automatización de contenido para la cuenta de Instagram @enigmaaiq, especializado en biohacking, fisiología y ciencia de la salud.

## 🚀 Funcionalidades
- **Generador de Ideas:** Basado en ciencia y curiosidad fisiológica ("¿Qué pasa si...").
- **Estilo Visual:** Cyber-Organic Biohacking (Neon Dark Mode).
- **Publicación Automática:** Subida directa de Instagram Reels mediante la Graph API oficial.
- **Automatización Total:** Programado para ejecutarse diariamente vía GitHub Actions.

## 🛠️ Requisitos
- Google Cloud Project (Vertex AI & Cloud Storage).
- Meta Developer App (Instagram Graph API).
- Tokens de acceso configurados en los Secrets del repositorio.

## ⚙️ Configuración de Secrets
Para que el bot funcione en GitHub Actions, debes configurar los siguientes Secrets:
- `IG_USER_ID`: ID de tu cuenta profesional de Instagram.
- `FACEBOOK_PAGE_ACCESS_TOKEN`: Token de acceso de Meta.
- `GCP_PROJECT_ID`: ID de tu proyecto de Google Cloud.
- `GCS_BUCKET_NAME`: Nombre del bucket de Cloud Storage.
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Contenido del archivo JSON de tu Service Account de Google.
- `GEMINI_API_KEY`: Tu clave de API de Google Gemini.

---
Desarrollado con 🧠 por Antigravity.
