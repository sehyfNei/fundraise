from __future__ import annotations

import base64
import html
import json


def encode_pdf_base64(pdf_bytes: bytes) -> str:
    return base64.b64encode(pdf_bytes).decode("utf-8")


def build_pdf_overlay_html(pdf_b64: str, reader_view_model: dict, selected_block_id: str | None = None) -> str:
    """
    Render PDF and visual overlay boxes similar to design-tool editors.

    Note: this is a Streamlit-embedded viewer shell. Selection is still driven
    by native Streamlit controls, but the PDF view itself appears as a canvas
    with component boxes.
    """
    safe_selected = html.escape(selected_block_id or "")
    vm_json = json.dumps(reader_view_model)

    return f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  body {{ margin: 0; font-family: Inter, system-ui, sans-serif; background: #f3f4f6; }}
  .shell {{ max-width: 980px; margin: 0 auto; padding: 12px; }}
  .stage {{ position: relative; width: 100%; height: 860px; border-radius: 14px; overflow: hidden; border: 1px solid #d1d5db; background: white; }}
  iframe {{ width: 100%; height: 100%; border: 0; }}
  .overlay {{ position: absolute; inset: 0; pointer-events: none; }}
  .box {{ position: absolute; border: 2px solid rgba(37,99,235,0.55); background: rgba(37,99,235,0.08); border-radius: 6px; }}
  .box.selected {{ border-color: #ef4444; background: rgba(239,68,68,0.15); }}
  .tag {{ position: absolute; top: -18px; left: 0; font-size: 10px; background: #111827; color: #fff; padding: 2px 6px; border-radius: 999px; white-space: nowrap; }}
  .legend {{ font-size: 12px; color: #4b5563; margin: 8px 2px 0; }}
</style>
</head>
<body>
  <div class="shell">
    <div class="stage">
      <iframe src="data:application/pdf;base64,{pdf_b64}"></iframe>
      <div class="overlay" id="overlay"></div>
    </div>
    <div class="legend">Blue = editable components, Red = selected component</div>
  </div>
<script>
  const viewModel = {vm_json};
  const selectedId = {json.dumps(safe_selected)};
  const overlay = document.getElementById('overlay');

  const firstPage = (viewModel.pages || [])[0];
  if (firstPage) {{
    const blocks = (viewModel.blocks || []).filter(b => b.page === firstPage.number && b.normalized_bbox);
    blocks.forEach((b) => {{
      const box = document.createElement('div');
      box.className = 'box' + (b.id === selectedId ? ' selected' : '');
      box.style.left = (b.normalized_bbox.left * 100) + '%';
      box.style.top = (b.normalized_bbox.top * 100) + '%';
      box.style.width = (b.normalized_bbox.width * 100) + '%';
      box.style.height = (b.normalized_bbox.height * 100) + '%';

      const tag = document.createElement('div');
      tag.className = 'tag';
      tag.textContent = b.id;
      box.appendChild(tag);

      overlay.appendChild(box);
    }});
  }}
</script>
</body>
</html>
"""
