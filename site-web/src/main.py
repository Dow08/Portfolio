"""
CyberDailyWatch - Orchestrateur Principal
Pipeline: Scraping → Traduction IA → Script Radio → Audio → JSON
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

from scraper import scrape_hackernews
from audio_gen import generate_audio_sync

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
PUBLIC_DIR = PROJECT_ROOT / "cyber-news"
AUDIO_DIR = PUBLIC_DIR / "audio"
DATA_FILE = PUBLIC_DIR / "data.json"
NUM_ARTICLES = 3

# Modèles IA
OPENAI_MODEL = "gpt-4o-mini"
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-pro",
]

AI_PROVIDER = None


def call_ai(system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
    """Appelle OpenAI ou Gemini avec fallback automatique multi-modèles."""
    global AI_PROVIDER

    # Tentative OpenAI
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            AI_PROVIDER = "openai"
            return response.choices[0].message.content.strip()
        except Exception as e:
            if any(x in str(e).lower() for x in ["quota", "rate", "insufficient"]):
                print("   ⚠️ OpenAI quota dépassé, basculement vers Gemini...")
            else:
                print(f"   ⚠️ Erreur OpenAI: {e}, basculement vers Gemini...")

    # Fallback Gemini multi-modèles
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if gemini_key:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=gemini_key)
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        for model in GEMINI_MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )
                AI_PROVIDER = "gemini"
                print(f"   ✓ Gemini: modèle {model} utilisé")
                return response.text.strip()
            except Exception as e:
                err = str(e).lower()
                if any(x in err for x in ["quota", "exhausted", "429"]):
                    print(f"   ⚠️ {model}: quota épuisé, essai suivant...")
                elif any(x in err for x in ["not found", "404"]):
                    print(f"   ⚠️ {model}: non disponible, essai suivant...")
                else:
                    raise RuntimeError(f"❌ Erreur Gemini ({model}): {e}")

        raise RuntimeError("❌ Tous les modèles Gemini ont échoué (quota épuisé)")

    raise ValueError("❌ Aucune clé API trouvée (OPENAI_API_KEY ou GEMINI_API_KEY)")


def translate_articles(news: list[dict]) -> list[dict]:
    """Traduit les articles en français via IA."""
    articles_text = "\n\n".join([
        f"[ARTICLE {i+1}]\nTITLE: {a['title']}\nSUMMARY: {a['summary']}"
        for i, a in enumerate(news)
    ])

    prompt = f"""Traduis ces {len(news)} articles en français.

{articles_text}

Réponds EXACTEMENT avec ce format pour CHAQUE article:
[ARTICLE 1]
TITRE: <titre traduit>
RESUME: <résumé traduit en 2-3 phrases>

[ARTICLE 2]
TITRE: <titre traduit>
RESUME: <résumé traduit en 2-3 phrases>

[ARTICLE 3]
TITRE: <titre traduit>
RESUME: <résumé traduit en 2-3 phrases>

IMPORTANT: Traduis TOUS les articles sans t'arrêter."""

    translated = call_ai("Tu es un traducteur anglais-français.", prompt, 0.3, 2000)

    result = []
    for i, article in enumerate(news):
        a = article.copy()
        try:
            section = translated.split(f"[ARTICLE {i+1}]")[1]
            if i + 2 <= len(news):
                section = section.split(f"[ARTICLE {i+2}]")[0]

            if "TITRE:" in section:
                a["title_fr"] = section.split("TITRE:")[1].split("\n")[0].strip()
            if "RESUME:" in section:
                a["summary_fr"] = section.split("RESUME:")[1].split("[ARTICLE")[0].strip()
            elif "RÉSUMÉ:" in section:
                a["summary_fr"] = section.split("RÉSUMÉ:")[1].split("[ARTICLE")[0].strip()
        except (IndexError, KeyError):
            a["title_fr"] = article["title"]
            a["summary_fr"] = article["summary"]
        result.append(a)

    return result


def generate_script(news: list[dict]) -> str:
    """Génère un script radio Flash Info Cyber."""
    content = "\n\n".join([
        f"**{i+1}. {a.get('title_fr', a['title'])}**\n{a.get('summary_fr', a['summary'])}"
        for i, a in enumerate(news)
    ])

    prompt = f"""Écris un script radio "Flash Info Cyber" de 200 à 250 mots en français.

ACTUALITÉS DU JOUR :
{content}

CONSIGNES STRICTES :
1. Commence par une accroche engageante ("Bonjour et bienvenue dans votre Flash Info Cyber du jour...")
2. Résume chaque actualité en 2-3 phrases concrètes, en te basant sur les résumés fournis
3. Termine par une conclusion ("Restez vigilants, et à demain pour un nouveau flash...")
4. Le texte doit être FLUIDE et naturel à l'oral, comme un vrai présentateur radio
5. NE PAS utiliser de markdown, de gras, de listes à puces, de numérotation ni de crochets
6. NE PAS écrire les titres bruts des articles, reformule-les naturellement
7. Le script doit être du TEXTE BRUT uniquement, prêt à être lu par un synthétiseur vocal

Écris le script COMPLET maintenant, en texte brut."""

    return call_ai("Tu es un journaliste radio français dynamique et professionnel.", prompt, 0.7, 1200)


def save_data(news: list[dict], script: str) -> None:
    """Sauvegarde les données en JSON pour le frontend."""
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "articles": news,
        "script": script,
        "audio_file": "audio/latest_briefing.mp3",
        "ai_provider": AI_PROVIDER
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Données sauvegardées: {DATA_FILE}")


def main():
    """Pipeline principal."""
    print("=" * 60)
    print("🛡️  CyberDailyWatch - Générateur de Flash Info")
    print("=" * 60)

    # Vérification API
    if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("❌ Aucune clé API trouvée!")
        print("💡 Ajoutez OPENAI_API_KEY ou GEMINI_API_KEY")
        sys.exit(1)

    # Étape 1: Scraping
    print("\n📰 Étape 1: Récupération des actualités...")
    news = scrape_hackernews(NUM_ARTICLES)
    if not news:
        print("❌ Aucune actualité trouvée. Arrêt.")
        return
    print(f"   ✓ {len(news)} articles récupérés")

    # Étape 2: Traduction
    print("\n🌍 Étape 2: Traduction en français...")
    news = translate_articles(news)
    print(f"   ✓ Articles traduits (via {AI_PROVIDER})")

    # Étape 3: Script
    print("\n🤖 Étape 3: Génération du script radio...")
    script = generate_script(news)
    print(f"   ✓ Script généré ({len(script.split())} mots)")

    # Étape 4: Audio
    print("\n🎙️ Étape 4: Génération de l'audio...")
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio_path = generate_audio_sync(script, AUDIO_DIR / "latest_briefing.mp3")
    print(f"   ✓ Audio sauvegardé: {audio_path}")

    # Étape 5: Sauvegarde
    print("\n💾 Étape 5: Sauvegarde des métadonnées...")
    save_data(news, script)

    print("\n" + "=" * 60)
    print(f"✅ Flash info généré avec succès! (Provider: {AI_PROVIDER})")
    print("=" * 60)


if __name__ == "__main__":
    main()
