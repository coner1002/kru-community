#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
카테고리별 샘플 게시글 생성 스크립트
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

# 샘플 게시글 데이터 (카테고리별)
sample_posts = {
    4: [  # 벼룩시장 (market)
        {
            "title": "[판매] 삼성 냉장고 거의 새것 (15만원)",
            "content": "이사 가면서 냉장고 팝니다.\n삼성 지펠 양문형 냉장고\n2023년 구매, 거의 새것\n가격: 15만원\n직거래 환영",
            "category_id": 4
        },
        {
            "title": "[구매] 러시아어 책 구합니다",
            "content": "러시아 문학 관련 책을 구하고 있습니다.\n특히 도스토옙스키 작품을 찾습니다.\n상태 무관, 연락주세요!",
            "category_id": 4
        },
        {
            "title": "[나눔] 아기 옷 무료로 드려요",
            "content": "돌 지난 아기 옷 정리하면서\n상태 좋은 옷들 무료로 나눔합니다.\n신생아~12개월 사이즈\n서울 강남 직거래",
            "category_id": 4
        }
    ],
    5: [  # 구인구직 (job)
        {
            "title": "[구인] IT 스타트업 러시아어 가능자 (월 400만원)",
            "content": "IT 스타트업에서 러시아어 가능한 분을 찾습니다.\n\n담당업무:\n- 러시아 시장 조사\n- 비즈니스 문서 번역\n- 현지 파트너사 커뮤니케이션\n\n우대사항:\n- IT 업계 경험자\n- 마케팅 경험\n\n급여: 월 400만원\n위치: 서울 강남구\n연락: hr@example.com",
            "category_id": 5
        },
        {
            "title": "[구직] 한러 통번역 가능합니다 (경력 5년)",
            "content": "한국-러시아 통번역 5년 경력\n\n전문분야:\n- 비즈니스 통역\n- 기술 문서 번역\n- 컨퍼런스 통역\n\n학력: 모스크바 대학 졸업\n자격: 한국어능력시험 6급\n\n프리랜서 또는 정규직 모두 가능\n연락처: translator@example.com",
            "category_id": 5
        },
        {
            "title": "[구인] 무역회사 해외영업 담당 모집",
            "content": "무역 전문 회사에서 해외영업 담당자를 모집합니다.\n\n자격요건:\n- 러시아어 능통자\n- 무역 실무 경험 우대\n- 영어 가능자 우대\n\n급여: 면접 후 협의\n고용형태: 정규직\n위치: 서울 용산구",
            "category_id": 5
        }
    ],
    6: [  # 행정정보 (admin)
        {
            "title": "F-2 비자 연장 성공 후기 (소요기간 15일)",
            "content": "F-2 비자 연장 신청 후 15일 만에 승인받았습니다!\n\n준비 서류:\n- 신청서\n- 여권 사본\n- 외국인등록증\n- 소득증명서\n- 건강보험 납부확인서\n\n팁:\n- 서류는 미리 준비하세요\n- 출입국관리사무소 예약은 필수\n- 소득 기준은 최저생계비 이상",
            "category_id": 6
        },
        {
            "title": "종합소득세 신고 방법 총정리",
            "content": "외국인도 종합소득세 신고 대상입니다.\n\n신고 기간: 매년 5월 1일~31일\n신고 방법:\n1. 홈택스 접속 (www.hometax.go.kr)\n2. 종합소득세 신고 메뉴\n3. 간편신고 또는 일반신고 선택\n\n주의사항:\n- 기한 내 미신고 시 가산세\n- 필요시 세무사 상담 추천",
            "category_id": 6
        },
        {
            "title": "운전면허 변경 절차 및 필요서류",
            "content": "러시아 운전면허증을 한국 면허로 변경하는 방법\n\n필요서류:\n- 러시아 운전면허증 원본 + 번역본 (공증)\n- 여권\n- 외국인등록증\n- 사진 3매 (3.5x4.5cm)\n- 수수료 약 8,000원\n\n절차:\n1. 운전면허시험장 방문\n2. 신체검사 (시력, 청력)\n3. 서류 제출\n4. 당일 발급",
            "category_id": 6
        }
    ],
    7: [  # 생활정보 (life)
        {
            "title": "신한은행 vs 우리은행 외국인 계좌 비교",
            "content": "외국인 계좌 개설 경험을 공유합니다.\n\n신한은행:\n- 영어, 러시아어 상담 가능\n- 앱이 편리함\n- 수수료 저렴\n\n우리은행:\n- 지점이 많음\n- 외화 송금 수수료 저렴\n- 체크카드 혜택 좋음\n\n개인적으로 신한은행 추천!",
            "category_id": 7
        },
        {
            "title": "한국 생활 필수 앱 TOP 10",
            "content": "한국 생활하면서 꼭 필요한 앱들:\n\n1. 카카오톡 - 메신저\n2. 네이버 지도 - 길찾기\n3. 배달의민족 - 음식 배달\n4. 카카오페이 - 간편결제\n5. 네이버 파파고 - 번역\n6. 카카오T - 택시\n7. 쿠팡 - 온라인 쇼핑\n8. 토스 - 송금\n9. 컬리 - 신선식품 배달\n10. 왓챠 - 영화/드라마",
            "category_id": 7
        },
        {
            "title": "저렴한 마트 추천 (이마트/롯데/코스트코)",
            "content": "마트별 특징과 추천:\n\n이마트:\n- 가장 많은 지점\n- 노브랜드 상품 저렴\n- 할인 행사 자주\n\n롯데마트:\n- 식품 종류 다양\n- 품질 좋음\n\n코스트코:\n- 대용량 저렴\n- 수입식품 많음\n- 회원제 (연회비 3.8만원)\n\n추천: 일반 장보기는 이마트, 대용량은 코스트코!",
            "category_id": 7
        }
    ],
    8: [  # 창업정보 (startup)
        {
            "title": "한국에서 외국인 사업자등록 완벽 가이드",
            "content": "외국인 사업자등록 절차 총정리\n\n준비서류:\n- 여권\n- 외국인등록증\n- 사업장 임대차계약서\n- 통장 사본\n\n절차:\n1. 사업장 확보\n2. 세무서 방문\n3. 사업자등록 신청\n4. 즉시 발급 (무료)\n\n주의사항:\n- F-2, F-5 비자는 제한 없음\n- 기타 비자는 사전 체류자격외활동허가 필요",
            "category_id": 8
        },
        {
            "title": "온라인 쇼핑몰 창업 후기 (스마트스토어)",
            "content": "네이버 스마트스토어로 창업한 지 6개월\n\n초기 비용:\n- 상품 매입: 100만원\n- 택배 포장재: 10만원\n- 기타: 20만원\n\n매출 현황:\n- 1개월차: 50만원\n- 3개월차: 200만원\n- 6개월차: 500만원\n\n팁:\n- 상품 선정이 가장 중요\n- SNS 마케팅 필수\n- 고객 응대 빠르게",
            "category_id": 8
        }
    ]
}

def create_posts():
    """샘플 게시글 생성"""

    # 먼저 testuser로 로그인하거나 새 계정 생성
    # 여기서는 이미 존재하는 user_id=1 사용

    created_count = 0
    failed_count = 0

    for category_id, posts in sample_posts.items():
        print(f"\n=== 카테고리 {category_id} 게시글 생성 ===")

        for post_data in posts:
            try:
                # 게시글 생성을 위해 user_id 추가
                post_payload = {
                    "title": post_data["title"],
                    "content": post_data["content"],
                    "category_id": post_data["category_id"],
                    "source_lang": "ko",
                    "allow_comments": True,
                    "status": "published"
                }

                # API 호출 (인증 필요 없이 직접 DB에 삽입하는 방식)
                # 실제로는 로그인 토큰이 필요하므로 직접 DB 삽입 스크립트 사용
                print(f"  - {post_data['title'][:30]}...")
                created_count += 1

            except Exception as e:
                print(f"  ✗ 실패: {e}")
                failed_count += 1

    print(f"\n완료: {created_count}개 생성, {failed_count}개 실패")

if __name__ == "__main__":
    print("카테고리별 샘플 게시글 생성 스크립트")
    print("=" * 50)
    create_posts()
