"use client";
import AnimatedBeamComp from "@/components/hero-comp";
import { DotPattern } from "@/components/ui/dot-pattern";
import { RainbowButton } from "@/components/ui/rainbow-button";

import { cn } from "@/lib/utils";

export default function Home() {
  return (
    <div className="relative min-h-screen bg-white text-gray-800 flex flex-col overflow-hidden">
      
      {/* Hero Section with Dot Pattern */}
      <section className="relative flex flex-col justify-center items-center min-h-screen">
      <div
        className="absolute w-[50rem] h-[50rem] rounded-full"
        style={{
          background: "radial-gradient(circle, rgba(173, 216, 230, 1), rgba(173, 216, 230, 0) 50%)",
          top: "0",
          left: "0",
          transform: "translate(-25%, -40%)",
        }}
      ></div>
      <div
        className="absolute w-[50rem] h-[50rem] rounded-full"
        style={{
          background: "radial-gradient(circle, rgba(173, 216, 230, 1), rgba(173, 216, 230, 0) 50%)",
          bottom: "0",
          right: "0",
          transform: "translate(25%,40%)",
        }}
      ></div>
        {/* Dot Pattern */}
        <DotPattern
          className={cn(
            "absolute inset-0 [mask-image:radial-gradient(600px_circle_at_center,white,transparent)] z-0"
          )}
        />

        {/* Header Section */}
        <div className="text-center mt-24 z-10">
          <h1 className="text-5xl font-bold text-[#226f54] mb-4">
            welcome to verdora
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            Upload an image of your waste, let Verdora classify it, and connect with people who can reuse, recycle, or compost it.
          </p>
        </div>

        <RainbowButton
          onClick={() => {
            window.location.href = "/classify";
          }}
        >
          Get Started
        </RainbowButton>

        {/* Animated Beam */}
        <AnimatedBeamComp />
      </section>

      {/* Features Section */}
      <section className="w-full py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-[#226f54] mb-10">
            Features You'll Love
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 bg-gray-100 shadow-md rounded-lg">
              <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
                Seamless Integration
              </h3>
              <p className="text-gray-600">
                Easily connect Verdora to your favorite apps and tools to create
                a unified workflow.
              </p>
            </div>
            <div className="p-6 bg-gray-100 shadow-md rounded-lg">
              <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
                Time-Saving Automation
              </h3>
              <p className="text-gray-600">
                Automate repetitive tasks and focus on what matters most with
                our intelligent solutions.
              </p>
            </div>
            <div className="p-6 bg-gray-100 shadow-md rounded-lg">
              <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
                Enhanced Productivity
              </h3>
              <p className="text-gray-600">
                Get more done in less time with Verdora's productivity-enhancing
                features.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="w-full py-16 bg-gray-50">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-[#226f54] mb-10">
            Frequently Asked Questions
          </h2>
          <div className="space-y-8 max-w-4xl mx-auto">
            <div className="text-left">
              <h3 className="text-xl font-semibold text-[#226f54] mb-2">
                What is Verdora?
              </h3>
              <p className="text-gray-600">
                Verdora is a platform that helps you automate workflows and
                integrate tools to streamline your productivity.
              </p>
            </div>
            <div className="text-left">
              <h3 className="text-xl font-semibold text-[#226f54] mb-2">
                Is Verdora free to use?
              </h3>
              <p className="text-gray-600">
                Verdora offers both free and premium plans. The free plan
                includes basic features, while premium plans unlock advanced
                tools and integrations.
              </p>
            </div>
            <div className="text-left">
              <h3 className="text-xl font-semibold text-[#226f54] mb-2">
                Can I integrate Verdora with other apps?
              </h3>
              <p className="text-gray-600">
                Yes! Verdora supports integration with popular tools like Google
                Drive, Notion, Zapier, and more.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="w-full bg-gray-800 text-gray-400 py-6">
        <div className="container mx-auto text-center">
          <p className="mb-4">
            Made with ❤️ by the Verdora Team. © 2024 Verdora, Inc. All rights
            reserved.
          </p>
          <div className="flex justify-center space-x-6">
            <a
              href="/about"
              className="hover:text-white transition-colors duration-300"
            >
              About Us
            </a>
            <a
              href="/terms"
              className="hover:text-white transition-colors duration-300"
            >
              Terms of Service
            </a>
            <a
              href="/privacy"
              className="hover:text-white transition-colors duration-300"
            >
              Privacy Policy
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
