from flask import Blueprint, request, jsonify
from ..services.transaction_service import TransactionService

bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")
_svc = TransactionService()


def _ok(data, status=200):
    return jsonify({"success": True, "data": data}), status

def _err(msg, status=400):
    return jsonify({"success": False, "error": msg}), status


@bp.get("")
def list_transactions():
    return _ok([tx.to_dict() for tx in _svc.list(
        date_from=request.args.get("date_from"),
        date_to=request.args.get("date_to"),
        tx_type=request.args.get("type"),
        limit=request.args.get("limit", type=int),
    )])


@bp.post("")
def create_transaction():
    body = request.get_json(silent=True) or {}
    try:
        tx = _svc.create(
            tx_type=body.get("type", ""),
            amount=body.get("amount", 0),
            tx_date=body.get("date"),
            category_id=body.get("category_id"),
            note=body.get("note"),
        )
        return _ok(tx.to_dict(), 201)
    except ValueError as e:
        return _err(str(e))


@bp.delete("/<int:tx_id>")
def delete_transaction(tx_id):
    try:
        _svc.delete(tx_id)
        return _ok({"id": tx_id})
    except ValueError as e:
        return _err(str(e), 404)
