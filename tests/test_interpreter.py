from pdf_editor.interpreter import interpret_instruction


def test_replace_instruction():
    cmd = interpret_instruction('replace all "AI" with "Artificial Intelligence"')
    assert cmd.action == "replace"
    assert cmd.find == "AI"
    assert cmd.replace == "Artificial Intelligence"


def test_rewrite_instruction_with_style():
    cmd = interpret_instruction("rewrite paragraph 2 in professional tone")
    assert cmd.action == "rewrite"
    assert cmd.target == "paragraph_2"
    assert cmd.style == "professional"
