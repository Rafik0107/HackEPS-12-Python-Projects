import pathlib, subprocess, sys

root = pathlib.Path(__file__).parent
for folder in sorted([p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")]):
    if folder.is_dir():
        print("TEST:",folder.name,flush=True)
        subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=folder,check=True)
print("All projects passed")
