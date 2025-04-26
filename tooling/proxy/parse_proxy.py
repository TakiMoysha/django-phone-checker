def parse_proxy_json(json):
    for ip, details in json.items():
        print(f"{ip}:{details['port']}")


PROXY_LIST = {}

if __name__ == "__main__":
    parse_proxy_json(PROXY_LIST)
