"""
한글-러시아어 음역(Transliteration) 유틸리티

한글을 러시아어 키릴 문자로, 러시아어를 한글로 음역합니다.
"""

# 한글 → 러시아어 음역 매핑 (국립국어원 외래어 표기법 기준)
KOREAN_TO_RUSSIAN = {
    # 초성
    'ㄱ': 'к', 'ㄲ': 'кк', 'ㄴ': 'н', 'ㄷ': 'т', 'ㄸ': 'тт',
    'ㄹ': 'р', 'ㅁ': 'м', 'ㅂ': 'п', 'ㅃ': 'пп', 'ㅅ': 'с',
    'ㅆ': 'сс', 'ㅇ': '', 'ㅈ': 'ч', 'ㅉ': 'чч', 'ㅊ': 'чх',
    'ㅋ': 'кх', 'ㅌ': 'тх', 'ㅍ': 'пх', 'ㅎ': 'х',

    # 중성
    'ㅏ': 'а', 'ㅐ': 'э', 'ㅑ': 'я', 'ㅒ': 'е', 'ㅓ': 'о',
    'ㅔ': 'е', 'ㅕ': 'ё', 'ㅖ': 'е', 'ㅗ': 'о', 'ㅘ': 'ва',
    'ㅙ': 'вэ', 'ㅚ': 'ве', 'ㅛ': 'ё', 'ㅜ': 'у', 'ㅝ': 'во',
    'ㅞ': 'ве', 'ㅟ': 'ви', 'ㅠ': 'ю', 'ㅡ': 'ы', 'ㅢ': 'ый',
    'ㅣ': 'и',

    # 종성
    'ㄱ_': 'к', 'ㄲ_': 'к', 'ㄳ_': 'кс', 'ㄴ_': 'н', 'ㄵ_': 'нч',
    'ㄶ_': 'нх', 'ㄷ_': 'т', 'ㄹ_': 'ль', 'ㄺ_': 'льк', 'ㄻ_': 'льм',
    'ㄼ_': 'льп', 'ㄽ_': 'льс', 'ㄾ_': 'льтх', 'ㄿ_': 'льпх', 'ㅀ_': 'льх',
    'ㅁ_': 'м', 'ㅂ_': 'п', 'ㅄ_': 'пс', 'ㅅ_': 'т', 'ㅆ_': 'т',
    'ㅇ_': 'н', 'ㅈ_': 'т', 'ㅊ_': 'т', 'ㅋ_': 'к', 'ㅌ_': 'т',
    'ㅍ_': 'п', 'ㅎ_': 'т',
}

# 러시아어 → 한글 음역 매핑
RUSSIAN_TO_KOREAN = {
    # 자음
    'б': '브', 'в': '브', 'г': '그', 'д': '드', 'ж': '주',
    'з': '즈', 'й': '이', 'к': '크', 'л': '르', 'м': '므',
    'н': '느', 'п': '프', 'р': '르', 'с': '스', 'т': '트',
    'ф': '프', 'х': '흐', 'ц': '츠', 'ч': '치', 'ш': '시',
    'щ': '시', 'ъ': '', 'ы': '이', 'ь': '', 'э': '에',

    # 모음 (단독 또는 자음 앞)
    'а': '아', 'е': '예', 'ё': '요', 'и': '이',
    'о': '오', 'у': '우', 'ю': '유', 'я': '야',

    # 자음 + 모음 조합 (더 자연스러운 발음)
    'ба': '바', 'ва': '바', 'га': '가', 'да': '다', 'жа': '자',
    'за': '자', 'ка': '카', 'ла': '라', 'ма': '마', 'на': '나',
    'па': '파', 'ра': '라', 'са': '사', 'та': '타', 'фа': '파',
    'ха': '하', 'ца': '차', 'ча': '차', 'ша': '샤', 'ща': '샤',

    'бе': '베', 'ве': '베', 'ге': '게', 'де': '데', 'же': '제',
    'зе': '제', 'ке': '케', 'ле': '레', 'ме': '메', 'не': '네',
    'пе': '페', 'ре': '레', 'се': '세', 'те': '테', 'фе': '페',
    'хе': 'хе', 'це': '체', 'че': '체', 'ше': '셰', 'ще': '셰',

    'би': '비', 'ви': '비', 'ги': '기', 'ди': '디', 'жи': '지',
    'зи': '지', 'ки': '키', 'ли': '리', 'ми': '미', 'ни': '니',
    'пи': '피', 'ри': '리', 'си': '시', 'ти': '티', 'фи': '피',
    'хи': '히', 'ци': '치', 'чи': '치', 'ши': 'ши', 'щи': '시',

    'бо': '보', 'во': '보', 'го': '고', 'до': '도', 'жо': '조',
    'зо': '조', 'ко': '코', 'ло': '로', 'мо': '모', 'но': '노',
    'по': '포', 'ро': '로', 'со': '소', 'то': '토', 'фо': '포',
    'хо': '호', 'цо': '초', 'чо': '초', 'шо': 'шо', 'що': '쇼',

    'бу': '부', 'ву': '부', 'гу': '구', 'ду': '두', 'жу': '주',
    'зу': '주', 'ку': '쿠', 'лу': '루', 'му': '무', 'ну': '누',
    'пу': '푸', 'ру': '루', 'су': '수', 'ту': '투', 'фу': '푸',
    'ху': '후', 'цу': '추', 'чу': '추', 'шу': '슈', 'щу': '슈',

    'бы': '비', 'вы': '비', 'гы': '기', 'ды': '디', 'жы': '지',
    'зы': '지', 'кы': '키', 'лы': '리', 'мы': '미', 'ны': '니',
    'пы': '피', 'ры': '리', 'сы': '시', 'ты': '티', 'фы': '피',
    'хы': '히', 'цы': '치', 'чы': '치', 'шы': '시', 'щы': '시',
}


def decompose_hangul(char: str) -> tuple:
    """
    한글 음절을 초성, 중성, 종성으로 분해
    """
    if not ('가' <= char <= '힣'):
        return None, None, None

    code = ord(char) - 0xAC00

    cho = code // (21 * 28)  # 초성
    jung = (code % (21 * 28)) // 28  # 중성
    jong = code % 28  # 종성

    CHO = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    JUNG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    JONG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    return CHO[cho], JUNG[jung], JONG[jong] if jong > 0 else ''


def korean_to_russian(text: str) -> str:
    """
    한글을 러시아어 키릴 문자로 음역

    Args:
        text: 한글 텍스트

    Returns:
        러시아어로 음역된 텍스트
    """
    if not text:
        return ""

    result = []

    for char in text:
        if '가' <= char <= '힣':
            cho, jung, jong = decompose_hangul(char)

            # 초성
            if cho in KOREAN_TO_RUSSIAN:
                result.append(KOREAN_TO_RUSSIAN[cho])

            # 중성
            if jung in KOREAN_TO_RUSSIAN:
                result.append(KOREAN_TO_RUSSIAN[jung])

            # 종성
            if jong and jong + '_' in KOREAN_TO_RUSSIAN:
                result.append(KOREAN_TO_RUSSIAN[jong + '_'])
        else:
            # 한글이 아닌 문자는 그대로 유지
            result.append(char)

    return ''.join(result).capitalize()


def russian_to_korean(text: str) -> str:
    """
    러시아어 키릴 문자를 한글로 음역

    Args:
        text: 러시아어 텍스트

    Returns:
        한글로 음역된 텍스트
    """
    if not text:
        return ""

    text = text.lower()
    result = []
    i = 0

    while i < len(text):
        # 2글자 조합 먼저 확인 (자음+모음)
        if i + 1 < len(text):
            two_char = text[i:i+2]
            if two_char in RUSSIAN_TO_KOREAN:
                result.append(RUSSIAN_TO_KOREAN[two_char])
                i += 2
                continue

        # 단일 문자 확인
        char = text[i]
        if char in RUSSIAN_TO_KOREAN:
            result.append(RUSSIAN_TO_KOREAN[char])
        else:
            # 매핑되지 않은 문자는 그대로 유지
            result.append(char)
        i += 1

    return ''.join(result)


def detect_language(text: str) -> str:
    """
    텍스트의 언어 감지 (한글 또는 러시아어)

    Args:
        text: 감지할 텍스트

    Returns:
        'ko' (한글), 'ru' (러시아어), 'unknown' (알 수 없음)
    """
    if not text:
        return 'unknown'

    korean_chars = sum(1 for c in text if '가' <= c <= '힣' or 'ㄱ' <= c <= 'ㅣ')
    russian_chars = sum(1 for c in text if 'а' <= c.lower() <= 'я' or c.lower() in 'ёъь')

    total_chars = len([c for c in text if c.strip()])

    if total_chars == 0:
        return 'unknown'

    korean_ratio = korean_chars / total_chars
    russian_ratio = russian_chars / total_chars

    if korean_ratio > 0.3:
        return 'ko'
    elif russian_ratio > 0.3:
        return 'ru'
    else:
        return 'unknown'


def transliterate_nickname(nickname: str) -> tuple:
    """
    닉네임을 감지하여 자동으로 양쪽 언어로 음역

    Args:
        nickname: 원본 닉네임

    Returns:
        (nickname_ko, nickname_ru) 튜플
    """
    if not nickname:
        return "", ""

    lang = detect_language(nickname)

    if lang == 'ko':
        # 한글 닉네임 → 러시아어로 음역
        return nickname, korean_to_russian(nickname)
    elif lang == 'ru':
        # 러시아어 닉네임 → 한글로 음역
        return russian_to_korean(nickname), nickname
    else:
        # 알 수 없는 언어는 원본 그대로
        return nickname, nickname
