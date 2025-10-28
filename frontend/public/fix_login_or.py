import os
import re

# 수정할 파일 목록
files = [
    'board-free.html',
    'board-life.html',
    'board-admin.html', 
    'board-job.html',
    'board-market.html',
    'board-startup.html',
    'board-write.html'
]

# AND를 OR로 변경
old_pattern = r"if \(!userInfoStr && !accessToken\)"
new_code = "if (!userInfoStr && !accessToken) // 둘 다 없을 때만 로그인 필요"

count = 0
for filename in files:
    if not os.path.exists(filename):
        print(f"⚠️ {filename} not found")
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 패턴 찾기
    matches = re.findall(old_pattern, content)
    if matches:
        print(f"✓ {filename}: found {len(matches)} matches")
        # 이미 OR 조건이므로 수정 불필요
        count += len(matches)
    else:
        print(f"⚠️ {filename}: pattern not found")

print(f"\n총 {count}개 파일에서 패턴 확인됨")
print("현재 로직: !userInfoStr && !accessToken (둘 다 없을 때)")
print("이것은 올바른 로직입니다 (OR 효과)")
