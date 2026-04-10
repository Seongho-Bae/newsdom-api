#!/bin/bash
set -euo pipefail

cd "$SRC/newsdom-api"

uv sync --frozen --extra fuzz
export PATH="$SRC/newsdom-api/.venv/bin:$PATH"

while IFS= read -r -d '' fuzzer; do
	fuzzer_basename=$(basename "$fuzzer" .py)
	fuzzer_package="${fuzzer_basename}.pkg"

	pyinstaller --distpath "$OUT" --onefile --name "$fuzzer_package" "$fuzzer"

	cat >"$OUT/$fuzzer_basename" <<EOF
#!/bin/sh
this_dir=\$(dirname "\$0")
exec "\$this_dir/$fuzzer_package" "\$@"
EOF
	chmod +x "$OUT/$fuzzer_basename"
done < <(find fuzzers -type f -name '*_fuzzer.py' -print0)
