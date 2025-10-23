import argparse
from text_normalizer import parse_and_normalize_text
from tokenizer import tokenize
from onnx_session import ONNXSession
from embedding_loader import load_embedding, morph_embeddings
from audio_postprocess import postprocess_audio
from mp3_encoder import encode_mp3
from voice import list_voices, import_voice
from subtitle import generate_timestamps, export_srt, export_vtt, export_chapters
from http_server import start_http_server
from multilingual import get_model_for_locale
from quality_metrics import analyze_audio_quality
import os

def run_cli(args):
    if not args:
        print("Usage: python main.py <command> [options]")
        print("Commands: synth, synth-file, batch, stream, list-voices, import-voice, preview-voice, bench, version, server")
        return

    command = args[0]
    if command == "synth":
        synth_command(args[1:])
    elif command == "synth-file":
        synth_file_command(args[1:])
    elif command == "batch":
        batch_command(args[1:])
    elif command == "stream":
        stream_command(args[1:])
    elif command == "list-voices":
        list_voices_command()
    elif command == "import-voice":
        import_voice_command(args[1:])
    elif command == "preview-voice":
        preview_voice_command(args[1:])
    elif command == "bench":
        bench_command()
    elif command == "version":
        print("Offline TTS v1.0.0")
    elif command == "server":
        port = int(args[1]) if len(args) > 1 else 8080
        start_http_server(port)
    else:
        print(f"Unknown command: {command}")

def synth_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    parser.add_argument('--voice', default='narrator')
    parser.add_argument('--morph-voice')
    parser.add_argument('--blend', type=float, default=0.0)
    parser.add_argument('--out', default='output.mp3')
    parser.add_argument('--bitrate', type=int, default=320)
    parser.add_argument('--title')
    parser.add_argument('--artist')
    parser.add_argument('--album')
    parser.add_argument('--rate', type=float, default=1.0)
    parser.add_argument('--pitch', type=float, default=0.0)
    parser.add_argument('--volume', type=float, default=1.0)
    parser.add_argument('--emotion', default='neutral')
    parser.add_argument('--locale', default='auto')
    parser.add_argument('--dict')
    parser.add_argument('--subtitle')
    parser.add_argument('--chapters')
    parser.add_argument('--jitter', type=float, default=0.0)
    parser.add_argument('--shimmer', type=float, default=0.0)
    parser.add_argument('--normalize-lufs', type=float, default=-16.0)
    parser.add_argument('--dither-bits', type=int, default=16)
    parser.add_argument('--phoneme-subtitles', action='store_true')
    parser.add_argument('--analyze-quality', action='store_true')
    opts = parser.parse_args(args)

    if opts.locale == 'auto':
        from multilingual import detect_language
        opts.locale = detect_language(opts.text)

    try:
        segments = parse_and_normalize_text(opts.text, opts.locale, opts.dict)
        full_pcm = []
        for seg in segments:
            tokens = tokenize(seg.text, opts.locale)
            embedding = load_embedding(opts.voice)
            if opts.morph_voice:
                emb2 = load_embedding(opts.morph_voice)
                embedding = morph_embeddings(embedding, emb2, opts.blend)
            lang_model = get_model_for_locale(opts.locale)
            model_path = lang_model.model_path
            session = ONNXSession(model_path)
            seg_rate = opts.rate * seg.rate
            seg_pitch = opts.pitch + seg.pitch
            seg_volume = opts.volume * seg.volume
            pcm = session.run_inference(tokens, embedding, seg_rate, seg_pitch, seg_volume, opts.emotion, opts.jitter, opts.shimmer, seg.emphasis, seg.breath)
            if seg.break_time > 0:
                silence = [0.0] * int(seg.break_time * 44100)
                full_pcm.extend(silence)
            else:
                full_pcm.extend(pcm)

        postprocess_audio(full_pcm, 'neutral', opts.normalize_lufs, opts.dither_bits)

        if opts.analyze_quality:
            report = analyze_audio_quality(full_pcm)
            print("Audio Quality Analysis:")
            print(f"  Peak Level: {report.peak_level}")
            print(f"  RMS Level: {report.rms_level}")
            print(f"  SNR: {report.snr_db} dB")
            print(f"  Clipping: {'Yes' if report.has_clipping else 'No'}")

        encode_mp3(full_pcm, opts.out, opts.bitrate, opts.title, opts.artist, opts.album)

        if opts.subtitle:
            timestamps = generate_timestamps(opts.text, full_pcm, opts.phoneme_subtitles)
            if opts.subtitle.endswith('.srt'):
                export_srt(timestamps, opts.subtitle)
            elif opts.subtitle.endswith('.vtt'):
                export_vtt(timestamps, opts.subtitle)
            print(f"Subtitles exported to {opts.subtitle}")

        if opts.chapters:
            timestamps = generate_timestamps(opts.text, full_pcm, False)
            export_chapters(timestamps, opts.chapters)
            print(f"Chapters exported to {opts.chapters}")

        print(f"Synthesized to {opts.out}")
    except Exception as e:
        print(f"Error: {e}")

# Add other commands similarly, but for brevity, placeholder
def synth_file_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('--voice', default='narrator')
    parser.add_argument('--out', default='output.mp3')
    parser.add_argument('--bitrate', type=int, default=320)
    opts = parser.parse_args(args)
    try:
        with open(opts.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        args_synth = ['synth', '--text', text, '--voice', opts.voice, '--out', opts.out, '--bitrate', str(opts.bitrate)]
        run_cli(args_synth)
        print(f"Synthesized from file to {opts.out}")
    except Exception as e:
        print(f"Error: {e}")

def batch_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('--voice', default='narrator')
    parser.add_argument('--out-dir', default='output')
    parser.add_argument('--bitrate', type=int, default=320)
    opts = parser.parse_args(args)
    import os
    os.makedirs(opts.out_dir, exist_ok=True)
    for file in os.listdir(opts.input_dir):
        if file.endswith('.txt'):
            input_path = os.path.join(opts.input_dir, file)
            output_path = os.path.join(opts.out_dir, file.replace('.txt', '.mp3'))
            args_file = ['synth-file', input_path, '--voice', opts.voice, '--out', output_path, '--bitrate', str(opts.bitrate)]
            run_cli(args_file)
    print(f"Batch synthesis completed in {opts.out_dir}")

def stream_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True)
    parser.add_argument('--voice', default='narrator')
    opts = parser.parse_args(args)
    try:
        segments = parse_and_normalize_text(opts.text)
        tokens = tokenize(segments[0].text)
        embedding = load_embedding(opts.voice)
        model_path = get_model_for_locale('en-US').model_path
        session = ONNXSession(model_path)
        def callback(pcm_chunk):
            # In real implementation, stream to audio device
            print(f"Streaming chunk of {len(pcm_chunk)} samples")
        session.run_streaming_inference(tokens, embedding, callback)
        print("Streaming completed")
    except Exception as e:
        print(f"Error: {e}")

def list_voices_command():
    voices = list_voices()
    print("Available voices:")
    for v in voices:
        print(f"- {v.name} ({v.gender}, {v.locale}): {v.description}")

def import_voice_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('embedding_path')
    parser.add_argument('--name', default='imported_voice')
    opts = parser.parse_args(args)
    if import_voice(opts.embedding_path, opts.name):
        print(f"Imported voice: {opts.name}")
    else:
        print("Failed to import voice")

def preview_voice_command(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('voice')
    opts = parser.parse_args(args)
    sample_text = f"This is a sample of the {opts.voice} voice."
    try:
        segments = parse_and_normalize_text(sample_text)
        tokens = tokenize(segments[0].text)
        embedding = load_embedding(opts.voice)
        model_path = get_model_for_locale('en-US').model_path
        session = ONNXSession(model_path)
        pcm = session.run_inference(tokens, embedding)
        postprocess_audio(pcm)
        encode_mp3(pcm, f'/tmp/preview_{opts.voice}.mp3', 320)
        print(f"Preview saved to /tmp/preview_{opts.voice}.mp3")
    except Exception as e:
        print(f"Error: {e}")

def bench_command():
    print("bench not implemented yet")