import os, sys, json, hashlib, importlib
from google.protobuf import json_format, message

# Ensure we can import generated code: run with PYTHONPATH=gen/python
if not any("gen/python" in p for p in sys.path):
    sys.path.append(os.path.join(os.getcwd(), "gen", "python"))

# Mapping: sample file -> (module, message class)
TABLE = [
    ("samples/bars/typical.json",            "ampy.bars.v1.bars_pb2",              "BarBatch"),
    ("samples/ticks/trade_typical.json",     "ampy.ticks.v1.ticks_pb2",            "TickBatch"),
    ("samples/fundamentals/typical.json",    "ampy.fundamentals.v1.fundamentals_pb2","FundamentalsBatch"),
    ("samples/news/typical.json",            "ampy.news.v1.news_pb2",              "NewsBatch"),
    ("samples/fx/typical.json",              "ampy.fx.v1.fx_pb2",                   "FxRateBatch"),
    ("samples/corporate_actions/split_typical.json","ampy.corporate_actions.v1.corporate_actions_pb2","CorporateActionBatch"),
    ("samples/universe/typical.json",        "ampy.universe.v1.universe_pb2",      "UniverseBatch"),
    ("samples/signals/alpha_typical.json",   "ampy.signals.v1.signals_pb2",        "SignalBatch"),
    ("samples/orders/limit_typical.json",    "ampy.orders.v1.orders_pb2",          "OrderRequestBatch"),
    ("samples/fills/partial_typical.json",   "ampy.fills.v1.fills_pb2",            "FillBatch"),
    ("samples/positions/typical.json",       "ampy.positions.v1.positions_pb2",    "PositionBatch"),
    ("samples/metrics/typical.json",         "ampy.metrics.v1.metrics_pb2",        "MetricBatch"),
]

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def roundtrip_one(path: str, modname: str, clsname: str) -> None:
    mod = importlib.import_module(modname)
    cls = getattr(mod, clsname)
    msg = cls()
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    # Parse from JSON -> message
    json_format.Parse(data, msg)

    # Serialize to bytes -> reparse -> bytes -> compare
    b1 = msg.SerializeToString()
    msg2 = cls()
    msg2.ParseFromString(b1)
    b2 = msg2.SerializeToString()

    # For protobuf maps, byte comparison may fail due to key ordering
    # So we compare the semantic content instead
    d1 = json_format.MessageToDict(msg, preserving_proto_field_name=False)
    d2 = json_format.MessageToDict(msg2, preserving_proto_field_name=False)
    
    # Normalize map ordering for comparison
    def normalize_maps(obj):
        if isinstance(obj, dict):
            # Sort map keys recursively
            result = {}
            for k, v in obj.items():
                result[k] = normalize_maps(v)
            return result
        elif isinstance(obj, list):
            return [normalize_maps(item) for item in obj]
        else:
            return obj
    
    d1_normalized = normalize_maps(d1)
    d2_normalized = normalize_maps(d2)
    
    ok = (d1_normalized == d2_normalized)
    print(f"[{'PASS' if ok else 'FAIL'}] {path}  sha={sha(b1)[:12]}")
    if not ok:
        print("Semantic mismatch after roundtrip")
        print("Original:", json.dumps(d1_normalized, indent=2, sort_keys=True)[:500])
        print("Roundtrip:", json.dumps(d2_normalized, indent=2, sort_keys=True)[:500])
        sys.exit(1)

if __name__ == "__main__":
    # Quick env guard
    try:
        import google.protobuf  # noqa
    except Exception:
        print("Please `pip install protobuf` and re-run.")
        sys.exit(2)

    any_fail = False
    for path, mod, cls in TABLE:
        try:
            roundtrip_one(path, mod, cls)
        except message.DecodeError as e:
            print(f"[FAIL] {path} decode error: {e}")
            any_fail = True
        except FileNotFoundError:
            print(f"[SKIP] {path} (missing)")
        except Exception as e:
            print(f"[FAIL] {path} unexpected error: {e}")
            any_fail = True
    sys.exit(1 if any_fail else 0)
