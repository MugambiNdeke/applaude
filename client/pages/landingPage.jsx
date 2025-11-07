import React, { useState } from 'react';
import Button from '../components/ui/Button';
import { Mail, Zap, CheckCircle, Lock, DollarSign, XCircle } from 'lucide-react';

const LandingPage = () => {
    // State for the Contact Form
    const [contactForm, setContactForm] = useState({ name: '', email: '', message: '' });
    const [contactStatus, setContactStatus] = useState(null); // 'success' or 'error'

    const handleContactChange = (e) => {
        setContactForm({ ...contactForm, [e.target.name]: e.target.value });
    };

    const handleContactSubmit = async (e) => {
        e.preventDefault();
        setContactStatus(null);
        
        try {
            // Placeholder: Replace with actual Django API endpoint
            const response = await fetch('/api/v1/contact/submit/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(contactForm),
            });

            if (response.ok) {
                setContactStatus('success');
                setContactForm({ name: '', email: '', message: '' }); // Clear form
            } else {
                setContactStatus('error');
            }
        } catch (error) {
            console.error('Contact Form Error:', error);
            setContactStatus('error');
        }
    };

    const features = [
        { icon: Zap, title: "10-Minute Pull Request", description: "Go from broken code to a production-ready PR in minutes, not days[cite: 12].", citation: '12' },
        { icon: CheckCircle, title: "Closed-Loop QA", description: "The AI agent finds, fixes, verifies, and delivers—a true Level 5 autonomous system[cite: 7, 21].", citation: '7, 21' },
        { icon: Lock, title: "Code-First Security", description: "Your GitHub token is securely stored and used only for agent operations[cite: 98].", citation: '98' },
    ];
    
    const pricingTiers = [
        { name: "Weekly Sprint", price: "$15", runs: "20 Runs/mo", target: "Indie Devs", citation: '80' },
        { name: "Monthly Startup", price: "$47", runs: "50 Runs/mo", target: "Startups (Our Core)", citation: '80, 50' },
        { name: "Yearly Scale-Up", price: "$495", runs: "600 Runs/yr", target: "Mid-Market Teams", citation: '80, 55' },
    ];

    const faqs = [
        { q: "How secure is my code and GitHub token?", a: "Your code is cloned into a secure, sandboxed environment on Digital Ocean. Your GitHub token is securely stored in a PostgreSQL database and only used by the Celery worker for cloning and creating PRs[cite: 87, 98, 124]." },
        { q: "What is a 'Level 5' Autonomous Agent?", a: "A Level 5 agent doesn't just find a bug; it actively fixes it, verifies the fix by re-running the test, and submits a final pull request—a complete, autonomous remediation loop[cite: 4, 21]." },
        { q: "What technologies do you support?", a: "We focus on a 'Zero Bug' launch, starting with expert support for React (Vite) + Django (DRF) + PostgreSQL, with plans to quickly expand to Next.js and FastAPI[cite: 152, 156]." },
        { q: "How is the pricing so efficient?", a: "Our model is built on 'damn good margins' by using Anthropic's Claude 4.0 efficiently as a planner/fixer, minimizing variable token costs per run[cite: 57, 61, 75]." },
        { q: "Can I manage my subscription and runs?", a: "Yes, your main dashboard tracks your `runs_remaining` and allows you to upgrade or manage your plan directly." },
    ];

    const FeatureCard = ({ icon: Icon, title, description, citation }) => (
        <div className="flex flex-col space-y-3 p-6 bg-soft-white/5 rounded-xl border border-soft-white/10 transition-transform hover:scale-[1.01] duration-300">
            <Icon className="w-8 h-8 text-electric-gold" strokeWidth={1.5} />
            <h3 className="text-xl font-bold text-soft-white">{title}</h3>
            <p className="text-soft-white/70 text-sm leading-relaxed">{description}</p>
        </div>
    );

    const PricingCard = ({ name, price, runs, target, citation }) => (
        <div className="flex flex-col p-8 bg-soft-white/5 rounded-xl border-t-4 border-electric-gold/50 shadow-lg hover:shadow-gold-glow/50 transition-all duration-300 space-y-6">
            <div className="flex justify-between items-center">
                <h3 className="text-2xl font-bold text-electric-gold">{name}</h3>
                <p className="text-sm font-medium text-soft-white/50">{target}</p>
            </div>
            <p className="text-5xl font-extrabold text-soft-white leading-none">{price}<span className="text-base font-normal text-soft-white/50">/ mo</span></p>
            <p className="text-lg text-soft-white/80 border-b border-soft-white/10 pb-4">{runs} Included</p>
            <Button variant="primary" className="w-full text-lg">Get Started</Button>
        </div>
    );

    const FAQItem = ({ q, a }) => {
        const [isOpen, setIsOpen] = useState(false);
        return (
            <div className="border-b border-soft-white/10 last:border-b-0">
                <button
                    className="flex justify-between items-center w-full py-4 text-left text-soft-white hover:text-electric-gold transition-colors"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    <span className="font-semibold">{q}</span>
                    {isOpen ? <XCircle className="w-5 h-5" /> : <DollarSign className="w-5 h-5" />}
                </button>
                {isOpen && (
                    <p className="pb-4 text-soft-white/70 leading-relaxed transition-all duration-500 ease-in-out">
                        {a}
                    </p>
                )}
            </div>
        );
    };


    return (
        <div className="min-h-screen bg-luxury-black font-poppins text-soft-white">
            <header className="max-w-7xl mx-auto py-6 px-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-electric-gold tracking-widest">APPLAUDE</h1>
                <Button variant="secondary" onClick={() => window.location.href='/dashboard'}>Sign In</Button>
            </header>

            <main>
                {/* 1. Hero Section */}
                <section className="max-w-4xl mx-auto text-center py-20 px-4 md:py-32 space-y-6">
                    <h2 className="text-6xl md:text-8xl font-extrabold leading-tight text-soft-white">
                        Autonomous Remediation. <span className="text-electric-gold">Level 5 QA.</span>
                    </h2>
                    <p className="text-xl md:text-2xl text-soft-white/70 max-w-3xl mx-auto">
                        Our core value proposition is not "find bugs faster," it is **"go from broken code to pull request in 10 minutes."** [cite: 12]
                    </p>
                    <div className="pt-8">
                        <Button variant="primary" className="px-10 py-3 text-lg mr-4">Start Free Trial</Button>
                        <Button variant="secondary" className="px-10 py-3 text-lg">See How It Works</Button>
                    </div>
                </section>
                
                {/* 2. Feature Grid */}
                <section className="max-w-7xl mx-auto py-16 px-4">
                    <div className="grid md:grid-cols-3 gap-8">
                        {features.map((f, i) => <FeatureCard key={i} {...f} />)}
                    </div>
                </section>

                {/* 3. Demo Video Placeholder */}
                <section className="max-w-7xl mx-auto py-20 px-4">
                    <h2 className="text-4xl font-bold text-center mb-12 text-soft-white">See Applaude In Action</h2>
                    <div className="aspect-video bg-soft-white/5 border border-electric-gold/30 rounded-xl flex items-center justify-center p-12">
                        <p className="text-xl text-soft-white/50">
                            [Demo Video Component Placeholder] - Coming Soon
                        </p>
                    </div>
                </section>

                {/* 4. Pricing Tiers */}
                <section className="max-w-7xl mx-auto py-20 px-4">
                    <h2 className="text-4xl font-bold text-center mb-16 text-soft-white">Pricing Built for Growth</h2>
                    <div className="grid md:grid-cols-3 gap-8">
                        {pricingTiers.map((p, i) => <PricingCard key={i} {...p} />)}
                    </div>
                </section>

                {/* 5. FAQ Section */}
                <section className="max-w-4xl mx-auto py-20 px-4">
                    <h2 className="text-4xl font-bold text-center mb-12 text-soft-white">Frequently Asked Questions</h2>
                    <div className="bg-soft-white/5 p-6 rounded-xl border border-soft-white/10">
                        {faqs.map((faq, i) => <FAQItem key={i} {...faq} />)}
                    </div>
                </section>

                {/* 6. Contact Form */}
                <section className="max-w-xl mx-auto py-20 px-4">
                    <h2 className="text-4xl font-bold text-center mb-10 text-soft-white">Get In Touch</h2>
                    <form onSubmit={handleContactSubmit} className="space-y-6 bg-soft-white/5 p-8 rounded-xl border border-soft-white/10">
                        <div>
                            <label htmlFor="name" className="block text-sm font-medium text-soft-white/80 mb-2">Name</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={contactForm.name}
                                onChange={handleContactChange}
                                className="w-full p-3 bg-luxury-black border border-soft-white/20 rounded-lg text-soft-white focus:ring-electric-gold focus:border-electric-gold transition-colors"
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-soft-white/80 mb-2">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={contactForm.email}
                                onChange={handleContactChange}
                                className="w-full p-3 bg-luxury-black border border-soft-white/20 rounded-lg text-soft-white focus:ring-electric-gold focus:border-electric-gold transition-colors"
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="message" className="block text-sm font-medium text-soft-white/80 mb-2">Message</label>
                            <textarea
                                id="message"
                                name="message"
                                rows="4"
                                value={contactForm.message}
                                onChange={handleContactChange}
                                className="w-full p-3 bg-luxury-black border border-soft-white/20 rounded-lg text-soft-white focus:ring-electric-gold focus:border-electric-gold transition-colors"
                                required
                            ></textarea>
                        </div>
                        {contactStatus === 'success' && (
                            <p className="text-green-400 flex items-center"><CheckCircle className="w-5 h-5 mr-2" /> Thank you! Your message has been received.</p>
                        )}
                        {contactStatus === 'error' && (
                            <p className="text-red-400 flex items-center"><XCircle className="w-5 h-5 mr-2" /> Failed to send message. Please try again.</p>
                        )}
                        <Button type="submit" variant="primary" className="w-full text-lg">
                            <Mail className="w-5 h-5 mr-2" strokeWidth={1.5} /> Send Message
                        </Button>
                    </form>
                </section>
            </main>

            <footer className="max-w-7xl mx-auto py-10 px-4 border-t border-soft-white/10 text-center text-soft-white/50">
                &copy; {new Date().getFullYear()} Applaude. Autonomous Remediation.
            </footer>
        </div>
    );
};

export default LandingPage;
