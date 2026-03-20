import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_get_posts():
    """测试获取文章列表"""
    print("=== 测试 GET /api/posts/ ===")
    response = requests.get(f'{BASE_URL}/posts/')
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
        except:
            print(f"响应文本: {response.text[:500]}")
    else:
        print(f"响应文本: {response.text[:1000]}")
    print()

def test_get_post_detail():
    """测试获取文章详情"""
    print("=== 测试 GET /api/posts/1/ ===")
    response = requests.get(f'{BASE_URL}/posts/1/')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
    else:
        print(f"响应文本: {response.text[:500]}")
    print()

if __name__ == '__main__':
    test_get_posts()
    test_get_post_detail()
