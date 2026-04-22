import Link from 'next/link';
import { Navigation } from '@/components/navigation';
import { ArrowRight, FileText, Zap, Globe } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-white to-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative max-w-7xl mx-auto px-6 py-20 flex flex-col lg:flex-row items-center gap-12">
        {/* Content */}
        <div className="flex-1">
          <div className="inline-block mb-4 px-4 py-2 bg-accent/20 border border-accent rounded-full">
            <span className="text-sm font-semibold text-accent">Preserving Indigenous Language</span>
          </div>

          <h1 className="text-5xl lg:text-6xl font-bold leading-tight mb-6 text-balance">
            <span className="text-primary">Bagobo-Tagabawa</span> Document Translation
          </h1>

          <p className="text-lg text-foreground/70 mb-8 max-w-xl leading-relaxed">
            Transform your documents into the Bagobo-Tagabawa language while preserving layout, images, and cultural integrity. Support indigenous language revitalization.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 mb-12">
            <Link
              href="/translate"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-primary to-secondary text-white font-semibold rounded-lg hover:shadow-xl hover:scale-105 transition-all duration-200 group"
            >
              Start Translating
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/about"
              className="inline-flex items-center justify-center px-8 py-4 border-2 border-primary text-primary font-semibold rounded-lg hover:bg-primary/5 transition-all duration-200"
            >
              Learn More
            </Link>
          </div>

          <div className="flex items-center gap-6 text-sm text-foreground/70">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-accent/30 flex items-center justify-center">
                <span className="text-primary font-bold">✓</span>
              </div>
              <span>PDF, DOCX, Images</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-accent/30 flex items-center justify-center">
                <span className="text-primary font-bold">✓</span>
              </div>
              <span>Layout Preserved</span>
            </div>
          </div>
        </div>

        {/* Visual Element */}
        <div className="flex-1 relative h-96 lg:h-[500px]">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-accent/20 to-secondary/20 rounded-2xl blur-3xl"></div>
          
          {/* Geometric pattern inspired by Inabal weaving */}
          <div className="absolute inset-8 border-4 border-primary/40 rounded-xl">
            <div className="absolute top-12 left-12 w-24 h-24 border-4 border-accent/60 rounded-lg transform rotate-45"></div>
            <div className="absolute bottom-20 right-16 w-32 h-32 border-4 border-secondary/50 rounded-lg transform -rotate-12"></div>
            <div className="absolute top-1/2 right-1/4 w-20 h-20 border-4 border-primary/50 rounded-full"></div>
          </div>

          {/* Center element */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-32 h-32 bg-gradient-to-br from-primary via-accent to-secondary rounded-2xl shadow-2xl flex items-center justify-center transform hover:scale-110 transition-transform duration-300">
              <FileText className="w-16 h-16 text-white" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white/50 py-20 border-t-2 border-b-2 border-accent/30">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-4 text-primary">
            Powerful Translation Features
          </h2>
          <p className="text-center text-foreground/70 mb-16 max-w-2xl mx-auto">
            Advanced document processing tailored for low-resource languages
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="p-8 bg-white border-2 border-primary/30 rounded-xl hover:shadow-xl transition-shadow duration-300 group">
              <div className="w-14 h-14 bg-gradient-to-br from-primary to-accent rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <FileText className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold text-primary mb-3">Multiple Formats</h3>
              <p className="text-foreground/70">
                Support for PDF, DOCX, JPG, and PNG. Digital or scanned documents—we handle them all.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="p-8 bg-white border-2 border-secondary/30 rounded-xl hover:shadow-xl transition-shadow duration-300 group">
              <div className="w-14 h-14 bg-gradient-to-br from-secondary to-accent rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold text-secondary mb-3">Layout Preservation</h3>
              <p className="text-foreground/70">
                Images, formatting, and structure stay intact. Only text is translated.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="p-8 bg-white border-2 border-accent/30 rounded-xl hover:shadow-xl transition-shadow duration-300 group">
              <div className="w-14 h-14 bg-gradient-to-br from-accent to-primary rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Globe className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold text-accent mb-3">Language Preservation</h3>
              <p className="text-foreground/70">
                Supporting Bagobo-Tagabawa revitalization through accessible translation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="bg-gradient-to-r from-primary via-accent to-secondary rounded-2xl p-12 text-center text-white shadow-2xl">
          <h2 className="text-4xl font-bold mb-4">Ready to Translate?</h2>
          <p className="text-lg mb-8 opacity-95">
            Join us in preserving the Bagobo-Tagabawa language. Start translating your documents today.
          </p>
          <Link
            href="/translate"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-primary font-bold rounded-lg hover:bg-white/90 transition-all duration-200 group"
          >
            Open Translator
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-foreground/5 border-t-2 border-primary/20 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-foreground/60 text-sm">
          <p>Supporting indigenous language revitalization and digital preservation</p>
        </div>
      </footer>
    </div>
  );
}
