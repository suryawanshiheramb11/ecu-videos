"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Moon, Sun, Play, Terminal, Check, X,
  Video, Code2, Sparkles, GraduationCap,
  ArrowRight, Github, Twitter, Linkedin
} from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { signIn, useSession } from "next-auth/react";

// --- Utility ---
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// --- Components ---

const Navbar = ({ darkMode, toggleTheme, onSignIn }: { darkMode: boolean; toggleTheme: () => void; onSignIn: () => void }) => (
  <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-white/70 dark:bg-slate-900/70 border-b border-slate-200 dark:border-slate-800 transition-colors duration-300">
    <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold">
          OS
        </div>
        <span className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">OnlyStudies</span>
      </div>

      <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600 dark:text-slate-300">
        <a href="#features" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">Features</a>
        <a href="#showcase" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">Showcase</a>
        <a href="#pricing" className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">Pricing</a>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-600 dark:text-slate-300"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
        <button
          onClick={onSignIn}
          className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm transition-transform hover:scale-105 active:scale-95"
        >
          Sign In
        </button>
      </div>
    </div>
  </nav>
);

const Hero = ({ onStart, darkMode }: { onStart: () => void; darkMode: boolean }) => {
  const { data: session } = useSession();

  return (
    <section className="relative pt-32 pb-20 px-6 overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-40 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Text Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-xs font-semibold mb-6">
            <Sparkles size={12} />
            <span>v2.0 Now Available</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-slate-900 dark:text-white leading-tight mb-6">
            Turn Text into <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400">
              Perfect Math Lessons
            </span>
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-300 mb-8 max-w-lg leading-relaxed">
            Generate professional Python Manim animations with AI voiceovers in seconds.
            Just type your topic, and let our AI do the teaching.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            {session ? (
              <a
                href={`http://localhost:8501?theme=${darkMode ? 'dark' : 'light'}&user=${session.user?.name}`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg shadow-lg shadow-indigo-500/25 transition-all hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
              >
                Go to App <ArrowRight size={20} />
              </a>
            ) : (
              <button
                onClick={onStart}
                className="px-8 py-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg shadow-lg shadow-indigo-500/25 transition-all hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
              >
                Start Creating for Free <ArrowRight size={20} />
              </button>
            )}
            <a
              href={`http://localhost:8501?theme=${darkMode ? 'dark' : 'light'}`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 font-bold text-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-all hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
            >
              <Play size={20} className="fill-current" /> Try Demo
            </a>
          </div>
        </motion.div>

        {/* Visual Content */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="relative"
        >
          <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-slate-200 dark:border-slate-700 bg-slate-900">
            {/* Mock Window Header */}
            <div className="flex items-center gap-2 px-4 py-3 bg-slate-800/50 border-b border-slate-700">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
              </div>
              <div className="ml-4 text-xs text-slate-400 font-mono">generator.py</div>
            </div>

            {/* Mock Content */}
            <div className="grid grid-cols-2 h-[400px]">
              {/* Code Side */}
              <div className="p-6 font-mono text-sm text-slate-300 border-r border-slate-800 bg-slate-900/50">
                <div className="flex gap-2 text-indigo-400 mb-2">
                  <Terminal size={16} />
                  <span>Prompt Input</span>
                </div>
                <p className="typing-effect text-slate-100">
                  "Visualize the Pythagorean Theorem with squares on each side..."
                </p>
                <div className="mt-4 space-y-2 opacity-50">
                  <div className="h-2 w-3/4 bg-slate-700 rounded" />
                  <div className="h-2 w-1/2 bg-slate-700 rounded" />
                  <div className="h-2 w-5/6 bg-slate-700 rounded" />
                </div>
              </div>

              {/* Preview Side */}
              <div className="relative bg-slate-950 flex items-center justify-center overflow-hidden">
                <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:24px_24px]" />
                <motion.div
                  animate={{
                    rotate: 360,
                    scale: [1, 1.2, 1],
                  }}
                  transition={{
                    duration: 10,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                  className="relative z-10"
                >
                  <div className="w-32 h-32 border-4 border-indigo-500 rounded-lg relative">
                    <div className="absolute -top-16 -left-16 w-32 h-32 border-4 border-purple-500 rounded-lg opacity-50" />
                    <div className="absolute -bottom-16 -right-16 w-32 h-32 border-4 border-pink-500 rounded-lg opacity-50" />
                  </div>
                </motion.div>

                {/* Floating UI Elements */}
                <div className="absolute bottom-4 left-4 right-4 bg-slate-900/90 backdrop-blur p-3 rounded-lg border border-slate-700">
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-indigo-500"
                      animate={{ width: ["0%", "100%"] }}
                      transition={{ duration: 3, repeat: Infinity }}
                    />
                  </div>
                  <div className="flex justify-between mt-2 text-xs text-slate-400">
                    <span>Rendering...</span>
                    <span>1080p</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

const Pricing = () => {
  const [isYearly, setIsYearly] = useState(false);

  const plans = [
    {
      name: "Student",
      price: 0,
      features: ["720p Rendering", "Watermarked Videos", "Standard Speed", "Community Support"],
      cta: "Start Free",
      popular: false
    },
    {
      name: "Tutor",
      price: isYearly ? 399 : 499,
      features: ["1080p Rendering", "No Watermark", "Priority Rendering", "Commercial License"],
      cta: "Get Pro",
      popular: true
    },
    {
      name: "Institute",
      price: isYearly ? 1599 : 1999,
      features: ["4K Rendering", "Custom Branding", "API Access", "Dedicated Support"],
      cta: "Contact Sales",
      popular: false
    }
  ];

  return (
    <section id="pricing" className="py-20 px-6 bg-slate-50 dark:bg-slate-900/50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mb-8">
            Choose the plan that fits your teaching needs.
          </p>

          <div className="flex items-center justify-center gap-4">
            <span className={cn("text-sm font-medium", !isYearly ? "text-slate-900 dark:text-white" : "text-slate-500")}>Monthly</span>
            <button
              onClick={() => setIsYearly(!isYearly)}
              className="w-12 h-6 rounded-full bg-indigo-600 p-1 transition-colors relative"
            >
              <motion.div
                animate={{ x: isYearly ? 24 : 0 }}
                className="w-4 h-4 rounded-full bg-white shadow-sm"
              />
            </button>
            <span className={cn("text-sm font-medium", isYearly ? "text-slate-900 dark:text-white" : "text-slate-500")}>
              Yearly <span className="text-indigo-600 text-xs">(Save 20%)</span>
            </span>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              viewport={{ once: true }}
              className={cn(
                "relative p-8 rounded-2xl border transition-all duration-300 hover:scale-105",
                plan.popular
                  ? "bg-white dark:bg-slate-800 border-indigo-500 shadow-xl shadow-indigo-500/10"
                  : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
              )}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-indigo-600 text-white text-xs font-bold rounded-full">
                  MOST POPULAR
                </div>
              )}
              <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-4xl font-extrabold text-slate-900 dark:text-white">₹{plan.price}</span>
                <span className="text-slate-500">/mo</span>
              </div>
              <ul className="space-y-4 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-300">
                    <Check size={16} className="text-indigo-500" />
                    {feature}
                  </li>
                ))}
              </ul>
              <button className={cn(
                "w-full py-3 rounded-xl font-bold transition-colors",
                plan.popular
                  ? "bg-indigo-600 hover:bg-indigo-700 text-white"
                  : "bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-900 dark:text-white"
              )}>
                {plan.cta}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};



const AuthModal = ({ isOpen, onClose, darkMode }: { isOpen: boolean; onClose: () => void; darkMode: boolean }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleGoogleSignIn = async () => {
    setIsLoading(true);
    await signIn("google", { callbackUrl: "http://localhost:3000" });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-white dark:bg-slate-900 rounded-2xl shadow-2xl z-50 p-8 border border-slate-200 dark:border-slate-700"
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
            >
              <X size={20} />
            </button>

            <div className="text-center mb-8">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 rounded-xl flex items-center justify-center mx-auto mb-4">
                <GraduationCap size={24} />
              </div>
              <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Welcome Back</h2>
              <p className="text-slate-600 dark:text-slate-400">Sign in to continue creating</p>
            </div>

            <div className="space-y-4">
              <button
                onClick={handleGoogleSignIn}
                disabled={isLoading}
                className="w-full py-3 px-4 rounded-xl border border-slate-200 dark:border-slate-700 flex items-center justify-center gap-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors text-slate-700 dark:text-slate-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-slate-400 border-t-indigo-600 rounded-full animate-spin" />
                ) : (
                  <svg className="w-5 h-5" viewBox="0 0 24 24">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                    <path d="M5.84 14.17c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.54z" fill="#FBBC05" />
                    <path d="M12 4.6c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 1.09 14.97 0 12 0 7.7 0 3.99 2.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                  </svg>
                )}
                {isLoading ? "Signing in..." : "Continue with Google"}
              </button>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-slate-200 dark:border-slate-700" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white dark:bg-slate-900 px-2 text-slate-500">Or continue with email</span>
                </div>
              </div>

              <input
                type="email"
                placeholder="Email address"
                className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 dark:text-white"
              />
              <input
                type="password"
                placeholder="Password"
                className="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 dark:text-white"
              />
              <button className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition-colors">
                Sign In
              </button>
            </div>

            <div className="mt-6 text-center">
              <a
                href={`http://localhost:8501?theme=${darkMode ? 'dark' : 'light'}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
              >
                Just browsing? Continue as Guest
              </a>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

const Footer = () => (
  <footer className="bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 py-12 px-6">
    <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-indigo-600 rounded flex items-center justify-center text-white text-xs font-bold">
          OS
        </div>
        <span className="font-bold text-slate-900 dark:text-white">OnlyStudies</span>
      </div>

      <div className="text-sm text-slate-500">
        © 2025 OnlyStudies. All rights reserved.
      </div>

      <div className="flex gap-4 text-slate-400">
        <Github size={20} className="hover:text-slate-900 dark:hover:text-white cursor-pointer transition-colors" />
        <Twitter size={20} className="hover:text-slate-900 dark:hover:text-white cursor-pointer transition-colors" />
        <Linkedin size={20} className="hover:text-slate-900 dark:hover:text-white cursor-pointer transition-colors" />
      </div>
    </div>
  </footer>
);

export default function Home() {
  const [darkMode, setDarkMode] = useState(true);
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div className={cn("min-h-screen bg-white dark:bg-slate-950 transition-colors duration-300 font-sans selection:bg-indigo-500/30")}>
      <Navbar
        darkMode={darkMode}
        toggleTheme={() => setDarkMode(!darkMode)}
        onSignIn={() => setIsAuthOpen(true)}
      />

      <main>
        <Hero onStart={() => setIsAuthOpen(true)} darkMode={darkMode} />
        <Pricing />
      </main>

      <Footer />

      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        darkMode={darkMode}
      />
    </div>
  );
}
