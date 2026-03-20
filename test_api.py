#!/usr/bin/env python
"""测试 API 接口"""
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000/api"

def test_get_posts():
    """测试获取文章列表"""
    print("=" * 50)
    print("测试 GET /api/posts/")
    print("=" * 50)
    
    req = urllib.request.Request(f"{BASE_URL}/posts/")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"状态码: {response.status}")
            print(f"文章总数: {data.get('count')}")
            print(f"返回文章数: {len(data.get('results', []))}")
            if data.get('results'):
                print(f"第一篇文章标题: {data['results'][0]['title']}")
            return True
    except urllib.error.HTTPError as e:
        print(f"错误: {e.code}")
        return False

def test_get_posts_pagination():
    """测试文章列表分页"""
    print("\n" + "=" * 50)
    print("测试 GET /api/posts/?page=2&page_size=5")
    print("=" * 50)
    
    req = urllib.request.Request(f"{BASE_URL}/posts/?page=2&page_size=5")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"状态码: {response.status}")
            print(f"文章总数: {data.get('count')}")
            print(f"返回文章数: {len(data.get('results', []))}")
            return True
    except urllib.error.HTTPError as e:
        print(f"错误: {e.code}")
        return False

def test_get_post_detail(post_id):
    """测试获取文章详情"""
    print("\n" + "=" * 50)
    print(f"测试 GET /api/posts/{post_id}/")
    print("=" * 50)
    
    req = urllib.request.Request(f"{BASE_URL}/posts/{post_id}/")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"状态码: {response.status}")
            print(f"文章ID: {data.get('id')}")
            print(f"标题: {data.get('title')}")
            print(f"阅读量: {data.get('views')}")
            print(f"有 body_html: {'body_html' in data}")
            return True
    except urllib.error.HTTPError as e:
        print(f"错误: {e.code}")
        return False

def test_get_post_detail_404():
    """测试获取不存在的文章"""
    print("\n" + "=" * 50)
    print("测试 GET /api/posts/99999/ (404)")
    print("=" * 50)
    
    req = urllib.request.Request(f"{BASE_URL}/posts/99999/")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"状态码: {response.status}")
            return False
    except urllib.error.HTTPError as e:
        print(f"状态码: {e.code} (预期 404)")
        return e.code == 404

def test_get_comments(post_id):
    """测试获取评论列表"""
    print("\n" + "=" * 50)
    print(f"测试 GET /api/posts/{post_id}/comments/")
    print("=" * 50)
    
    req = urllib.request.Request(f"{BASE_URL}/posts/{post_id}/comments/")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"状态码: {response.status}")
            print(f"评论数: {len(data.get('results', []))}")
            return True
    except urllib.error.HTTPError as e:
        print(f"错误: {e.code}")
        return False

def test_create_comment(post_id):
    """测试创建评论"""
    print("\n" + "=" * 50)
    print(f"测试 POST /api/posts/{post_id}/comments/create/")
    print("=" * 50)
    
    data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "text": "这是一篇很好的文章！"
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/posts/{post_id}/comments/create/",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"状态码: {response.status} (预期 201)")
            print(f"评论ID: {result.get('id')}")
            print(f"评论者: {result.get('name')}")
            print(f"评论内容: {result.get('text')}")
            return response.status == 201
    except urllib.error.HTTPError as e:
        print(f"错误: {e.code}")
        error_body = e.read().decode('utf-8')
        print(f"错误详情: {error_body}")
        return False

def test_create_comment_validation_error(post_id):
    """测试创建评论验证失败"""
    print("\n" + "=" * 50)
    print(f"测试 POST /api/posts/{post_id}/comments/create/ (400 验证错误)")
    print("=" * 50)
    
    data = {
        "name": "",  # 空名称，应该验证失败
        "email": "invalid-email",  # 无效邮箱
        "text": ""  # 空内容
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/posts/{post_id}/comments/create/",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"状态码: {response.status}")
            return False
    except urllib.error.HTTPError as e:
        print(f"状态码: {e.code} (预期 400)")
        error_body = json.loads(e.read().decode('utf-8'))
        print(f"错误详情: {json.dumps(error_body, ensure_ascii=False, indent=2)}")
        return e.code == 400 and 'errors' in error_body

def test_create_comment_404():
    """测试对不存在的文章创建评论"""
    print("\n" + "=" * 50)
    print("测试 POST /api/posts/99999/comments/create/ (404)")
    print("=" * 50)
    
    data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "text": "测试评论"
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/posts/99999/comments/create/",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"状态码: {response.status}")
            return False
    except urllib.error.HTTPError as e:
        print(f"状态码: {e.code} (预期 404)")
        return e.code == 404

if __name__ == "__main__":
    print("开始测试 API 接口...\n")
    
    results = []
    
    # 测试文章列表
    results.append(("GET /api/posts/", test_get_posts()))
    results.append(("GET /api/posts/?page=2&page_size=5", test_get_posts_pagination()))
    
    # 获取一个有效的文章ID
    req = urllib.request.Request(f"{BASE_URL}/posts/")
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('results'):
                post_id = data['results'][0]['id']
                
                # 测试文章详情
                results.append((f"GET /api/posts/{post_id}/", test_get_post_detail(post_id)))
                results.append(("GET /api/posts/99999/ (404)", test_get_post_detail_404()))
                
                # 测试评论
                results.append((f"GET /api/posts/{post_id}/comments/", test_get_comments(post_id)))
                results.append((f"POST /api/posts/{post_id}/comments/create/", test_create_comment(post_id)))
                results.append((f"POST /api/posts/{post_id}/comments/create/ (400)", test_create_comment_validation_error(post_id)))
                results.append(("POST /api/posts/99999/comments/create/ (404)", test_create_comment_404()))
                
                # 再次获取评论列表，验证评论已创建
                results.append((f"GET /api/posts/{post_id}/comments/ (after create)", test_get_comments(post_id)))
    except Exception as e:
        print(f"获取文章列表失败: {e}")
    
    # 打印测试结果汇总
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    for name, result in results:
        status = "通过" if result else "失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
