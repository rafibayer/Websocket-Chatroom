import yaml
import os


with open("server/config/server.yaml") as f:
    cfg = yaml.safe_load(f)
    print(type(cfg))
    print(cfg)
    hostname = cfg["server"]["host"]
    print(type(hostname))
    print(hostname)