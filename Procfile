web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --worker-class sync --max-requests 1000 --max-requests-jitter 50 --preload --worker-tmp-dir /dev/shm
