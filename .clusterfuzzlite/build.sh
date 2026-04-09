#!/bin/bash
set -euo pipefail

cd "$SRC/newsdom-api"

pip3 install . pyinstaller atheris

for fuzzer in $(find fuzzers -name '*_fuzzer.py'); do
	fuzzer_basename=$(basename -s .py "$fuzzer")
	fuzzer_package="${fuzzer_basename}.pkg"

	pyinstaller --distpath "$OUT" --onefile --name "$fuzzer_package" "$fuzzer"

	cat >"$OUT/$fuzzer_basename" <<EOF
#!/bin/sh
this_dir=\$(dirname "\$0")
exec "\$this_dir/$fuzzer_package" "\$@"
EOF
	chmod +x "$OUT/$fuzzer_basename"
done
