import os
import subprocess
from datetime import datetime

# 1. Geração automática de código (exemplo: novo módulo no PayloadBuilder)
NEW_CODE = """
    def for_rings_with_chaos(self):
        return {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {"filters": {"category": {"option": "accessory.ring"}}},
                    "misc_filters": {"filters": {"chaos_resistance": {"min": 20}}}
                }
            },
            "sort": {"price": "asc"}
        }
"""

def inject_code():
    file_path = "core/payload_builder.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "for_rings_with_chaos" not in content:
        # insere antes do final da classe
        content = content.replace("    # 🚀 Novo módulo sugerido pela IA", NEW_CODE)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Novo método for_rings_with_chaos() adicionado.")
    else:
        print("⚠️ Método já existe, nada a fazer.")

def run_tests():
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def git_commit():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Auto-commit: add rings_with_chaos ({now})"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("🚀 Commit enviado para o GitHub.")

if __name__ == "__main__":
    inject_code()
    if run_tests():
        git_commit()
    else:
        print("❌ Testes falharam, commit cancelado.")
