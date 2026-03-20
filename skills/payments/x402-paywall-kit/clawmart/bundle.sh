#!/usr/bin/env bash
# Bundle the x402-kit for ClawMart upload.
# Creates a tarball with all files needed for the paid listing.
#
# Usage: ./clawmart/bundle.sh
# Output: clawmart/x402-paywall-kit-1.0.0.tar.gz

set -euo pipefail

VERSION="1.0.0"
BUNDLE_NAME="x402-paywall-kit-${VERSION}"
OUT_DIR="clawmart"
TARBALL="${OUT_DIR}/${BUNDLE_NAME}.tar.gz"
STAGING="/tmp/${BUNDLE_NAME}"

echo "Bundling x402-kit v${VERSION} for ClawMart..."

# Build all packages first
echo "Building packages..."
npm run build

# Stage files into a temp directory for clean tarball structure
rm -rf "${STAGING}"
mkdir -p "${STAGING}"

# Copy files preserving directory structure
cp SKILL.md LICENSE package.json tsconfig.json vitest.config.ts "${STAGING}/"
cp -r references/ "${STAGING}/references/"
cp -r demo/ "${STAGING}/demo/"
cp -r x402-agent/ "${STAGING}/x402-agent/"
mkdir -p "${STAGING}/docs"
cp docs/PRD.md "${STAGING}/docs/"

for pkg in shared agent express; do
  mkdir -p "${STAGING}/packages/${pkg}"
  cp -r "packages/${pkg}/src/" "${STAGING}/packages/${pkg}/src/"
  cp "packages/${pkg}/package.json" "${STAGING}/packages/${pkg}/"
  cp "packages/${pkg}/README.md" "${STAGING}/packages/${pkg}/"
  cp "packages/${pkg}/tsconfig.json" "${STAGING}/packages/${pkg}/"
  cp "packages/${pkg}/tsup.config.ts" "${STAGING}/packages/${pkg}/"
done

# Create tarball from staging directory
tar czf "${TARBALL}" -C /tmp "${BUNDLE_NAME}"

# Clean up
rm -rf "${STAGING}"

echo "Created: ${TARBALL}"
echo "Size: $(du -h "${TARBALL}" | cut -f1)"
echo ""
echo "Contents:"
tar tzf "${TARBALL}" | head -20
echo "..."
