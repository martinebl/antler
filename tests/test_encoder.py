import pytest
from llmtest.encoder import Encoder

@pytest.mark.parametrize("string, enc_string", [
    ("The quick brown fox jumps over 13 lazy dogs.", "Gur dhvpx oebja sbk whzcf bire 13 ynml qbtf."),
    #("Gur dhvpx oebja sbk whzcf bire 13 ynml qbtf.", "The quick brown fox jumps over 13 lazy dogs."),
])
def test_rot13_encoder(string, enc_string):
    assert Encoder.encodeROT13(string) == enc_string

@pytest.mark.parametrize("enc_string, string", [
    ("Gur dhvpx oebja sbk whzcf bire 13 ynml qbtf.", "The quick brown fox jumps over 13 lazy dogs."),
])
def test_rot13_decoder(enc_string, string):
    assert Encoder.decodeROT13(enc_string) == string