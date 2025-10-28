import { getRequestConfig } from 'next-intl/server'
import { cookies } from 'next/headers'

export default getRequestConfig(async () => {
  // 쿠키에서 언어 설정 읽기 또는 기본값 사용
  const cookieStore = cookies()
  const locale = cookieStore.get('locale')?.value || 'ko'

  return {
    locale,
    messages: (await import(`../locales/${locale}.json`)).default
  }
})