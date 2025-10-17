import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { Toaster } from 'sonner'
import Providers from '@/components/providers'
import Header from '@/components/layout/header'
import Footer from '@/components/layout/footer'
import '../globals.css'

const inter = Inter({ subsets: ['latin', 'cyrillic'] })

export const metadata: Metadata = {
  title: 'Russian.Town - 러시아인을 위한 한국 커뮤니티',
  description: '한국 거주 러시아인과 교포를 위한 정보 공유 커뮤니티',
  keywords: ['러시아', '한국', '커뮤니티', '교포', '러시아인', 'Russian', 'Korea'],
}

export default async function LocaleLayout({
  children,
  params
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  // In Next.js 15+, params is a Promise
  const { locale } = params

  // Load messages for the current locale
  const messages = await getMessages({ locale })

  return (
    <html lang={locale}>
      <body className={inter.className}>
        <NextIntlClientProvider locale={locale} messages={messages}>
          <Providers>
            <div className="min-h-screen flex flex-col">
              <Header />
              <main className="flex-1">{children}</main>
              <Footer />
            </div>
            <Toaster richColors position="top-right" />
          </Providers>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
