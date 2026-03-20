import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_post_list():
    """测试文章列表接口"""
    print('=== 测试 GET /api/posts/ ===')
    response = requests.get(f'{BASE_URL}/posts/')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'返回结构: {list(data.keys())}')
        print(f'总数: {data.get("count")}')
        print(f'结果数量: {len(data.get("results", []))}')
        if data.get('results'):
            print(f'第一条结果字段: {list(data["results"][0].keys())}')
    print()

def test_post_list_pagination():
    """测试文章列表分页"""
    print('=== 测试分页参数 ===')
    response = requests.get(f'{BASE_URL}/posts/', params={'page': 1, 'page_size': 5})
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'每页数量: {len(data.get("results", []))}')
    print()

def test_post_detail_404():
    """测试文章详情 404"""
    print('=== 测试 GET /api/posts/99999/ (404) ===')
    response = requests.get(f'{BASE_URL}/posts/99999/')
    print(f'状态码: {response.status_code} (期望: 404)')
    print()

def test_post_detail():
    """测试文章详情接口"""
    print('=== 测试 GET /api/posts/1/ ===')
    response = requests.get(f'{BASE_URL}/posts/1/')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'返回字段: {list(data.keys())}')
        print(f'包含 body_html: {"body_html" in data}')
        print(f'阅读量: {data.get("views")}')
    print()

def test_comment_list():
    """测试评论列表接口"""
    print('=== 测试 GET /api/posts/1/comments/ ===')
    response = requests.get(f'{BASE_URL}/posts/1/comments/')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'评论数量: {data.get("count")}')
    print()

def test_comment_list_404():
    """测试评论列表 404"""
    print('=== 测试 GET /api/posts/99999/comments/ (404) ===')
    response = requests.get(f'{BASE_URL}/posts/99999/comments/')
    print(f'状态码: {response.status_code} (期望: 404)')
    print()

def test_create_comment():
    """测试创建评论接口"""
    print('=== 测试 POST /api/posts/1/comments/ ===')
    comment_data = {
        'name': '测试用户',
        'email': 'test@example.com',
        'text': '这是一条测试评论',
    }
    response = requests.post(
        f'{BASE_URL}/posts/1/comments/',
        json=comment_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f'状态码: {response.status_code} (期望: 201)')
    if response.status_code == 201:
        data = response.json()
        print(f'新评论 ID: {data.get("id")}')
    print()

def test_create_comment_validation_error():
    """测试创建评论校验错误"""
    print('=== 测试 POST 校验错误 (400) ===')
    comment_data = {
        'name': '',  # 空名称
        'email': 'invalid-email',  # 无效邮箱
        'text': '',  # 空内容
    }
    response = requests.post(
        f'{BASE_URL}/posts/1/comments/',
        json=comment_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f'状态码: {response.status_code} (期望: 400)')
    if response.status_code == 400:
        data = response.json()
        print(f'错误字段: {list(data.get("errors", {}).keys())}')
    print()

def test_create_comment_404():
    """测试创建评论 404"""
    print('=== 测试 POST /api/posts/99999/comments/ (404) ===')
    comment_data = {
        'name': '测试用户',
        'email': 'test@example.com',
        'text': '这是一条测试评论',
    }
    response = requests.post(
        f'{BASE_URL}/posts/99999/comments/',
        json=comment_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f'状态码: {response.status_code} (期望: 404)')
    print()

if __name__ == '__main__':
    print('开始 API 测试...\n')
    test_post_list()
    test_post_list_pagination()
    test_post_detail_404()
    test_post_detail()
    test_comment_list()
    test_comment_list_404()
    test_create_comment()
    test_create_comment_validation_error()
    test_create_comment_404()
    print('测试完成!')
