'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

export function Navigation() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full bg-white/95 backdrop-blur-sm border-b-2 border-primary shadow-sm">
      <nav className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 bg-gradient-to-br from-primary via-accent to-secondary rounded-lg flex items-center justify-center shadow-lg">
            <span className="text-white font-bold text-lg">ᴮᵀ</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-primary leading-tight">Bagobo</h1>
            <p className="text-xs text-secondary font-semibold">Translator</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <div className="flex items-center gap-8">
          <Link
            href="/"
            className={cn(
              'text-sm font-semibold transition-all duration-200 relative',
              pathname === '/'
                ? 'text-primary'
                : 'text-foreground/70 hover:text-primary'
            )}
          >
            HOME
            {pathname === '/' && (
              <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gradient-to-r from-accent to-secondary rounded-full"></div>
            )}
          </Link>

          <Link
            href="/translate"
            className={cn(
              'text-sm font-semibold transition-all duration-200 relative',
              pathname === '/translate'
                ? 'text-primary'
                : 'text-foreground/70 hover:text-primary'
            )}
          >
            TRANSLATE
            {pathname === '/translate' && (
              <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gradient-to-r from-accent to-secondary rounded-full"></div>
            )}
          </Link>

          <Link
            href="/about"
            className={cn(
              'text-sm font-semibold transition-all duration-200 relative',
              pathname === '/about'
                ? 'text-primary'
                : 'text-foreground/70 hover:text-primary'
            )}
          >
            ABOUT
            {pathname === '/about' && (
              <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gradient-to-r from-accent to-secondary rounded-full"></div>
            )}
          </Link>
        </div>
      </nav>
    </header>
  );
}
