import { useTranslations } from 'next-intl'

export default function CommunityStats() {
  const t = useTranslations('HomePage')

  const stats = [
    {
      number: '2,547',
      label: '총 회원수',
      icon: '👥'
    },
    {
      number: '8,932',
      label: '총 게시글',
      icon: '📝'
    },
    {
      number: '156',
      label: '파트너 업체',
      icon: '🤝'
    },
    {
      number: '24/7',
      label: '번역 서비스',
      icon: '🌐'
    }
  ]

  return (
    <div className="text-center">
      <h2 className="text-3xl font-bold mb-8">
        함께 성장하는 커뮤니티
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-2">
              {stat.icon}
            </div>
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {stat.number}
            </div>
            <div className="text-gray-600">
              {stat.label}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <p className="text-gray-600 max-w-2xl mx-auto">
          한국에서의 새로운 시작을 함께하는 따뜻한 커뮤니티입니다.
          궁금한 것이 있으시면 언제든지 물어보세요!
        </p>
      </div>
    </div>
  )
}