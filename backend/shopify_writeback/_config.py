"""Shared config for shopify_writeback scripts. Data lives in ../shopify_app/"""
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'shopify_app')

STORE_URL = os.environ.get("SHOPIFY_STORE_URL", "")
ACCESS_TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")
API_VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-01")
