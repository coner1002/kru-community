import { useTranslations } from 'next-intl'

export default function PartnerDirectory() {
  const t = useTranslations('HomePage')

  const partners = [
    {
      id: 1,
      name: '러시아 부동산 컨설팅',
      category: '부동산',
      description: '서울 강남구 전문 부동산, 러시아어 상담 가능',
      rating: 4.8,
      reviews: 156
    },
    {
      id: 2,
      name: '모스크바 클리닉',
      category: '병원',
      description: '러시아어 진료 가능한 종합병원',
      rating: 4.9,
      reviews: 89
    },
    {
      id: 3,
      name: '한러 번역 서비스',
      category: '번역',
      description: '공문서 번역 전문, 신속 정확한 서비스',
      rating: 4.7,
      reviews: 234
    }
  ]

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {partners.map((partner) => (
          <div key={partner.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div className="mb-4">
              <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mb-2">
                {partner.category}
              </span>
              <h3 className="text-lg font-semibold">
                {partner.name}
              </h3>
            </div>

            <p className="text-gray-600 mb-4">
              {partner.description}
            </p>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-yellow-400">★</span>
                <span className="font-medium">{partner.rating}</span>
                <span className="text-gray-500 text-sm">({partner.reviews})</span>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                상세보기
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center">
        <button className="border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-lg hover:bg-blue-600 hover:text-white transition">
          전체 파트너 보기
        </button>
      </div>
    </div>
  )
}