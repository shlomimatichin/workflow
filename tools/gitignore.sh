#!/bin/sh
cat > $1/.gitignore << EOF
*.pyc
EOF
git add $1/.gitignore
