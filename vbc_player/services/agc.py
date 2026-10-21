"""Reconstrução analítica fornecida do callback ZaraRadio 1.6.2 (0x407b60).

Não é código-fonte original nem reprodução bit a bit do x87.
As fronteiras de chamadas/blocos fazem parte do resultado do algoritmo.
"""
import math

DECAY = 0.982
BIAS = 97_700_000_000.0
NUMERATOR = 3_127_000.0
CEILING = 28_300
PEAK_MEMORY_FACTOR = 12_000.0
BLOCK_FRAMES = 1024


class ZaraAGC:
    def __init__(self):
        self.reset()

    def reset(self):
        self.energy_left = 0.0
        self.energy_right = 0.0

    def process(self, interleaved):
        if len(interleaved) % 2:
            raise ValueError("Forneça pares de amostras estéreo.")
        if any(not isinstance(x, int) or not -32768 <= x <= 32767 for x in interleaved):
            raise ValueError("As amostras devem ser inteiros PCM16.")
        result = list(interleaved)
        for start in range(0, len(result), BLOCK_FRAMES * 2):
            stop = min(start + BLOCK_FRAMES * 2, len(result))
            self.energy_left = DECAY * self.energy_left + sum(result[i] ** 2 for i in range(start, stop, 2))
            self.energy_right = DECAY * self.energy_right + sum(result[i] ** 2 for i in range(start + 1, stop, 2))
            gain_left = NUMERATOR / math.sqrt(self.energy_left + BIAS)
            gain_right = NUMERATOR / math.sqrt(self.energy_right + BIAS)
            for i in range(start, stop, 2):
                left, right = result[i], result[i + 1]
                out_left, out_right = left * gain_left, right * gain_right
                if abs(int(out_right)) > CEILING:
                    out_right = CEILING if out_right > 0 else -CEILING
                    self.energy_right = PEAK_MEMORY_FACTOR * right * right - BIAS
                    gain_right = NUMERATOR / math.sqrt(self.energy_right + BIAS)
                if abs(int(out_left)) > CEILING:
                    out_left = CEILING if out_left > 0 else -CEILING
                    self.energy_left = PEAK_MEMORY_FACTOR * left * left - BIAS
                    gain_left = NUMERATOR / math.sqrt(self.energy_left + BIAS)
                result[i], result[i + 1] = int(out_left), int(out_right)
        return result


def rms_dbfs(samples):
    energy = sum(x * x for x in samples)
    return 10 * math.log10(energy / len(samples) / 32768 ** 2) if energy else -math.inf
