import subprocess
from pathlib import Path


WORKERS = [
    Path("iot-worker"),
    Path("db-worker")
]

def deploy_worker(worker_path: Path):
    if not worker_path.exists():
        print(f"[!] - Worker path doesn't exist: {worker_path}")
        return
    
    print(f'\nDeploying worker: {worker_path.name}')

    subprocess.run(
        ['npx', 'wrangler', 'deploy'],
        cwd=worker_path,
        check=True
    )

def main():
    for worker in WORKERS:
        deploy_worker(worker)

    print('\n\n\n[x] - All workers are now deployed to Cloudflare!')

if __name__ == "__main__":
    main()
