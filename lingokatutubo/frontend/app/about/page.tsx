import { Navigation } from '@/components/navigation';
import { Heart, Book, Users, Lightbulb } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background via-white to-background">
      <Navigation />

      <main className="max-w-4xl mx-auto px-6 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-primary mb-4">About This Project</h1>
          <p className="text-xl text-foreground/70 max-w-2xl mx-auto">
            Preserving and revitalizing the Bagobo-Tagabawa language through innovative technology
          </p>
        </div>

        {/* Mission Section */}
        <section className="mb-16 p-8 bg-white border-2 border-primary/30 rounded-2xl">
          <h2 className="text-3xl font-bold text-primary mb-4 flex items-center gap-3">
            <Heart className="w-8 h-8" />
            Our Mission
          </h2>
          <p className="text-lg text-foreground/80 leading-relaxed mb-4">
            The Bagobo-Tagabawa Document Translator is dedicated to supporting the revitalization and preservation of the Bagobo-Tagabawa language. We believe that digital tools can play a crucial role in keeping indigenous languages alive by making translation accessible, accurate, and culturally sensitive.
          </p>
          <p className="text-lg text-foreground/80 leading-relaxed">
            This project bridges the gap between traditional knowledge and modern technology, enabling speakers and learners of Bagobo-Tagabawa to translate important documents while maintaining their cultural authenticity and linguistic integrity.
          </p>
        </section>

        {/* The Bagobo-Tagabawa */}
        <section className="mb-16 p-8 bg-white border-2 border-secondary/30 rounded-2xl">
          <h2 className="text-3xl font-bold text-secondary mb-4 flex items-center gap-3">
            <Book className="w-8 h-8" />
            About the Bagobo-Tagabawa People
          </h2>
          <p className="text-lg text-foreground/80 leading-relaxed mb-4">
            The Bagobo-Tagabawa are one of the major indigenous ethnic groups of Mindanao in the southern Philippines. Known for their rich cultural heritage, they are renowned for their exceptional artistry, particularly in:
          </p>
          <ul className="space-y-3 mb-4">
            <li className="flex gap-3 items-start">
              <span className="text-secondary font-bold">•</span>
              <span className="text-foreground/80"><strong>Inabal Weaving:</strong> Intricate geometric patterns created through traditional abaca ikat weaving techniques that have been passed down through generations.</span>
            </li>
            <li className="flex gap-3 items-start">
              <span className="text-secondary font-bold">•</span>
              <span className="text-foreground/80"><strong>Pangulabe (Beadwork):</strong> Elaborate beaded textiles and jewelry featuring vibrant colors and meaningful symbolic designs inspired by nature.</span>
            </li>
            <li className="flex gap-3 items-start">
              <span className="text-secondary font-bold">•</span>
              <span className="text-foreground/80"><strong>Nature-Inspired Art:</strong> Deep connection to natural elements reflected in their designs, from mythological creatures to sacred symbols.</span>
            </li>
          </ul>
          <p className="text-lg text-foreground/80 leading-relaxed">
            The Bagobo-Tagabawa language is a valuable part of the world&apos;s linguistic diversity, carrying centuries of cultural wisdom and traditions. Like many indigenous languages, it faces the challenge of limited speakers among younger generations—making digital preservation efforts essential.
          </p>
        </section>

        {/* Design Inspiration */}
        <section className="mb-16 p-8 bg-white border-2 border-accent/30 rounded-2xl">
          <h2 className="text-3xl font-bold text-accent mb-4 flex items-center gap-3">
            <Lightbulb className="w-8 h-8" />
            Design Heritage
          </h2>
          <p className="text-lg text-foreground/80 leading-relaxed mb-4">
            The visual design of this translator is inspired by the authentic artistic traditions of the Bagobo-Tagabawa people:
          </p>
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="p-4 bg-gradient-to-br from-primary/20 to-accent/20 rounded-lg">
              <p className="font-bold text-primary mb-2">Vibrant Color Palette</p>
              <p className="text-sm text-foreground/70">Rich, saturated colors reflecting the boldness of traditional textiles and beadwork.</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-secondary/20 to-accent/20 rounded-lg">
              <p className="font-bold text-secondary mb-2">Geometric Patterns</p>
              <p className="text-sm text-foreground/70">Intricate geometric designs inspired by Inabal weaving and traditional motifs.</p>
            </div>
            <div className="p-4 bg-gradient-to-br from-accent/20 to-primary/20 rounded-lg">
              <p className="font-bold text-accent mb-2">Nature Elements</p>
              <p className="text-sm text-foreground/70">Symbols and design elements drawn from the natural world that surrounds the Bagobo-Tagabawa homeland.</p>
            </div>
          </div>
        </section>

        {/* Technology Section */}
        <section className="mb-16 p-8 bg-white border-2 border-primary/30 rounded-2xl">
          <h2 className="text-3xl font-bold text-primary mb-4">How It Works</h2>
          <div className="space-y-6">
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center flex-shrink-0 text-white font-bold">
                1
              </div>
              <div>
                <h3 className="font-bold text-primary mb-2">Upload & Detect</h3>
                <p className="text-foreground/80">Your document is analyzed to determine its type and whether it&apos;s digital or scanned.</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-secondary to-accent flex items-center justify-center flex-shrink-0 text-white font-bold">
                2
              </div>
              <div>
                <h3 className="font-bold text-secondary mb-2">Extract & Preserve</h3>
                <p className="text-foreground/80">Text is carefully extracted while preserving layout, images, and formatting information.</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-accent to-primary flex items-center justify-center flex-shrink-0 text-white font-bold">
                3
              </div>
              <div>
                <h3 className="font-bold text-accent mb-2">Translate Intelligently</h3>
                <p className="text-foreground/80">Using our multilingual dataset, we translate while maintaining linguistic and cultural integrity.</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0 text-white font-bold">
                4
              </div>
              <div>
                <h3 className="font-bold text-primary mb-2">Reconstruct & Download</h3>
                <p className="text-foreground/80">A new PDF is created with translated text while keeping all original elements intact.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Community Section */}
        <section className="mb-16 p-8 bg-gradient-to-r from-primary/10 via-accent/10 to-secondary/10 border-2 border-primary/20 rounded-2xl">
          <h2 className="text-3xl font-bold text-primary mb-4 flex items-center gap-3">
            <Users className="w-8 h-8" />
            Community & Support
          </h2>
          <p className="text-lg text-foreground/80 leading-relaxed mb-6">
            This project is built with respect for and in collaboration with the Bagobo-Tagabawa community. We are committed to:
          </p>
          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-white rounded-lg border-l-4 border-primary">
              <p className="font-bold text-primary mb-2">Language Authenticity</p>
              <p className="text-sm text-foreground/70">Working with native speakers and linguistic experts to ensure accurate translation.</p>
            </div>
            <div className="p-4 bg-white rounded-lg border-l-4 border-secondary">
              <p className="font-bold text-secondary mb-2">Cultural Sensitivity</p>
              <p className="text-sm text-foreground/70">Respecting traditional knowledge and ensuring cultural context is preserved.</p>
            </div>
            <div className="p-4 bg-white rounded-lg border-l-4 border-accent">
              <p className="font-bold text-accent mb-2">Community Benefit</p>
              <p className="text-sm text-foreground/70">Creating tools that serve the community&apos;s needs and goals.</p>
            </div>
            <div className="p-4 bg-white rounded-lg border-l-4 border-primary">
              <p className="font-bold text-primary mb-2">Accessibility</p>
              <p className="text-sm text-foreground/70">Making translation tools easy to use for speakers of all backgrounds.</p>
            </div>
          </div>
        </section>

        {/* Vision Section */}
        <section className="p-8 bg-white border-2 border-secondary/30 rounded-2xl">
          <h2 className="text-3xl font-bold text-secondary mb-4">Our Vision</h2>
          <p className="text-lg text-foreground/80 leading-relaxed mb-4">
            We envision a future where technology serves as a bridge—not a replacement—for indigenous languages. By making translation accessible and preserving cultural authenticity, we hope to:
          </p>
          <ul className="space-y-2 text-foreground/80">
            <li className="flex gap-2 items-start">
              <span className="text-secondary font-bold">✓</span>
              <span>Support younger generations in learning and using Bagobo-Tagabawa</span>
            </li>
            <li className="flex gap-2 items-start">
              <span className="text-secondary font-bold">✓</span>
              <span>Create economic opportunities through document translation services</span>
            </li>
            <li className="flex gap-2 items-start">
              <span className="text-secondary font-bold">✓</span>
              <span>Preserve written records in the Bagobo-Tagabawa language</span>
            </li>
            <li className="flex gap-2 items-start">
              <span className="text-secondary font-bold">✓</span>
              <span>Inspire similar projects for other indigenous languages</span>
            </li>
          </ul>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-foreground/5 border-t-2 border-primary/20 mt-20 py-12">
        <div className="max-w-4xl mx-auto px-6 text-center text-foreground/60 text-sm">
          <p className="mb-2">
            Bagobo-Tagabawa Document Translator
          </p>
          <p>
            Preserving indigenous languages through technology and cultural respect
          </p>
        </div>
      </footer>
    </div>
  );
}
