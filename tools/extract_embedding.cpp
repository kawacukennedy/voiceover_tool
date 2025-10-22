#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <cmath>
// Assume ONNX Runtime for extractor model
// Assume audio loading library, e.g., libsndfile or similar
// For demo, we'll use a simple WAV loader placeholder

// Simple WAV header struct
struct WAVHeader {
    char riff[4];
    uint32_t file_size;
    char wave[4];
    char fmt[4];
    uint32_t fmt_size;
    uint16_t audio_format;
    uint16_t num_channels;
    uint32_t sample_rate;
    uint32_t byte_rate;
    uint16_t block_align;
    uint16_t bits_per_sample;
    char data[4];
    uint32_t data_size;
};

// Load WAV file (placeholder implementation)
std::vector<float> load_wav(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Cannot open audio file: " + path);
    }

    WAVHeader header;
    file.read(reinterpret_cast<char*>(&header), sizeof(header));

    if (std::string(header.riff, 4) != "RIFF" || std::string(header.wave, 4) != "WAVE") {
        throw std::runtime_error("Invalid WAV file: " + path);
    }

    if (header.bits_per_sample != 16 || header.num_channels != 1) {
        throw std::runtime_error("Unsupported WAV format. Need 16-bit mono.");
    }

    std::vector<int16_t> pcm16(header.data_size / 2);
    file.read(reinterpret_cast<char*>(pcm16.data()), header.data_size);

    std::vector<float> pcm(pcm16.size());
    for (size_t i = 0; i < pcm16.size(); ++i) {
        pcm[i] = pcm16[i] / 32768.0f;
    }

    return pcm;
}

// Preprocess audio: normalize, remove silence, etc.
std::vector<float> preprocess_audio(std::vector<float> pcm) {
    // Normalize
    float max_val = *std::max_element(pcm.begin(), pcm.end(), [](float a, float b){ return std::abs(a) < std::abs(b); });
    if (max_val > 0) {
        for (auto& sample : pcm) sample /= max_val;
    }

    // Remove leading/trailing silence
    const float threshold = 0.01f;
    size_t start = 0;
    while (start < pcm.size() && std::abs(pcm[start]) < threshold) ++start;
    size_t end = pcm.size();
    while (end > start && std::abs(pcm[end - 1]) < threshold) --end;
    pcm = std::vector<float>(pcm.begin() + start, pcm.begin() + end);

    // Truncate to 30 seconds max
    const size_t max_samples = 16000 * 30;
    if (pcm.size() > max_samples) {
        pcm.resize(max_samples);
    }

    return pcm;
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: extract_embedding <audio_file.wav> <output_embedding.bin> [--model <extractor_model.onnx>]\n";
        return 1;
    }
    std::string audio_file = argv[1];
    std::string output = argv[2];
    std::string model_path = "models/extractor.onnx"; // default

    for (int i = 3; i < argc; ++i) {
        if (std::string(argv[i]) == "--model" && i + 1 < argc) {
            model_path = argv[++i];
        }
    }

    try {
        // Load and preprocess audio
        std::vector<float> pcm = load_wav(audio_file);
        pcm = preprocess_audio(pcm);

        if (pcm.size() < 16000 * 5) { // Minimum 5 seconds
            throw std::runtime_error("Audio too short. Need at least 5 seconds.");
        }

        std::cout << "Loaded " << pcm.size() / 16000.0f << " seconds of audio\n";

        // Load ONNX model for extractor
        // Assuming ONNXSession has run_extractor_inference method
        // ONNXSession extractor_session(model_path);
        // std::vector<float> embedding = extractor_session.run_extractor_inference(pcm);

        // Placeholder: dummy embedding
        std::vector<float> embedding(256, 0.0f);
        // Simple average-based embedding (placeholder)
        for (size_t i = 0; i < embedding.size(); ++i) {
            float sum = 0.0f;
            for (size_t j = i; j < pcm.size(); j += embedding.size()) {
                sum += pcm[j];
            }
            embedding[i] = sum / (pcm.size() / embedding.size());
        }

        // Save to file
        std::ofstream file(output, std::ios::binary);
        if (!file) {
            throw std::runtime_error("Failed to open output file: " + output);
        }
        file.write(reinterpret_cast<char*>(embedding.data()), embedding.size() * sizeof(float));
        std::cout << "Embedding extracted to " << output << "\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
}