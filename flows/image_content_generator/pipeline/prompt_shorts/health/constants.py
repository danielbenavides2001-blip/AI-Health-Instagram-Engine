# flake8: noqa: E501
AUDIO_PROMPT: str = "{audio_text}"

IDEA_PROMPT_MINDSET: str = """# 🧠 GENERADOR DE IDEAS — CIENCIA Y BIOHACKING OSCURO
**Objetivo:** Generar conceptos únicos y fascinantes sobre neuropsicología, procesos biológicos invisibles y optimización humana.

**Directiva de Variedad:**
- Selecciona un tema de estas categorías: Misterios del cerebro, procesos biológicos invisibles (nervios, sangre, células), psicología del sueño/comportamiento, o biohacking de alto rendimiento.
- El tono debe ser serio, oscuro y científico.

**Estructura de la Idea:**
- **Hook:** Una frase impactante que use el "tú" (Ej: "Tu cerebro está borrando recuerdos ahora mismo").
- **Category:** Neuropsicología, Biología, Psicología o Biohacking.
- **Scientific_Explanation:** El núcleo denso pero digerible.
- **Practical_Benefit:** El truco o reflexión final.
"""

SCRIPT_PROMPT: str = """# 📝 PROMPT MAESTRO — PRODUCTOR SENIOR CIENCIA (DARK STYLE)
**Objetivo:** Crear un video de 50-60 segundos con narrativa densa y estética Medical-Futuristic.

**Estructura del Guion (3 Actos / 10 Escenas):**
1. **El Hook (Escena 1):** Frase de impacto usando "Tú". (0-5s)
2. **El Desarrollo (Escenas 2-8):** Explicación científica densa, tono narrativo oscuro y serio. (5-45s)
3. **La Resolución (Escenas 9-10):** Cierre conclusivo, truco práctico o reflexión profunda. (45-60s)

**Reglas de Edición:**
- Ritmo: Pausado, con autoridad. Silencios dramáticos de 0.3s a 0.5s.
- Densidad: Máximo 16-18 palabras por escena. No omitas términos técnicos; la explicación debe ser completa y profesional.

## 🎨 REGLAS VISUALES (MEDICAL-FUTURISTIC)
El `image_prompt` debe estar en INGLÉS y seguir este estilo:
"Cinematic photorealism, dark, medical-futuristic style. Chiaroscuro lighting, cold blue moonlight contrasted with internal glowing neon orange and amber lights representing neural activity. Details: translucent skin, anatomical bones, visible neural networks, floating light particles. 9:16 aspect ratio. [INSERTA ACCIÓN/SUJETO AQUÍ]"
"""
