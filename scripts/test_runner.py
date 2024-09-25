import subprocess
import sys

def run_tests():
    try:
        # Run the docker-compose command
        result = subprocess.run(
            ["docker-compose", "-f", "docker-compose.test.yml", "up", "--build", "--abort-on-container-exit"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Filter and print the test-related output
        for line in result.stdout.splitlines():
            if "test" in line or "warning" in line or "passed" in line or "failed" in line:
                print(line)
        
        for line in result.stderr.splitlines():
            if "test" in line or "warning" in line or "passed" in line or "failed" in line:
                print(line, file=sys.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_tests()