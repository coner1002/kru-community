'use client'

import { useEffect, useState } from 'react'
import { useTranslations, useLocale } from 'next-intl'
import Link from 'next/link'
import { getCategories, type Category } from '@/lib/api/categories'

export default function Categories() {
  const t = useTranslations('Categories')
  const locale = useLocale()
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchCategories() {
      try {
        const data = await getCategories()
        // 부모 카테고리만 필터링 (parent_id가 null인 것들)
        const mainCategories = data.filter(cat => !cat.parent_id)
        setCategories(mainCategories)
      } catch (err) {
        console.error('카테고리 로딩 실패:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchCategories()
  }, [])

  // 카테고리별 색상 매핑
  const getCategoryColor = (index: number) => {
    const colors = [
      'bg-green-500',
      'bg-blue-500',
      'bg-purple-500',
      'bg-yellow-500',
      'bg-red-500',
      'bg-indigo-500',
      'bg-pink-500',
      'bg-orange-500'
    ]
    return colors[index % colors.length]
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-500">{locale === 'ru' ? 'Загрузка...' : '로딩 중...'}</div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {categories.map((category, index) => (
        <Link key={category.id} href={`/${locale}/boards/${category.slug}`}>
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition cursor-pointer">
            <div className={`w-12 h-12 ${getCategoryColor(index)} rounded-lg flex items-center justify-center text-white text-2xl mb-4`}>
              {category.icon || '📋'}
            </div>
            <h3 className="text-lg font-semibold mb-2">
              {locale === 'ru' ? category.name_ru : category.name_ko}
            </h3>
            <p className="text-gray-600 text-sm">
              {locale === 'ru'
                ? (category.description_ru || 'Различная информация')
                : (category.description_ko || '다양한 정보를 찾아보세요')
              }
            </p>
          </div>
        </Link>
      ))}
    </div>
  )
}
