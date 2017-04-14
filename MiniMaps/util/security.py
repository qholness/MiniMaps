from itsdangerous import URLSafeTimedSerializer

from main import MinimalMaps

ts = URLSafeTimedSerializer(MinimalMaps.config["tempDevConfig"])