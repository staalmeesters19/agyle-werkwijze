"""
Meeting Transcriptie Tool
Transcribeert audio (m4a, mp3, wav, mp4) met speaker diarization via AssemblyAI.
Output: transcript met sprekeridentificatie als .md bestand.
"""

import assemblyai as aai
import sys
import os
import json
from pathlib import Path
from datetime import datetime


def transcribe(audio_path: str, language: str = "nl") -> dict:
    """
    Transcribeert een audiobestand met sprekeridentificatie.

    Args:
        audio_path: Pad naar het audiobestand (m4a, mp3, wav, mp4)
        language: Taalcode - 'nl' voor Nederlands, 'en' voor Engels

    Returns:
        dict met transcript, sprekers, en metadata
    """
    # API key uit environment variable
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        # Fallback: probeer .env bestand
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("ASSEMBLYAI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if not api_key:
        print("FOUT: Geen AssemblyAI API key gevonden.")
        print("Stel in via: export ASSEMBLYAI_API_KEY='jouw-key'")
        sys.exit(1)

    aai.settings.api_key = api_key

    # Controleer of bestand bestaat
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"FOUT: Bestand niet gevonden: {audio_path}")
        sys.exit(1)

    print(f"Transcriberen: {audio_file.name}")
    print(f"Taal: {'Nederlands' if language == 'nl' else 'Engels'}")
    print(f"Bestandsgrootte: {audio_file.stat().st_size / (1024*1024):.1f} MB")
    print("Dit kan enkele minuten duren...\n")

    # Configuratie met speaker diarization
    config = aai.TranscriptionConfig(
        language_code=language,
        speaker_labels=True,
        speakers_expected=None,  # auto-detect aantal sprekers
    )
    # Override speech_models met juiste API-waarde (SDK enum is verouderd)
    # Voor niet-Engels: beide modellen nodig voor volledige taalondersteuning
    config._raw_transcription_config.speech_models = ["universal-3-pro", "universal-2"]

    # Transcribeer
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(str(audio_file), config=config)

    if transcript.status == aai.TranscriptStatus.error:
        print(f"FOUT bij transcriptie: {transcript.error}")
        sys.exit(1)

    # Verwerk resultaten
    speakers = set()
    utterances = []

    for utterance in transcript.utterances:
        speaker = f"Spreker {utterance.speaker}"
        speakers.add(speaker)

        # Tijdstempel formatteren (ms naar mm:ss)
        start_sec = utterance.start / 1000
        minutes = int(start_sec // 60)
        seconds = int(start_sec % 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        utterances.append({
            "speaker": speaker,
            "text": utterance.text,
            "timestamp": timestamp,
            "start_ms": utterance.start,
            "end_ms": utterance.end,
        })

    # Duur berekenen
    duration_sec = transcript.utterances[-1].end / 1000 if transcript.utterances else 0
    duration_min = int(duration_sec // 60)
    duration_remaining_sec = int(duration_sec % 60)

    result = {
        "bestandsnaam": audio_file.name,
        "taal": "Nederlands" if language == "nl" else "Engels",
        "duur": f"{duration_min} min {duration_remaining_sec} sec",
        "aantal_sprekers": len(speakers),
        "sprekers": sorted(list(speakers)),
        "utterances": utterances,
        "volledige_tekst": transcript.text,
        "datum_verwerkt": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    return result


def save_transcript_md(result: dict, output_path: str) -> str:
    """Slaat het transcript op als markdown bestand."""

    lines = []
    lines.append(f"# Meeting Transcript: {result['bestandsnaam']}\n")
    lines.append(f"| | |")
    lines.append(f"|---|---|")
    lines.append(f"| **Bestand** | {result['bestandsnaam']} |")
    lines.append(f"| **Taal** | {result['taal']} |")
    lines.append(f"| **Duur** | {result['duur']} |")
    lines.append(f"| **Aantal sprekers** | {result['aantal_sprekers']} |")
    lines.append(f"| **Sprekers** | {', '.join(result['sprekers'])} |")
    lines.append(f"| **Verwerkt op** | {result['datum_verwerkt']} |")
    lines.append(f"\n---\n")

    lines.append(f"## Transcript\n")

    current_speaker = None
    for u in result["utterances"]:
        if u["speaker"] != current_speaker:
            current_speaker = u["speaker"]
            lines.append(f"\n**{current_speaker}** [{u['timestamp']}]:\n")
        lines.append(f"{u['text']}\n")

    lines.append(f"\n---\n")
    lines.append(f"## Volledige tekst (doorlopend)\n")
    lines.append(result["volledige_tekst"])

    output = Path(output_path)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nTranscript opgeslagen: {output_path}")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Gebruik: python transcribe.py <audio_bestand> [taal] [output_pad]")
        print("  taal: 'nl' (default) of 'en'")
        print("  output_pad: optioneel, default is zelfde map als audio")
        sys.exit(1)

    audio_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "nl"

    # Output pad bepalen
    audio_file = Path(audio_path)
    if len(sys.argv) > 3:
        output_path = sys.argv[3]
    else:
        output_path = str(audio_file.with_suffix(".transcript.md"))

    # Transcribeer
    result = transcribe(audio_path, language)

    # Sla transcript op
    save_transcript_md(result, output_path)

    # Sla ook JSON op voor verdere verwerking
    json_path = str(Path(output_path).with_suffix(".json"))
    Path(json_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON data opgeslagen: {json_path}")

    # Print samenvatting
    print(f"\n--- Klaar ---")
    print(f"Duur: {result['duur']}")
    print(f"Sprekers: {result['aantal_sprekers']} gedetecteerd")
    print(f"Transcript: {output_path}")


if __name__ == "__main__":
    main()
