import json

from pdf_editor import llm


def test_rewrite_text_without_api_key_falls_back(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = llm.rewrite_text_with_llm("hello", "professional")
    assert result == "[professional rewrite] hello"


def test_rewrite_text_with_groq_response(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(
                {
                    "choices": [
                        {
                            "message": {
                                "content": "Polished rewrite output"
                            }
                        }
                    ]
                }
            ).encode("utf-8")

    def fake_urlopen(req, timeout=0):
        assert req.full_url == llm.GROQ_ENDPOINT
        assert timeout == 20
        return FakeResponse()

    monkeypatch.setattr(llm.request, "urlopen", fake_urlopen)
    result = llm.rewrite_text_with_llm("hello", "professional")
    assert result == "Polished rewrite output"
