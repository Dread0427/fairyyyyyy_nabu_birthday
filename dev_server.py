#!/usr/bin/env python3
import json, os, re, base64, mimetypes
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, 'site-data.json')
PHOTOS_DIR = os.path.join(ROOT, 'assets', 'photos')
os.makedirs(PHOTOS_DIR, exist_ok=True)

def safe_photo_name(name):
    if not re.fullmatch(r'photo-(0[1-9]|1[0-2])\.(jpg|jpeg|png|webp)', name, re.I):
        return None
    # normalize extension
    base, ext = os.path.splitext(name.lower())
    if ext == '.jpeg': ext = '.jpg'
    return base + ext

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/data':
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {}
            # also report which photos exist
            existing = []
            for i in range(1, 13):
                for ext in ('jpg','png','webp'):
                    fn = f'photo-{i:02d}.{ext}'
                    if os.path.exists(os.path.join(PHOTOS_DIR, fn)):
                        existing.append(fn)
                        break
            data['_photos'] = existing
            return self._send_json(200, data)
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != '/api/save':
            return self._send_json(404, {'ok': False, 'error': 'Not found'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode('utf-8'))
        except Exception as e:
            return self._send_json(400, {'ok': False, 'error': f'Bad request: {e}'})

        saved_photos = []
        photos = payload.get('photos', {})
        if isinstance(photos, dict):
            for key, data_url in photos.items():
                name = safe_photo_name(key)
                if not name or not isinstance(data_url, str):
                    continue
                m = re.match(r'^data:image/(jpeg|jpg|png|webp);base64,(.+)$', data_url, re.DOTALL)
                if not m:
                    continue
                ext = m.group(1).lower()
                if ext == 'jpeg': ext = 'jpg'
                # enforce name ext matches
                name = os.path.splitext(name)[0] + '.' + ext
                try:
                    blob = base64.b64decode(m.group(2))
                except Exception:
                    continue
                # limit ~8MB per photo
                if len(blob) > 8 * 1024 * 1024:
                    continue
                # remove other extensions for same slot
                slot = os.path.splitext(name)[0]
                for e2 in ('jpg','png','webp'):
                    old = os.path.join(PHOTOS_DIR, slot + '.' + e2)
                    if os.path.exists(old) and os.path.basename(old) != name:
                        try: os.remove(old)
                        except: pass
                with open(os.path.join(PHOTOS_DIR, name), 'wb') as f:
                    f.write(blob)
                saved_photos.append(name)

        # Save text data (strip photos blobs)
        data = {
            'page1': {
                'title': str(payload.get('page1', {}).get('title', ''))[:300],
                'subtitle': str(payload.get('page1', {}).get('subtitle', ''))[:300],
                'paragraphs': [str(p)[:2000] for p in payload.get('page1', {}).get('paragraphs', [])[:12]],
                'sign': str(payload.get('page1', {}).get('sign', ''))[:300],
            },
            'memories': []
        }
        for i, mem in enumerate(payload.get('memories', [])[:3]):
            caps = [str(c)[:300] for c in mem.get('captions', [])[:4]]
            while len(caps) < 4: caps.append('')
            data['memories'].append({
                'title': str(mem.get('title', f'Memory 0{i+1}'))[:200],
                'subtitle': str(mem.get('subtitle', 'A few little words under every photo.'))[:300],
                'captions': caps[:4],
            })
        while len(data['memories']) < 3:
            i = len(data['memories'])
            data['memories'].append({'title': f'Memory 0{i+1}','subtitle':'A few little words under every photo.','captions':['','','','']})
        data['last'] = {
            'title': str(payload.get('last', {}).get('title', ''))[:300],
            'paragraphs': [str(p)[:2000] for p in payload.get('last', {}).get('paragraphs', [])[:8]],
            'big': str(payload.get('last', {}).get('big', ''))[:300],
            'small': str(payload.get('last', {}).get('small', ''))[:300],
        }

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return self._send_json(200, {'ok': True, 'saved_photos': saved_photos, 'data_file': 'site-data.json'})

    def log_message(self, fmt, *args):
        print(fmt % args)

if __name__ == '__main__':
    port = 8080
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'Serving on http://127.0.0.1:{port}')
    server.serve_forever()
