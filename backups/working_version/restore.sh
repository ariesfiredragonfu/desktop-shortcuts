#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TEMPLATE_FILE="${PROJECT_ROOT}/howell-forge-template.html"
TARGET_DIR="${1:-${PROJECT_ROOT}}"
TARGET_FILE="${TARGET_DIR}/index.html"

if [[ ! -f "${TEMPLATE_FILE}" ]]; then
  echo "Error: template file not found at ${TEMPLATE_FILE}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

if [[ -f "${TARGET_FILE}" ]]; then
  TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
  BACKUP_FILE="${TARGET_DIR}/index.html.backup.${TIMESTAMP}"
  cp "${TARGET_FILE}" "${BACKUP_FILE}"
  echo "Backed up existing index.html to ${BACKUP_FILE}"
fi

cp "${TEMPLATE_FILE}" "${TARGET_FILE}"
echo "Restored website file to ${TARGET_FILE}"
