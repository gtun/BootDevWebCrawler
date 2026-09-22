import sys
import requests

header_user_agent = {"User-Agent": "BootCrawler/1.0"}

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url: str = sys.argv[1]
#    print(f"starting crawl of: {base_url}")
    print(get_html(base_url))
    

def get_html(url: str):
    try:
        response = requests.get(url, headers={
         **header_user_agent
        })
    except Exception as e:
        print(f".get() error: {type(e).__name__}")
    
    #print(f"DEBUG A: {response.headers["Content-Type"]}")
    
    #for key, value in vars(response).items():
    #    print(f"{key}: {value}")
    #print(f"DEBUG A: {response.text}")
    
    if response.status_code // 100 == 4:
        raise Exception("http 4xx error")
    if "text/html" not in response.headers["Content-Type"]:
        raise Exception("content type is not text/html")
    
    return response.text

if __name__ == "__main__":
    main()