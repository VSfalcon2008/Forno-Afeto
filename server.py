"""Servidor demonstrativo local para a pizzaria Forno & Afeto (Python stdlib)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json
import os
import secrets
import threading
from datetime import datetime

ROOT = Path(__file__).resolve().parent
ORDERS = {}
CHATS = {}
RESERVATIONS = {}
LOCK = threading.Lock()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/chat':
            order_id = parse_qs(parsed.query).get('orderId', [''])[0]
            with LOCK:
                messages = CHATS.get(order_id, [])
            return self._json(200, {'messages': messages})
        if parsed.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        try:
            length = min(int(self.headers.get('Content-Length', '0')), 200_000)
            data = json.loads(self.rfile.read(length) or b'{}')
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {'error': 'JSON inválido'})

        if parsed.path == '/api/orders':
            order_id = secrets.token_hex(3).upper()
            safe_order = {key: data.get(key) for key in ('item', 'category', 'base', 'total', 'flavor', 'crust', 'drinks', 'name', 'address', 'method')}
            safe_order.update({'orderId': order_id, 'status': 'Em preparo', 'createdAt': datetime.now().isoformat(timespec='seconds')})
            with LOCK:
                ORDERS[order_id] = safe_order
                CHATS[order_id] = [{'sender': 'attendant', 'message': f"Oi, {safe_order.get('name') or 'tudo bem'}! 🍕 Seu pedido chegou pra gente e já estamos preparando tudo com carinho.", 'time': 'Agora'}]
            return self._json(201, {'orderId': order_id, 'status': 'Em preparo'})

        if parsed.path == '/api/reservations':
            required = ('name', 'contact', 'date', 'time', 'guests')
            if any(not str(data.get(key) or '').strip() for key in required):
                return self._json(400, {'error': 'Preencha nome, contato, data, horário e número de pessoas.'})
            reservation_id = secrets.token_hex(3).upper()
            reservation = {key: str(data.get(key) or '').strip()[:300] for key in (*required, 'occasion', 'notes')}
            reservation['reservationId'] = reservation_id
            with LOCK:
                RESERVATIONS[reservation_id] = reservation
            return self._json(201, {'reservationId': reservation_id, 'demo': True})

        if parsed.path == '/api/payment/pix':
            # O código é deliberadamente apenas ilustrativo: não representa cobrança Pix.
            total = float(data.get('total') or 0)
            return self._json(200, {'payload': f"DEMO-FORNO-{data.get('orderId', 'SEM-PEDIDO')}-{total:.2f}", 'simulated': True})

        if parsed.path == '/api/chat':
            order_id = str(data.get('orderId') or 'local')[:40]
            message = str(data.get('message') or '').strip()[:500]
            if not message:
                return self._json(400, {'error': 'Mensagem vazia'})
            now = datetime.now().strftime('%H:%M')
            with LOCK:
                messages = CHATS.setdefault(order_id, [])
                messages.append({'sender': 'customer', 'message': message, 'time': now})
                messages.append({'sender': 'attendant', 'message': 'Recebemos sua mensagem! Nosso atendente já vai falar com você. 😊', 'time': now})
            return self._json(200, {'reply': 'Recebemos sua mensagem! Nosso atendente já vai falar com você. 😊'})

        self._json(404, {'error': 'Rota não encontrada'})

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', '8000'))
    print(f'Forno & Afeto disponível em http://{host}:{port}')
    print('Demonstração local: pagamentos e atendimento são simulados.')
    ThreadingHTTPServer((host, port), Handler).serve_forever()
