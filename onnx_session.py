import onnxruntime as ort
import numpy as np

class ONNXSession:
    def __init__(self, model_path):
        try:
            self.session = ort.InferenceSession(model_path)
            self.input_names = [i.name for i in self.session.get_inputs()]
            self.output_names = [o.name for o in self.session.get_outputs()]
        except Exception as e:
            print(f"ONNX Runtime not available, using dummy: {e}")
            self.session = None

    def run_inference(self, tokens, embedding, rate=1.0, pitch=0.0, volume=1.0, emotion='neutral', jitter=0.0, shimmer=0.0):
        if self.session is None:
            # Dummy
            audio = np.random.randn(44100).astype(np.float32) * 0.1
            # Apply jitter/shimmer
            for i in range(len(audio)):
                audio[i] += jitter * (np.random.rand() - 0.5)
                if i > 0:
                    audio[i] += shimmer * (audio[i] - audio[i-1])
            return audio.tolist()

        # Prepare inputs
        inputs = {
            'tokens': np.array([tokens], dtype=np.int64),
            'speaker_embedding': np.array([embedding], dtype=np.float32),
            'rate': np.array([rate], dtype=np.float32),
            'pitch': np.array([pitch], dtype=np.float32),
            'volume': np.array([volume], dtype=np.float32),
            'emotion': np.array([0 if emotion == 'neutral' else 1 if emotion == 'happy' else 2 if emotion == 'sad' else 3], dtype=np.int64)
        }

        outputs = self.session.run(self.output_names, inputs)
        audio = outputs[0][0].tolist()
        return audio

    def run_streaming_inference(self, tokens, embedding, callback):
        chunk_size = 10
        buffer = []
        buffer_size = 1024
        for i in range(0, len(tokens), chunk_size):
            chunk = tokens[i:i+chunk_size]
            pcm = self.run_inference(chunk, embedding)
            buffer.extend(pcm)
            while len(buffer) >= buffer_size:
                chunk_pcm = buffer[:buffer_size]
                callback(chunk_pcm)
                buffer = buffer[buffer_size:]
        if buffer:
            callback(buffer)

    def run_extractor_inference(self, pcm):
        if self.session is None:
            # Dummy embedding
            return np.random.randn(256).tolist()
        # Assume extractor inputs
        inputs = {'audio': np.array([pcm], dtype=np.float32)}
        outputs = self.session.run(self.output_names, inputs)
        return outputs[0][0].tolist()

    @staticmethod
    def validate_model_checksum(model_path):
        # Placeholder
        return True