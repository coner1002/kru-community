#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
게시판별 글쓰기 버튼 권한 수정
- 공지사항: 관리자만
- 나머지 게시판: 로그인한 사용자 모두
"""

import re

# 공지사항을 제외한 일반 게시판 파일들
regular_boards = [
    'board-life.html',
    'board-admin.html',
    'board-job.html',
    'board-market.html',
    'board-startup.html',
]

# 공지사항 게시판
notice_board = 'board-notice.html'

def update_regular_boards():
    """일반 게시판: 로그인한 사용자 모두 글쓰기 가능"""
    old_pattern = r'// 관리자 권한 체크 및 글쓰기 버튼 표시.*?}\s*}\s*}\s*}\)'

    new_code = """// 로그인 사용자 권한 체크 및 글쓰기 버튼 표시 (로그인한 사용자 모두 글쓰기 가능)
            const userInfoStr = localStorage.getItem('userInfo');
            if (userInfoStr) {
                try {
                    const userInfo = JSON.parse(userInfoStr);
                    // 로그인한 사용자 모두 글쓰기 가능
                    const writeBtn = document.getElementById('writeBtn');
                    if (writeBtn) {
                        writeBtn.style.display = 'inline-block';
                    }
                } catch (e) {
                    console.error('사용자 정보 파싱 오류:', e);
                }
            }
        })"""

    for filename in regular_boards:
        print(f'Processing {filename}...')
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            if re.search(old_pattern, content, re.DOTALL):
                content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'  SUCCESS: Updated {filename}')
            else:
                print(f'  SKIP: Pattern not found in {filename}')
        except Exception as e:
            print(f'  ERROR: {filename} - {e}')

def update_notice_board():
    """공지사항 게시판: 관리자만 글쓰기 가능"""
    old_pattern = r'// 관리자 권한 체크 및 글쓰기 버튼 표시.*?}\s*}\s*}\s*}\)'

    new_code = """// 관리자 권한 체크 및 글쓰기 버튼 표시 (공지사항은 관리자만 작성 가능)
            const userInfoStr = localStorage.getItem('userInfo');
            if (userInfoStr) {
                try {
                    const userInfo = JSON.parse(userInfoStr);
                    const isAdmin = userInfo.role === 'admin' || userInfo.role === 'moderator';

                    // 관리자만 글쓰기 버튼 표시
                    if (isAdmin) {
                        const writeBtn = document.getElementById('writeBtn');
                        if (writeBtn) {
                            writeBtn.style.display = 'inline-block';
                        }
                    }
                } catch (e) {
                    console.error('사용자 정보 파싱 오류:', e);
                }
            }
        })"""

    print(f'Processing {notice_board}...')
    try:
        with open(notice_board, 'r', encoding='utf-8') as f:
            content = f.read()

        if re.search(old_pattern, content, re.DOTALL):
            content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

            with open(notice_board, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  SUCCESS: Updated {notice_board}')
        else:
            print(f'  SKIP: Pattern not found in {notice_board}')
    except Exception as e:
        print(f'  ERROR: {notice_board} - {e}')

if __name__ == '__main__':
    print('=== Updating Regular Boards (Logged in users can write) ===\n')
    update_regular_boards()

    print('\n=== Updating Notice Board (Admin only) ===\n')
    update_notice_board()

    print('\nComplete!')
