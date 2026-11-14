#!/usr/bin/env sh

echo '=== [Deploy Stage] Menghentikan proses aplikasi setelah jeda 1 menit ==='
set -x
kill $(cat .pidfile)
rm -f .pidfile
set +x
echo 'Aplikasi telah dihentikan secara otomatis dan Deploy stage selesai dengan sukses.'
