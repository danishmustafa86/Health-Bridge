import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { Calendar, FileText, CreditCard, User, Clock, Upload } from 'lucide-react';
import AppointmentBooking from './AppointmentBooking';
import MedicalRecords from './MedicalRecords';
import AppointmentHistory from './AppointmentHistory';
import Profile from './Profile';

export default function PatientDashboard() {
  const location = useLocation();
  const currentPath = location.pathname;

  const navigation = [
    { name: 'Overview', href: '/patient', icon: User },
    { name: 'Book Appointment', href: '/patient/book', icon: Calendar },
    { name: 'Medical Records', href: '/patient/records', icon: FileText },
    { name: 'Appointments', href: '/patient/appointments', icon: Clock },
    { name: 'Profile', href: '/patient/profile', icon: User },
  ];

  const stats = [
    { name: 'Upcoming Appointments', value: '2', icon: Calendar, color: 'bg-blue-500' },
    { name: 'Medical Records', value: '8', icon: FileText, color: 'bg-green-500' },
    { name: 'Consultations', value: '12', icon: Clock, color: 'bg-purple-500' },
    { name: 'Payments', value: '$240', icon: CreditCard, color: 'bg-orange-500' },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Patient Portal</h2>
        </div>
        <nav className="mt-6">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = currentPath === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-6 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={<PatientOverview stats={stats} />} />
          <Route path="/book" element={<AppointmentBooking />} />
          <Route path="/records" element={<MedicalRecords />} />
          <Route path="/appointments" element={<AppointmentHistory />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </div>
  );
}

function PatientOverview({ stats }: { stats: any[] }) {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, John!</h1>
        <p className="text-gray-600">Here's an overview of your healthcare journey.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link
              to="/patient/book"
              className="flex items-center p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
            >
              <Calendar className="w-5 h-5 text-blue-600 mr-3" />
              <span className="text-blue-700 font-medium">Book New Appointment</span>
            </Link>
            <Link
              to="/patient/records"
              className="flex items-center p-3 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
            >
              <Upload className="w-5 h-5 text-green-600 mr-3" />
              <span className="text-green-700 font-medium">Upload Medical Records</span>
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm text-gray-900">Appointment scheduled</p>
                <p className="text-xs text-gray-500">2 hours ago</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm text-gray-900">Blood test results uploaded</p>
                <p className="text-xs text-gray-500">1 day ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}