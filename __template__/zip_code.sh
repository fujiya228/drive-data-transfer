#!/bin/bash

# .gcloudignoreファイルの解析とファイル除外
exclude_patterns=""
while IFS= read -r line; do
  # 末尾が/の場合は/*に変換
  if [[ "$line" == */ ]]; then
    line="${line%?}/*"
  fi
  exclude_patterns+=" \"$line\""
done < .gcloudignore

eval "zip -r code.zip . -x $exclude_patterns"
