import sys
import json
import requests
from pathlib import Path

def run_sticker_workflow(image_path, style, emoji_type):
    workflow_path = "backend/workflows/sticker_workflow.json"
    
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)
    
    for node in workflow.get("nodes", []):
        if node.get("type") == "LoadImage":
            node["inputs"]["image"] = str(image_path)
    
    text_encode_node = next((n for n in workflow.get("nodes", []) if n.get("type") == "CLIPTextEncode"), None)
    if text_encode_node:
        prompt = f"cute cartoon animal sticker, {emoji_type} expression, thick black outline, transparent background, high quality, 512x512, {style}"
        text_encode_node["inputs"]["text"] = prompt
    
    url = "http://127.0.0.1:8188/workflow"
    resp = requests.post(url, json=workflow)
    resp.raise_for_status()
    
    print("生成成功！9张图片已保存到 outputs/")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python run_comfy.py <图片路径> <风格> <表情类型>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    style = sys.argv[2]
    emoji = sys.argv[3]
    run_sticker_workflow(image_path, style, emoji)
