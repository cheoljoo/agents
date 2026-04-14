#!/bin/bash
# Copy .gemini .claude .github .vscode to current directory
for dir in .gemini .claude .github .vscode; do
  if [ -d "$dir" ]; then
    cp -r "$dir" ..
    echo "Copied $dir to .."
  else
    echo "$dir does not exist, skipping."
  fi
done
