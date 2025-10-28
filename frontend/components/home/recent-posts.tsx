'use client'

import { useEffect, useState } from 'react'
import { useTranslations, useLocale } from 'next-intl'
import Link from 'next/link'
import { getPosts, type PostResponse } from '@/lib/api/posts'
import { getCategories, type Category } from '@/lib/api/categories'

export default function RecentPosts() {
  const t = useTranslations('HomePage')
  const locale = useLocale()
  const [posts, setPosts] = useState<PostResponse[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)

        // 카테고리와 최근 게시글 동시 로딩
        const [categoriesData, postsData] = await Promise.all([
          getCategories(),
          getPosts({ page: 1, page_size: 6 })
        ])

        setCategories(categoriesData)
        setPosts(postsData.items)
        setError(null)
      } catch (err) {
        console.error('데이터 로딩 실패:', err)
        setError('게시글을 불러오는데 실패했습니다.')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // 카테고리 ID로 카테고리 이름 찾기
  const getCategoryName = (categoryId: number) => {
    const category = categories.find(c => c.id === categoryId)
    if (!category) return ''
    return locale === 'ru' ? category.name_ru : category.name_ko
  }

  // 게시글 제목 가져오기 (번역 우선)
  const getPostTitle = (post: PostResponse) => {
    if (locale === 'ru') {
      return post.translated_title_ru || post.title
    }
    return post.translated_title_ko || post.title
  }

  // 게시글 요약 가져오기 (번역 우선)
  const getPostSummary = (post: PostResponse) => {
    if (locale === 'ru') {
      return post.translated_summary_ru || post.summary
    }
    return post.translated_summary_ko || post.summary
  }

  // 날짜 포맷팅
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString(locale === 'ru' ? 'ru-RU' : 'ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-500">{locale === 'ru' ? 'Загрузка...' : '로딩 중...'}</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-red-500">{error}</div>
      </div>
    )
  }

  if (posts.length === 0) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-500">{locale === 'ru' ? 'Нет записей' : '게시글이 없습니다'}</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <div key={post.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <Link href={`/${locale}/posts/${post.id}`}>
                <h3 className="text-xl font-semibold mb-2 hover:text-blue-600 cursor-pointer">
                  {getPostTitle(post)}
                </h3>
              </Link>
              {getPostSummary(post) && (
                <p className="text-gray-600 mb-3">
                  {getPostSummary(post)}
                </p>
              )}
              <div className="flex items-center text-sm text-gray-500 space-x-4">
                <span>{formatDate(post.created_at)}</span>
                {getCategoryName(post.category_id) && (
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    {getCategoryName(post.category_id)}
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t">
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>👁 {post.view_count}</span>
              <span>👍 {post.like_count}</span>
              <span>💬 {post.comment_count}</span>
            </div>
            <Link href={`/${locale}/posts/${post.id}`}>
              <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                {locale === 'ru' ? 'Подробнее →' : '자세히 보기 →'}
              </button>
            </Link>
          </div>
        </div>
      ))}

      <div className="text-center">
        <Link href={`/${locale}/posts`}>
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
            {locale === 'ru' ? 'Больше записей' : '더 많은 게시글 보기'}
          </button>
        </Link>
      </div>
    </div>
  )
}
