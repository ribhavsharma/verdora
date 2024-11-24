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
      <section className="w-full py-16 px-24 md:px-24">
  <div className="container mx-auto">
    <h2 className="text-4xl font-bold text-[#226f54] mb-10 text-left">
      Features You'll Love
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div className="bg-gray-100 shadow-sm border rounded-lg p-6">
        <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
          Smart Waste Classification
        </h3>
        <p className="text-gray-600">
          Take a photo of your waste, and Verdora uses advanced AI to classify
          it into categories like recyclable materials, e-waste, clothing, and
          more.
        </p>
      </div>
      <div className="bg-gray-100 shadow-sm border rounded-lg p-6">
        <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
          Connect with Buyers
        </h3>
        <p className="text-gray-600">
          Turn your trash into treasure by connecting with potential buyers or
          recyclers who are interested in your classified items.
        </p>
      </div>
      <div className="bg-gray-100 shadow-sm border rounded-lg p-6">
        <h3 className="text-2xl font-semibold text-[#226f54] mb-4">
          Promote Sustainability
        </h3>
        <p className="text-gray-600">
          Reduce waste and promote a circular economy by ensuring items are
          recycled, reused, or sold rather than sent to landfills.
        </p>
      </div>
    </div>
  </div>
</section>

{/* FAQ Section */}
<section className="w-full py-16 px-24 md:px-24">
  <div className="container mx-auto">
    <h2 className="text-4xl font-bold text-[#226f54] mb-10 text-left">
      Frequently Asked Questions
    </h2>
    <div className="space-y-8 max-w-4xl">
      <div className="bg-white shadow-sm border rounded-lg p-6">
        <h3 className="text-xl font-semibold text-[#226f54] mb-2">
          What is Verdora?
        </h3>
        <p className="text-gray-600">
          Verdora is a sustainability platform that helps you classify waste
          using AI and connects you with buyers or recyclers, turning waste into
          opportunities while promoting eco-friendly practices.
        </p>
      </div>
      <div className="bg-white shadow-sm border rounded-lg p-6">
        <h3 className="text-xl font-semibold text-[#226f54] mb-2">
          How does Verdora classify waste?
        </h3>
        <p className="text-gray-600">
          Using advanced image recognition technology, Verdora identifies
          categories like recyclable items, e-waste, compostable materials, and
          more from a simple photo of the waste.
        </p>
      </div>
      <div className="bg-white shadow-sm border rounded-lg p-6">
        <h3 className="text-xl font-semibold text-[#226f54] mb-2">
          Can I sell items on Verdora?
        </h3>
        <p className="text-gray-600">
          Yes! Verdora helps you connect with buyers or recyclers who may be
          interested in purchasing or reusing your items, promoting a circular
          economy.
        </p>
      </div>
    </div>
  </div>
</section>

{/* Footer Section */}
<footer className="w-full bg-gray-800 text-gray-400 py-6">
  <div className="container mx-auto text-center">
    <p className="mb-4">
      Made with ❤️ to promote sustainability by the Verdora Team. © 2024 Verdora,
      Inc. All rights reserved.
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
