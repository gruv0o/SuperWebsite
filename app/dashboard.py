from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
@bp.route('/')
def index():
    db = get_db()
    vault = db.execute()