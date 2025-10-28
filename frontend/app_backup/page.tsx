import { useTranslations } from 'next-intl'
import Hero from '@/components/home/hero'
import Categories from '@/components/home/categories'
import RecentPosts from '@/components/home/recent-posts'
import PartnerDirectory from '@/components/home/partner-directory'
import CommunityStats from '@/components/home/community-stats'

export default function HomePage() {
  const t = useTranslations('HomePage')

  return (
    <div className="flex flex-col">
      <Hero />

      <section className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold mb-8 text-center">
          {t('sections.categories')}
        </h2>
        <Categories />
      </section>

      <section className="bg-gray-50 py-12">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8 text-center">
            {t('sections.recentPosts')}
          </h2>
          <RecentPosts />
        </div>
      </section>

      <section className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold mb-8 text-center">
          {t('sections.partners')}
        </h2>
        <PartnerDirectory />
      </section>

      <section className="bg-blue-50 py-12">
        <div className="container mx-auto px-4">
          <CommunityStats />
        </div>
      </section>
    </div>
  )
}