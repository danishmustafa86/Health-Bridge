import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { Users, FileText, Bell, User, Calendar, Activity } from 'lucide-react';
import PatientList from './PatientList';
import PatientRecords from './PatientRecords';
import DiagnosisNotes from './DiagnosisNotes';
import DoctorProfile from './DoctorProfile';

export default function DoctorDashboard() {
  const location = useLocation();
  const currentPath = location.pathname;

  const navigation = [
    { name: 'Overview', href: '/doctor', icon: Activity },
    { name: 'Patients', href: '/doctor/patients', icon: Users },
    { name: 'Records', href: '/doctor/records', icon: FileText },
    { name: 'Diagnosis', href: '/doctor/diagnosis', icon: FileText },
    { name: 'Profile', href: '/doctor/profile', icon: User },
  ];

  const stats = [
    { name: 'Total Patients', value: '47', icon: Users, color: 'bg-blue-500' },
    { name: 'Today\'s Appointments', value: '8', icon: Calendar, color: 'bg-green-500' },
    { name: 'Pending Records', value: '12', icon: FileText, color: 'bg-orange-500' },
    { name: 'Notifications', value: '3', icon: Bell, color: 'bg-purple-500' },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Doctor Portal</h2>
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
          <Route path="/" element={<DoctorOverview stats={stats} />} />
          <Route path="/patients" element={<PatientList />} />
          <Route path="/records" element={<PatientRecords />} />
          <Route path="/diagnosis" element={<DiagnosisNotes />} />
          <Route path="/profile" element={<DoctorProfile />} />
        </Routes>
      </div>
    </div>
  );
}

function DoctorOverview({ stats }: { stats: any[] }) {
  const todaysAppointments = [
    { id: '1', patient: 'John Doe', time: '9:00 AM', type: 'Checkup' },
    { id: '2', patient: 'Jane Smith', time: '10:30 AM', type: 'Follow-up' },
    { id: '3', patient: 'Bob Johnson', time: '2:00 PM', type: 'Consultation' },
  ];

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, Dr. Sarah!</h1>
        <p className="text-gray-600">Here's your practice overview for today.</p>
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

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Appointments</h3>
          <div className="space-y-3">
            {todaysAppointments.map((appointment) => (
              <div key={appointment.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{appointment.patient}</p>
                  <p className="text-sm text-gray-600">{appointment.type}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{appointment.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activities</h3>
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm text-gray-900">Diagnosis added for John Doe</p>
                <p className="text-xs text-gray-500">30 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm text-gray-900">Medical record reviewed</p>
                <p className="text-xs text-gray-500">1 hour ago</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
              <div>
                <p className="text-sm text-gray-900">New patient registered</p>
                <p className="text-xs text-gray-500">2 hours ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}