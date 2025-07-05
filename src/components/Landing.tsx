import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Shield, Users, Calendar, FileText, CreditCard } from 'lucide-react';

export default function Landing() {
  const features = [
    {
      icon: <Calendar className="w-8 h-8 text-blue-600" />,
      title: 'Easy Appointment Booking',
      description: 'Book appointments with qualified doctors at your convenience.'
    },
    {
      icon: <FileText className="w-8 h-8 text-green-600" />,
      title: 'Medical Records',
      description: 'Securely upload and manage your medical reports and documents.'
    },
    {
      icon: <Shield className="w-8 h-8 text-teal-600" />,
      title: 'Secure & Private',
      description: 'Your medical data is protected with enterprise-grade security.'
    },
    {
      icon: <Users className="w-8 h-8 text-purple-600" />,
      title: 'Expert Doctors',
      description: 'Connect with certified healthcare professionals.'
    },
    {
      icon: <CreditCard className="w-8 h-8 text-orange-600" />,
      title: 'Secure Payments',
      description: 'Safe and convenient payment processing for all services.'
    },
    {
      icon: <Heart className="w-8 h-8 text-red-600" />,
      title: 'Quality Care',
      description: 'Receive personalized healthcare tailored to your needs.'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-blue-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Your Health, <span className="text-blue-200">Our Priority</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
              Connect with qualified doctors, manage your medical records, and take control of your healthcare journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/register"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors"
              >
                Sign In
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose MedCare?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Experience modern healthcare with our comprehensive platform designed for both patients and doctors.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors">
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-green-600 to-teal-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your Healthcare Experience?
          </h2>
          <p className="text-xl mb-8 text-green-100">
            Join thousands of patients and doctors who trust MedCare for their healthcare needs.
          </p>
          <Link
            to="/register"
            className="bg-white text-green-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-green-50 transition-colors inline-block"
          >
            Start Your Journey
          </Link>
        </div>
      </section>
    </div>
  );
}