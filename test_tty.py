import sys
import time

print("Testing TTY behavior...")
print(f"isatty(): {sys.stdin.isatty()}")

if sys.stdin.isatty():
    print("\n=== TEST CLI ===", file=sys.stderr)
    print("This is a TTY terminal", file=sys.stderr)
    print("Type something and press Ctrl+D:", file=sys.stderr)
    
    data = sys.stdin.read()
    print("\n=== PROCESSING ===", file=sys.stderr)
    print(f"Read {len(data)} characters", file=sys.stderr)
else:
    data = sys.stdin.read()
    print("Non-interactive mode", file=sys.stderr)
    print(f"Read {len(data)} characters", file=sys.stderr)

print("\nTest complete")
