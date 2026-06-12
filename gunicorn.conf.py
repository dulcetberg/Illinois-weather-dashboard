import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8050')}"
workers = 2
