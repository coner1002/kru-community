import { useTranslations } from 'next-intl'
import LanguageSwitcher from './language-switcher'

export default function Header() {
  const t = useTranslations('Navigation')

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-3">
            {/* 러시아 국기 */}
            <span
              className="inline-block w-8 h-6 rounded"
              style={{
                backgroundImage: 'url(\'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5IDYiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoOXY2SDB6Ii8+PHBhdGggZmlsbD0iIzAwMzlhNiIgZD0iTTAgMmg5djRIMHoiLz48cGF0aCBmaWxsPSIjZDUyYjFlIiBkPSJNMCA0aDl2MkgweiIvPjwvc3ZnPg==\')',
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
              title="Русский флаг"
            />
            <h1 className="text-xl font-bold text-blue-600">
              Russian.Town
            </h1>
          </div>

          <nav className="hidden md:flex space-x-8">
            <a href="/" className="text-gray-900 hover:text-blue-600">
              {t('home')}
            </a>
            <a href="/community" className="text-gray-900 hover:text-blue-600">
              {t('community')}
            </a>
            <a href="/partners" className="text-gray-900 hover:text-blue-600">
              {t('partners')}
            </a>
          </nav>

          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
              {t('login')}
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}