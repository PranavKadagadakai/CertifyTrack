import React from "react";
import { Link } from "react-router-dom";

function LandingPage() {
  return (
    <>

    {/* hello this is a PR from shubham */}
      <section className="bg-blue-600 text-white py-20 text-center">
        <h1 className="text-4xl md:text-5xl font-bold">
          Effortless Certificate Management
        </h1>
        <p className="mt-4 text-lg max-w-2xl mx-auto">
          CertifyTrack simplifies event-based certification, helping
          institutions manage and verify certificates seamlessly.
        </p>
        <div className="mt-8 space-x-4">
          <Link
            to="/signup"
            className="bg-white text-blue-600 px-6 py-3 rounded-lg shadow-md font-semibold hover:bg-gray-100"
          >
            Get Started
          </Link>
          <Link
            to="/login"
            className="bg-blue-500 text-white px-6 py-3 rounded-lg shadow-md font-semibold hover:bg-blue-700"
          >
            Log In
          </Link>
        </div>
      </section>

      <section className="py-16 bg-gray-100 text-center">
        <h2 className="text-3xl font-semibold text-gray-800">
          Why Choose CertifyTrack?
        </h2>
        <div className="container mx-auto grid md:grid-cols-3 gap-8 mt-10">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mt-4">Automated Generation</h3>
            <p className="text-gray-600 mt-2">
              Generate AICTE-compliant certificates instantly upon event
              completion.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mt-4">Easy Verification</h3>
            <p className="text-gray-600 mt-2">
              Mentors and institutions can verify certificates with a single
              click.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mt-4">Secure Storage</h3>
            <p className="text-gray-600 mt-2">
              All certificates are securely stored and accessible anytime.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}

export default LandingPage;
