#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 board-*.html 파일의 인증 헤더 로직을 수정하는 스크립트
"""

import os
import re

# 수정할 파일 리스트
files = [
    'public/board-free.html',
    'public/board-life.html',
    'public/board-job.html',
    'public/board-market.html',
    'public/board-startup.html',
    'public/board-notice.html',
]

# 찾을 패턴 (이전 코드)
old_pattern = r'''            try \{
                // 로그인 토큰 가져오기
                const userInfo = localStorage\.getItem\('userInfo'\);
                const headers = \{\};

                if \(userInfo\) \{
                    const user = JSON\.parse\(userInfo\);
                    if \(user\.access_token\) \{
                        headers\['Authorization'\] = `Bearer \$\{user\.access_token\}`;
                    \}
                \}'''

# 새로운 코드
new_code = '''            try {
                // 로그인 토큰 가져오기
                const userInfoStr = localStorage.getItem('userInfo');
                const accessToken = localStorage.getItem('access_token');
                const token = accessToken || (userInfoStr ? JSON.parse(userInfoStr).access_token : null);

                const headers = {};
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }'''

for filename in files:
    filepath = os.path.join(os.path.dirname(__file__), filename)

    if not os.path.exists(filepath):
        print(f"⚠️  파일 없음: {filename}")
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 패턴 매칭 및 교체
        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, new_code, content)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ 수정 완료: {filename}")
        else:
            # 대안: 간단한 문자열 교체 시도
            old_simple = """            try {
                // 로그인 토큰 가져오기
                const userInfo = localStorage.getItem('userInfo');
                const headers = {};

                if (userInfo) {
                    const user = JSON.parse(userInfo);
                    if (user.access_token) {
                        headers['Authorization'] = `Bearer ${user.access_token}`;
                    }
                }"""

            if old_simple in content:
                new_content = content.replace(old_simple, new_code)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"✅ 수정 완료 (문자열 교체): {filename}")
            else:
                print(f"⚠️  패턴 없음: {filename}")

    except Exception as e:
        print(f"❌ 오류 ({filename}): {e}")

print("\n🎉 모든 파일 처리 완료!")
