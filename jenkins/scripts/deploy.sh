#!/usr/bin/env sh

echo '=== [Deploy Stage] Menjalankan binary CLI hasil PyInstaller ==='
set -x
./dist/add2vals 25 75
set +x

echo '=== [Deploy Stage] Menjalankan Python Web Application di background ==='
set -x
PORT=5050 python3 sources/web_app.py > /tmp/python_web_app.log 2>&1 &
sleep 1
echo $! > .pidfile
set +x

echo '=== [Deploy Stage] Verifikasi aplikasi berjalan di Localhost (port 5050) & Cloud Render.com ==='
set -x
curl -s http://localhost:5050/health || true
curl -s https://submission-cicd-irfx-programmer.onrender.com/health || true
set +x

echo 'Aplikasi Python Web telah berhasil di-deploy (PID: '$(cat .pidfile)').'
echo 'Menjeda eksekusi pipeline selama 1 menit sebelum aplikasi dihentikan otomatis...'
